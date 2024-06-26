from flask import Flask, render_template, request, make_response, jsonify
from dotenv import load_dotenv
import os
from db import collection
from datetime import datetime

# Load environment variables
load_dotenv()

# Retrieve environment variables
PORT = os.getenv("PORT")
MONGO_URL = os.getenv("MONGO_URL")

# Initialize Flask application
app = Flask(__name__)

@app.route("/recieveEvents", methods=["POST"])
def event_receiver():
    """
    Receive webhook events from GitHub and store them in MongoDB.

    Returns:
        HTTP response: Returns HTTP response to GitHub
    """
    data = request.get_json()
    event = request.headers.get("X-Github-Event")

    if event == "push":
        collection.insert_one({
            "request_id": data['head_commit']['id'],
            "author": data['pusher']['name'],
            "action": "PUSH",
            "from_branch": "-",
            "to_branch": data['ref'].split("/")[-1],
            "timestamp": datetime.utcnow().replace(microsecond=0),
        })
    elif event == "pull_request":
        if data['action'] == "opened":
            collection.insert_one({
                "request_id": data['pull_request']['id'],
                "author": data['pull_request']['user']['login'],
                "action": "PULL_REQUEST",
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow().replace(microsecond=0),
            })
        elif data['action'] == "closed" and data['pull_request']['merged']:
            collection.insert_one({
                "request_id": data['pull_request']['id'],
                "author": data['pull_request']['merged_by']['login'],
                "action": "MERGE",
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow().replace(microsecond=0),
            })

    return make_response({"status": 200, "message": "Event received successfully"})

@app.route("/")
def main():
    """
    Render the index.html page.

    Returns:
        template: Home page of the application
    """
    return render_template("index.html")

@app.route('/fetch_data')
def fetch_data():
    """
    Retrieve data from MongoDB based on timestamp parameter.

    Query Parameters:
        last_time (str): Timestamp of the last fetched data in "%a, %d %b %Y %H:%M:%S %Z" format.

    Returns:
        json-object: MongoDB documents based on last_time checkpoint
    """
    query_param = request.args.get('last_time')

    if not query_param:
        return jsonify({"error": "Timestamp parameter is required"}), 400

    try:
        query_datetime = datetime.strptime(query_param, "%a, %d %b %Y %H:%M:%S %Z")
        results = collection.find({
            "timestamp": {"$gt": query_datetime}
        })

        result_list = []
        for result in results:
            result['_id'] = str(result['_id'])
            result_list.append(result)

        if result_list:
            return jsonify({"data": result_list, "last_time": result_list[-1]['timestamp']})

        return jsonify({"data": [], "last_time": query_param})

    except ValueError:
        return jsonify({"error": "Invalid timestamp format"}), 400

if __name__ == "__main__":
    print(f"Application running on port {PORT}")
    app.run("localhost", port=PORT, debug=True)
