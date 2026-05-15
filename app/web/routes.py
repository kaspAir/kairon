from flask import Blueprint, jsonify

api = Blueprint("api", __name__)


@api.get("/")
def index():
    return jsonify({
        "application": "KAIRON",
        "status": "running",
        "api_base": "/api",
        "decision_collection": "/api/decisions",
        "health": "/health",
    })


@api.get("/health")
def health():
    return jsonify({"status": "ok"})
