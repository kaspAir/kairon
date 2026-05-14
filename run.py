from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/")
def index():
    return jsonify({
        "application": "KAIRON",
        "environment": os.getenv("FLASK_ENV", "unknown"),
        "status": "running"
    })

@app.get("/health")
def health():
    return jsonify({
        "status": "ok"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)