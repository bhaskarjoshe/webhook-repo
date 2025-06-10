from datetime import datetime
from datetime import timezone

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from app.extensions import mongo
from app.webhook.tasks import async_store_event

from ..settings.exception import InvalidGithubEvent
from ..settings.logger import logger

webhook = Blueprint("Webhook", __name__, url_prefix="/webhook")


def get_timestamp():
    """
    Helper function to get current time stamp
    """
    return datetime.now(timezone.utc).strftime("%d %B %Y - %I:%M:%S %p UTC")


def handle_push_event(payload):
    """
    Extract push event details from the GitHub webhook payload.
    """
    try:
        return {
            "request_id": payload.get("after"),
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": payload["ref"].split("/")[-1],
            "to_branch": payload["ref"].split("/")[-1],
        }
    except (KeyError, TypeError) as e:
        logger.error(f"Error parsing push event: {e}")
        raise


def handle_pull_request_event(payload):
    """
    Extract pull request event details if it's an open or merged PR.
    """
    try:
        pr = payload.get("pull_request", {})
        action = payload.get("action")
        if action == "opened":
            action_type = "PULL_REQUEST"
        elif action == "closed" and pr.get("merged", False):
            action_type = "MERGE"
        else:
            return None

        return {
            "request_id": pr.get("number"),
            "author": pr.get("user", {}).get("login"),
            "action": action_type,
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
        }
    except (KeyError, TypeError) as e:
        logger.error("Error parsing pull request event: %s", e)
        raise


def store_event(data):
    """
    Stores the retreived data in github_webhooks database
    """
    try:
        data["timestamp"] = get_timestamp()
        mongo.db.github_webhooks.insert_one(data)
    except Exception as e:
        logger.error("Failed to store event: %s", e)
        raise


@webhook.route("/receiver", methods=["GET", "POST"])
def receiver():
    if request.method == "GET":
        return render_template("index.html")

    try:
        if request.headers.get("Content-Type") != "application/json":
            logger.warning("Unsupported Content-Type")
            return jsonify({"error": "unsupported Content-Type"}), 400

        event_type = request.headers.get("X-GitHub-Event")
        payload = request.json

        if not payload:
            logger.warning("Missing JSON payload")
            return jsonify({"error": "missing JSON payload"}), 400

        logger.info(f"{event_type} Event occured")
        if event_type == "push":
            event_data = handle_push_event(payload)

        elif event_type == "pull_request":
            event_data = handle_pull_request_event(payload)
            if event_data is None:
                logger.info("Pull request ignored")
                return jsonify({"status": "ignored"}), 200

        else:
            raise InvalidGithubEvent(f"Unsupported event type: {event_type}")

        # store_event(event_data)
        # return jsonify({"status": "success"}), 200

        task = async_store_event.delay(event_data)
        return jsonify({"status": "queued", "task_id": task.id}), 202

    except InvalidGithubEvent as e:
        logger.error("InvalidGitHubEvent: %s", e)
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.exception(f"Unexpected error occurred {e}")
        return jsonify({"error": "internal server error"}), 500


@webhook.route("/events", methods=["GET"])
def get_events():
    """
    Retrieves all GitHub events from Mongo sorted by timestamp.
    """
    try:
        events = list(mongo.db.github_webhooks.find().sort("timestamp", -1))
        date_format = "%d %B %Y - %I:%M:%S %p %Z"
        utc_now = datetime.now(timezone.utc)
        last_15_seconds_event = []

        for event in events:
            event["_id"] = str(event["_id"])
            event_time = datetime.strptime(event["timestamp"], date_format)
            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=timezone.utc)

            diff = utc_now - event_time
            # if diff.total_seconds() > 15:
            #     break
            last_15_seconds_event.append(event)

        return jsonify(last_15_seconds_event)

    except Exception as e:
        logger.error("Error fetching events from DB: %s", e)
        return jsonify({"error": "could not retrieve events"}), 500
