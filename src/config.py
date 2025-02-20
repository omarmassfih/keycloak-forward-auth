import os
import json
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def load_service_routes() -> Dict[str, Any]:
    """Load service routes dynamically from the SERVICE_ROUTES_JSON environment variable."""
    routes_env = os.getenv("SERVICE_ROUTES_JSON", "{}")

    try:
        routes = json.loads(routes_env)
        if not isinstance(routes, dict):
            raise ValueError("SERVICE_ROUTES_JSON must be a valid JSON object")

        logger.debug(f"Loaded service routes: {routes}")
        return routes
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse SERVICE_ROUTES_JSON: {e}")
        return {}


def get_env_var(name: str, default = "", required: bool = False) -> Optional[str]:
    """Retrieve an environment variable and optionally raise an error if missing."""
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_env_list(name: str, default: str = "") -> List[str]:
    """Retrieve an environment variable as a list, splitting by commas."""
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


SERVICE_ROUTES = load_service_routes()

KEYCLOAK_ISSUER = get_env_var("KEYCLOAK_ISSUER", required=True)
KEYCLOAK_JWKS_URL = get_env_var("KEYCLOAK_JWKS_URL", required=True)
KEYCLOAK_CLIENT_ID = get_env_var("KEYCLOAK_CLIENT_ID", required=True)
KEYCLOAK_CLIENT_SECRET = get_env_var("KEYCLOAK_CLIENT_SECRET", required=True)
KEYCLOAK_LOGIN_URL = get_env_var("KEYCLOAK_LOGIN_URL", required=True)
KEYCLOAK_LOGOUT_URL = get_env_var("KEYCLOAK_LOGOUT_URL", required=True)
REDIRECT_URL = get_env_var("REDIRECT_URL", required=True)
KEYCLOAK_SCOPE = get_env_var("KEYCLOAK_SCOPE", required=True)
FRONTEND_URL = get_env_var("FRONTEND_URL", required=True)

KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/token"

TIMEOUT = get_env_var("TIMEOUT", 300, required=False)
ALLOW_METHODS = get_env_list("ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
ALLOW_HEADERS = get_env_list("ALLOW_HEADERS", "Authorization,Content-Type")

logger.info("Keycloak configuration loaded successfully.")
logger.info(f"Allowed methods: {ALLOW_METHODS}")
logger.info(f"Allowed headers: {ALLOW_HEADERS}")
