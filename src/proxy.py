import httpx
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urljoin
from src.config import (
    KEYCLOAK_SCOPE,
    SERVICE_ROUTES,
    KEYCLOAK_LOGIN_URL,
    KEYCLOAK_CLIENT_ID,
    TIMEOUT,
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


def get_request_headers(request: Request, token: str) -> dict:
    """Prepare headers for the forwarded request."""
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def send_streaming_request(target_url: str, request: Request):
    """Stream the response from the target service."""
    async with httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT)) as client:
        async with client.stream(
            method=request.method,
            url=target_url,
            headers=get_request_headers(request, request.cookies.get("access_token")),
            content=await request.body(),
        ) as response:
            yield {
                "status_code": response.status_code,
                "headers": {k: v for k, v in response.headers.items() if k.lower() != "content-encoding"},
            }

            async for chunk in response.aiter_bytes():
                yield chunk


async def stream_response(target_url: str, request: Request):
    """Stream response chunks with authentication checks."""
    token = request.cookies.get("access_token")

    if not token and not request.url.path.startswith("/callback"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    full_url = urljoin(target_url, request.url.path)
    if request.query_params:
        full_url += f"?{request.query_params}"

    try:
        async for chunk in send_streaming_request(full_url, request):
            yield chunk

    except httpx.RequestError as e:
        logger.error(f"Request to {target_url} failed: {e}")
        raise HTTPException(status_code=502, detail="Bad Gateway: Service Unavailable")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def forward_request(target_url: str, request: Request) -> StreamingResponse:
    """Forward the request to the appropriate service as a streamed response."""
    stream = stream_response(target_url, request)
    first_chunk = await anext(stream, None)

    if first_chunk is None:
        raise HTTPException(status_code=500, detail="No response received from backend")

    if isinstance(first_chunk, dict):
        status_code = first_chunk.get("status_code", 200)
        headers = {k: v for k, v in first_chunk.get("headers", {}).items()}

        headers.pop("content-encoding", None)

        return StreamingResponse(
            stream,
            status_code=status_code,
            headers=headers,
            media_type=headers.get("content-type", "application/octet-stream"),
        )

    raise HTTPException(status_code=500, detail="Malformed response from backend")
