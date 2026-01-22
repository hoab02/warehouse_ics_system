from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/v1/events/robot", methods=["POST"])
def receive_robot_event():
    mission = request.json
    print("Received mission event:")
    print(mission)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
