from flask import Flask, send_from_directory, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('templates', 'index.html')




# @app.route("/jsonEndpoint")
# def json_mess():
#     return jsonify({"message":"Hello, world"}), 200

@app.route("/jsonEndpoint")
def json_mess():
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"message":curr_time}), 200

if __name__ == "__main__":
    app.run(debug=True, port=3000)
