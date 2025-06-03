from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from app.extensions import mongo

webhook = Blueprint("Webhook", __name__, url_prefix="/webhook")


def get_timestamp():
    """
    Helper function to get current time stamp
    """
    return datetime.now(timezone.utc).strftime("%d %B %Y - %I:%M %p UTC")


def handle_push_event(payload):
    """
    Extract push event details from the GitHub webhook payload.
    """
    return {
        "request_id": payload.get("after"),
        "author": payload["pusher"]["name"],
        "action": "PUSH",
        "from_branch": payload["ref"].split("/")[-1],
        "to_branch": payload["ref"].split("/")[-1],
    }


def handle_pull_request_event(payload):
    """
    Extract pull request event details if it's an open or merged PR.
    """
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


def store_event(data):
    """
    Stores the retreived data in github_webhooks database
    """
    data["timestamp"] = get_timestamp()
    mongo.db.github_webhooks.insert_one(data)


@webhook.route("/receiver", methods=["POST"])
def receiver():
    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"error": "unsupported Content-Type"}), 400

    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "push":
        event_data = handle_push_event(payload)

    elif event_type == "pull_request":
        event_data = handle_pull_request_event(payload)
        if event_data is None:
            return jsonify({"status": "ignored"}), 200

    else:
        return jsonify({"error": "event not supported"}), 400

    store_event(event_data)
    return jsonify({"status": "success"}), 200
