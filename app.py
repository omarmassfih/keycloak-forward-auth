from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.auth import exchange_code_for_token
from src.proxy import forward_request, get_matching_service
from src.config import (
    ALLOW_HEADERS,
    ALLOW_METHODS,
    FRONTEND_URL,
    KEYCLOAK_CLIENT_ID,
    KEYCLOAK_LOGIN_URL,
    KEYCLOAK_SCOPE,
    REDIRECT_URL,
    KEYCLOAK_LOGOUT_URL,
)
from src.logger import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[REDIRECT_URL],
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)


@app.get("/callback")
async def handle_callback(request: Request):
    """Handle Keycloak authentication callback and store tokens."""
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(
            status_code=400, detail="Missing authorization code")

    token_data = await exchange_code_for_token(code)
    id_token = token_data.get("id_token")
    access_token = token_data.get("access_token")

    if not access_token:
        logger.error(f"Failed to get tokens: {token_data}")
        raise HTTPException(status_code=400, detail="Failed to get tokens")

    response = RedirectResponse(url=FRONTEND_URL)
    response.set_cookie("access_token", access_token,
                        httponly=True, secure=True, samesite="Lax")

    if id_token:
        response.set_cookie("id_token", id_token,
                            httponly=True, secure=True, samesite="Lax")

    logger.info("User logged in successfully, redirecting to frontend")
    return response


@app.get("/logout")
async def logout(request: Request):
    """Log out the user, clear session, and redirect to Keycloak logout."""
    logger.info(
        f"Logout request received: {request.method}, Headers: {dict(request.headers)}")

    if "sec-purpose" in request.headers and "prefetch" in request.headers["sec-purpose"]:
        logger.warning("Ignoring prefetch request for /logout.")
        return Response(status_code=204)

    id_token = request.cookies.get("id_token")
    logout_url = f"{KEYCLOAK_LOGOUT_URL}?post_logout_redirect_uri={FRONTEND_URL}"

    if id_token:
        logout_url += f"&id_token_hint={id_token}"

    response = RedirectResponse(url=logout_url)
    response.delete_cookie("access_token", httponly=True,
                           secure=True, samesite="Lax")
    response.delete_cookie("id_token", httponly=True,
                           secure=True, samesite="Lax")

    logger.info("User session cleared, redirecting to Keycloak logout.")
    return response


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_request(request: Request):
    """Redirect requests to the correct service, ensuring authentication."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")

    token = request.cookies.get("access_token")
    if not token:
        logger.warning("Unauthorized request, redirecting to OIDC login")
        auth_url = (
            f"{KEYCLOAK_LOGIN_URL}?"
            f"client_id={KEYCLOAK_CLIENT_ID}&"
            f"response_type=code&"
            f"redirect_uri={REDIRECT_URL}&"
            f"scope={KEYCLOAK_SCOPE}"
        )
        return RedirectResponse(url=auth_url)

    matched_service = get_matching_service(request.url.path)
    if not matched_service:
        logger.warning(f"No matching service for {request.url.path}")
        raise HTTPException(status_code=404, detail="Service not found")

    return await forward_request(matched_service, request)
