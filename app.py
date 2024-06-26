from flask import Flask, render_template, request, make_response, jsonify
from dotenv import load_dotenv
import os
from db import collection
from datetime import datetime, timezone, timedelta

load_dotenv()
PORT = os.getenv("PORT")
MONGO_URL = os.getenv("MONGO_URL")

app = Flask(__name__)

def getUTCtime(dt_str):
    local_dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S%z")
    utc_dt = local_dt.astimezone(timezone.utc)
    return local_dt.astimezone(timezone.utc)

@app.route("/recieveEvents", methods=["POST"])
def eventReciever():
    data = request.get_json()
    event = request.headers["X-Github-Event"]
    print(event)
    if event == "push":
        collection.insert_one(
            {
                "request_id": data['head_commit']['id'],
                "author": data['pusher']['name'],
                "action": "PUSH",
                "from_branch": "-",
                "to-branch": data['ref'].split("/")[-1],
                "timestamp": datetime.now().utcnow(),
            }
        )
    elif event == "pull_request":
        if data['action'] == "opened":
            collection.insert_one(
                {
                    "request_id": data['pull_request']['id'],
                    "author": data['pull_request']['user']['login'],
                    "action": "PULL REQUEST",
                    "from_branch": data['pull_request']['head']['ref'],
                    "to-branch": data['pull_request']['base']['ref'],
                    "timestamp": datetime.now().utcnow(),
                }
            )
        elif data['action'] == "closed" and data['pull_request']['merged']:
            collection.insert_one(
                {
                    "request_id": data['pull_request']['id'],
                    "author": data['pull_request']['user']['login'],
                    "action": "MERGE",
                    "from_branch": data['pull_request']['head']['ref'],
                    "to-branch": data['pull_request']['base']['ref'],
                    "timestamp": datetime.now().utcnow(),
                }
            )
    return make_response({"status": 200, "message": "Event recieve successfully"})


@app.route("/")
def main():
    return render_template("./index.html")

@app.route('/fetch_data')
def fetch_data():
    query_param = request.args.get('last_time')
    if not query_param:
        return jsonify({"error": "Timestamp parameter is required"}), 400

    try:
        query_datetime = datetime.strptime(query_param, "%a, %d %b %Y %H:%M:%S %Z")
        print(query_param)
        results = collection.find({
            "timestamp": {"$gt": query_datetime}
        })
        result_list = []
        for result in results:
            result['_id'] = str(result['_id'])
            result_list.append(result)  
        if len(result_list) > 0:
            return jsonify({"data":result_list, "last_time":result_list[-1]['timestamp']})
        return jsonify({"data":[], "last_time":query_param})
    except ValueError as e:
        return jsonify({"error": "Invalid timestamp format"}), 400

if __name__ == "__main__":
    print(f"Application run on port {PORT}")
    app.run("localhost", port=PORT, debug=True)
