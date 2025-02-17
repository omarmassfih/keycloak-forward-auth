## **Example `.env` File**
```ini
# Keycloak Configuration
KEYCLOAK_ISSUER=https://keycloak.example.com/auth/realms/myrealm
KEYCLOAK_JWKS_URL=https://keycloak.example.com/auth/realms/myrealm/protocol/openid-connect/certs
KEYCLOAK_CLIENT_ID=my-client-id
KEYCLOAK_CLIENT_SECRET=my-client-secret
KEYCLOAK_LOGIN_URL=https://keycloak.example.com/login
KEYCLOAK_LOGOUT_URL=https://keycloak.example.com/protocol/openid-connect/logout
KEYCLOAK_SCOPE="openid email profile"

# Service Routing (JSON format)
SERVICE_ROUTES_JSON={" /": "http://frontend:3000", "/api": "http://backend:8080"}

# Redirect URL after login
REDIRECT_URL=https://frontend.example.com/callback

# Frontend URL
FRONTEND_URL=https://frontend.example.com

# CORS Settings
ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOW_HEADERS=Authorization,Content-Type
```

---

## **Keycloak Authentication**
These variables define authentication settings:

| Variable                 | Description                                        |
|--------------------------|----------------------------------------------------|
| `KEYCLOAK_ISSUER`        | Keycloak realm URL                                |
| `KEYCLOAK_JWKS_URL`      | JSON Web Key Set (JWKS) URL                       |
| `KEYCLOAK_CLIENT_ID`     | Keycloak client ID                                |
| `KEYCLOAK_CLIENT_SECRET` | Client secret for authentication                  |
| `KEYCLOAK_LOGIN_URL`     | Login endpoint for Keycloak                       |
| `KEYCLOAK_LOGOUT_URL`    | Logout endpoint for Keycloak                      |
| `KEYCLOAK_SCOPE`         | Scopes requested (e.g., `"openid email profile"`) |

---

## **Service Routing**
| Variable               | Description                                        |
|------------------------|----------------------------------------------------|
| `SERVICE_ROUTES_JSON`  | JSON object mapping paths (`"/api"`, `"/"`) to backend services |

---

## **CORS Settings**
These variables define allowed **HTTP methods** and **headers**:

| Variable         | Description                                             |
|-----------------|---------------------------------------------------------|
| `ALLOW_METHODS` | Allowed HTTP methods (e.g., `GET, POST, PUT, DELETE, OPTIONS`) |
| `ALLOW_HEADERS` | Allowed HTTP headers (e.g., `Authorization, Content-Type`) |

---

## **Frontend & Redirect URLs**
| Variable        | Description                                        |
|----------------|----------------------------------------------------|
| `FRONTEND_URL` | Base URL of the frontend                          |
| `REDIRECT_URL` | URL where users are redirected after authentication |
