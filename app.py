from flask import Flask, render_template, request, make_response
from dotenv import load_dotenv
import os
from db import collection

load_dotenv()
PORT = os.getenv("PORT")
MONGO_URL = os.getenv("MONGO_URL")

app = Flask(__name__)


@app.route("/recieveEvents", methods=["POST"])
def eventReciever():
    data = request.get_json()
    event = request.headers["X-Github-Event"]
    print(event)
    print(data)
    if event == "push":
        collection.insert_one(
            {
                "request_id": data['head_commit']['id'],
                "author": data['pusher']['name'],
                "action": "PUSH",
                "from_branch": "-",
                "to-branch": data['ref'].split("/")[-1],
                "timestamp": data['head_commit']['timestamp'],
            }
        )
    elif event == "pull_request":
        collection.insert_one(
            {
                "request_id": data['pull_request']['id'],
                "author": data['user']['name'],
                "action": "PUSH",
                "from_branch": "-",
                "to-branch": data['ref'].split("/")[-1],
                "timestamp": data['updated_at'],
            }
        )
    return make_response({"status": 200, "message": "Event recieve successfully"})


@app.route("/")
def main():
    return render_template("./index.html")


if __name__ == "__main__":
    print(f"Application run on port {PORT}")
    app.run("localhost", port=PORT, debug=True)
