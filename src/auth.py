import jwt
import httpx
from jwt import PyJWKClient
from fastapi import Header, HTTPException, Request
from src.config import (
    KEYCLOAK_JWKS_URL,
    KEYCLOAK_CLIENT_ID,
    KEYCLOAK_ISSUER,
    KEYCLOAK_CLIENT_SECRET,
    KEYCLOAK_SCOPE,
    KEYCLOAK_TOKEN_URL,
    REDIRECT_URL,
)
from src.logger import logger

jwks_client = PyJWKClient(KEYCLOAK_JWKS_URL)


def get_token_from_request(request: Request, authorization: str = Header(None)) -> str:
    """Retrieve JWT token from the Authorization header or cookies."""
    if authorization and authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1]

    token = request.cookies.get("access_token")
    if token:
        return token

    logger.warning("No token found, user is unauthorized")
    raise HTTPException(status_code=401, detail="Unauthorized")


def verify_token(request: Request, authorization: str = Header(None)) -> dict:
    """Validate JWT from Keycloak, checking both headers and cookies."""
    token = get_token_from_request(request, authorization)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=KEYCLOAK_CLIENT_ID,
            issuer=KEYCLOAK_ISSUER,
        )
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired, user must re-authenticate")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid token provided")
        raise HTTPException(status_code=401, detail="Invalid token")


async def exchange_code_for_token(code: str) -> dict:
    """Exchange an authorization code for an access token from Keycloak."""
    data = {
        "grant_type": "authorization_code",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URL,
        "scope": KEYCLOAK_SCOPE,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(KEYCLOAK_TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error exchanging code for token: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=502, detail="Failed to exchange code for token")
    except httpx.RequestError as e:
        logger.error(f"Network error during token exchange: {e}")
        raise HTTPException(
            status_code=502, detail="Keycloak authentication service unavailable")
