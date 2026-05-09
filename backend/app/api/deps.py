from functools import lru_cache

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_settings

settings = get_settings()
security = HTTPBearer()


@lru_cache(maxsize=1)
def _get_clerk_jwks() -> dict:
    """Fetch Clerk's public keys once and cache for the process lifetime."""
    resp = httpx.get(
        "https://api.clerk.com/v1/jwks",
        headers={"Authorization": f"Bearer {settings.clerk_secret_key}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    try:
        jwks = _get_clerk_jwks()
        header = jwt.get_unverified_header(token)
        # Find the matching key by kid
        key = next(
            (k for k in jwks.get("keys", []) if k.get("kid") == header.get("kid")),
            None,
        )
        if key is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown signing key")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        claims = jwt.decode(token, public_key, algorithms=["RS256"])
        user_id: str | None = claims.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
