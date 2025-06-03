# GitHub Webhook Events Feed

This project displays GitHub webhook events (push, pull request, merge) on a simple web page. The backend uses Flask to receive webhook payloads, and the frontend dynamically fetches and displays these events in a scrollable container.

## Features

- Displays GitHub push, pull request, and merge events
- Real-time webhook event processing
- Scrollable event feed with the latest event labeled
- Clean and responsive UI
- MongoDB integration for event storage
- RESTful API endpoints

## Prerequisites

- Python 3.7 or higher
- MongoDB Atlas account (or local MongoDB instance)
- GitHub repository with admin access
- ngrok account (free tier works)

---

## Setup Instructions

### Code Setup

1. **Clone the repository and navigate to the project directory.**
   ```bash
   git clone https://github.com/bhaskarjoshe/webhook-repo.git
   cd webhook-repo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the flask application:**
   ```bash
   python run.py
   ```

5. **The endpoint is at:**
   ```bash
   GET http://127.0.0.1:5000/webhook/receiver
   ```

### ngrok Configuration

1. Download and install [ngrok](https://ngrok.com/).

2. Start ngrok to expose your local Flask server (assuming it's running on port 5000):
   ```bash
   ngrok http 5000
   ```

3. Copy the generated HTTPS forwarding URL (e.g., https://abcdef1234.ngrok.io).

4. In your GitHub repository, go to:
   ```
   Settings > Webhooks > Add webhook
   ```

5. Set the Payload URL to:
   ```
   https://abcdef1234.ngrok.io/receiver
   ```

6. Set the Content type to:
   ```
   application/json
   ```

7. Select the events you want to subscribe to (e.g., Push events, Pull requests).

8. Click Add webhook to save the configuration.

9. Ensure your Flask server is running locally to receive webhook events via the ngrok tunnel.

### Database Configuration

Create a `.env` file in the project root and add your MongoDB connection string:

```bash
# .env file
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name
```

See `.env.example` for reference.

## Project Structure

```
webhook-repo/
├── app/
│   ├── static
│   ├── templates
│   ├── webhook
│   │     ├── __init.py__
│   │     ├── routes.py
│   ├── __init__.py
│   └── extensions.py
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
├── run.py
├── .env.example
└── README.md
```

## API Endpoints


- `POST /webhook/receiver` - Webhook endpoint for GitHub events
- `GET /webhook/receiver` - Retrieve stored webhook events

## Troubleshooting

### Common Issues

1. **Webhook not receiving events**
   - Verify ngrok is running and the URL is correct
   - Check GitHub webhook delivery status in repository settings
   - Ensure Flask app is running on the correct port

2. **Database connection errors**
   - Verify MongoDB URI in `.env` file
   - Check network connectivity to MongoDB Atlas
   - Ensure database user has proper permissions

3. **ngrok tunnel issues**
   - Restart ngrok if the tunnel expires
   - Update GitHub webhook URL with new ngrok URL
   - Check ngrok account limits



## Notes

- Ngrok URLs are temporary and will change every time you restart ngrok unless you have a paid account
- Ensure the Flask app endpoint (`/receiver`) matches the webhook payload URL configured in GitHub
- The application listens for GitHub webhook events and stores them for display on the frontend
- Keep your `.env` file secure and never commit it to version control


## Author

- **Bhaskar Joshi** - [GitHub Profile](https://github.com/bhaskarjoshe)
