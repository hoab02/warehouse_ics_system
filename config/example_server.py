from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/v1/events/robot", methods=["POST"])
def receive_robot_task_event():
    mission = request.json
    print("Received TASK event:")
    print(mission)
    return jsonify({"status": "ok"})


@app.route("/api/v1/events/scenario", methods=["POST"])
def receive_robot_scenario_event():
    mission = request.json
    print("Received SCENARIO event:")
    print(mission)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
