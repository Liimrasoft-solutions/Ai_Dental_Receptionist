"""Auth for people (dashboard) and for machines (agents sending events)."""
import hashlib
import hmac
import time
from dataclasses import dataclass

from fastapi import Header, HTTPException

from .config import settings

MAX_SKEW_SECONDS = 300


@dataclass
class User:
    email: str
    role: str  # admin | manager | staff
    location_ids: list[str] | None = None  # None = all locations


def current_user(authorization: str | None = Header(None)) -> User:
    if settings.auth_mode == "dev":
        return User(email="dev@localhost", role="admin")
    # TODO(cognito): verify the JWT from Authorization: Bearer <token> against the
    # Cognito user pool JWKS, then read role and location ids from token groups/claims.
    raise HTTPException(401, "Sign-in is not configured. Set AUTH_MODE=dev for local work.")


def require_role(user: User, *roles: str) -> None:
    if user.role not in roles:
        raise HTTPException(403, f"This action needs one of these roles: {', '.join(roles)}")


def sign(secret: str, timestamp: str, body: bytes) -> str:
    mac = hmac.new(secret.encode(), timestamp.encode() + b"." + body, hashlib.sha256)
    return "sha256=" + mac.hexdigest()


def verify_signed(secret: str, timestamp: str | None, signature: str | None, body: bytes) -> None:
    """Agents sign `{timestamp}.{raw body}` with their source secret (HMAC-SHA256)."""
    if not timestamp or not signature:
        raise HTTPException(401, "Missing X-Hub-Timestamp or X-Hub-Signature header")
    try:
        ts = int(timestamp)
    except ValueError:
        raise HTTPException(401, "X-Hub-Timestamp must be Unix seconds")
    if abs(time.time() - ts) > MAX_SKEW_SECONDS:
        raise HTTPException(401, "X-Hub-Timestamp is more than 5 minutes off")
    if not hmac.compare_digest(sign(secret, timestamp, body), signature):
        raise HTTPException(401, "Signature does not match")
