from __future__ import annotations

from flask import request

DEFAULT_ACTOR = "system"


def actor_from_request(payload: dict | None = None) -> str:
    """Resolve the technical actor for auditable create operations.

    MVP rule: accept an explicit non-default created_by field in JSON for tests and
    manual API use. Otherwise prefer lightweight headers, then default to system.
    This is intentionally not IAM yet.
    """
    payload = payload or {}
    payload_actor = str(payload.get("created_by") or "").strip()
    if payload_actor and payload_actor != DEFAULT_ACTOR:
        return payload_actor

    header_actor = (
        request.headers.get("X-Kairon-User")
        or request.headers.get("X-User")
        or ""
    )
    header_actor = str(header_actor).strip()
    if header_actor:
        return header_actor

    return DEFAULT_ACTOR
