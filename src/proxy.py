import httpx
from fastapi import Request, HTTPException
from fastapi.responses import Response, RedirectResponse
from src.config import (
    KEYCLOAK_SCOPE,
    SERVICE_ROUTES,
    KEYCLOAK_LOGIN_URL,
    KEYCLOAK_CLIENT_ID,
)
from src.logger import logger


def get_matching_service(path: str) -> str:
    """Find the matching service using the first segment of the path."""
    path_segments = path.strip("/").split("/")
    first_segment = f"/{path_segments[0]}" if path_segments else "/"
    return SERVICE_ROUTES.get(first_segment, SERVICE_ROUTES.get("/", ""))


def construct_login_redirect_url(request: Request) -> str:
    """Construct the Keycloak login URL for redirecting unauthorized users."""
    return (
        f"{KEYCLOAK_LOGIN_URL}?"
        f"client_id={KEYCLOAK_CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={request.url.scheme}://{request.url.netloc}/callback&"
        f"scope={KEYCLOAK_SCOPE}"
    )


async def forward_request(target_url: str, request: Request) -> Response:
    """Forward the request to the appropriate service, ensuring authentication."""
    try:
        token = request.cookies.get("access_token")

        if not token:
            if not request.url.path.startswith("/callback"):
                logger.warning(
                    f"Unauthorized request to {request.url.path}, redirecting to login")
                return RedirectResponse(url=construct_login_redirect_url(request))
            logger.info("Skipping login redirect: Already in callback flow")

        full_url = f"{target_url}{request.url.path}"
        if request.query_params:
            full_url += f"?{request.query_params}"

        headers = {
            key: value for key, value in request.headers.items() if key.lower() != "host"
        }
        headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=full_url,
                headers=headers,
                content=await request.body(),
            )

        excluded_headers = {"content-encoding", "transfer-encoding"}
        filtered_headers = {k: v for k, v in response.headers.items(
        ) if k.lower() not in excluded_headers}

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=filtered_headers,
        )

    except httpx.RequestError as e:
        logger.error(f"Request to {target_url} failed: {e}")
        raise HTTPException(
            status_code=502, detail="Bad Gateway: Service Unavailable")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
