## **Endpoints**

### **1. Handle Keycloak Authentication Callback**
#### **`GET /callback`**
##### **Description**
Handles the OAuth2 authentication callback from Keycloak.

##### **Request Parameters**
| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `code`    | `str` | ✅ Yes   | Authorization code received from Keycloak. |

##### **Response**
| Status Code | Description |
|-------------|-------------|
| `302 Found` | Redirects the user to the frontend after authentication. |
| `400 Bad Request` | Missing or invalid authorization code. |

##### **Example Request**
```http
GET /callback?code=abcd1234 HTTP/1.1
Host: proxy.example.com
```

##### **Example Response**
- **Success:** Redirects to the frontend with authentication cookies set.
- **Failure:** Returns `400 Bad Request` if the token exchange fails.

---

### **2. Logout and Invalidate Session**
#### **`GET /logout`**
##### **Description**
Logs out the user by:
- Clearing session cookies.
- Redirecting to Keycloak's logout endpoint.

##### **Response**
| Status Code | Description |
|-------------|-------------|
| `302 Found` | Redirects the user to Keycloak logout. |
| `204 No Content` | Ignores browser prefetch requests. |

##### **Example Request**
```http
GET /logout HTTP/1.1
Host: proxy.example.com
```

##### **Example Response**
- **Success:** Redirects to Keycloak logout.
- **Failure:** If no valid session exists, the user is still redirected to Keycloak logout.

---

### **3. Proxy Requests to Backend Services**
#### **`ANY /{full_path:path}`**
##### **Description**
Forwards authenticated requests to backend services dynamically.

##### **Request Parameters**
| Parameter    | Type   | Required | Description |
|-------------|--------|----------|-------------|
| `full_path` | `str`  | ✅ Yes   | Path of the requested resource (e.g., `/api/data`). |

##### **Authentication**
- **If authenticated:** Forwards the request to the correct backend service.
- **If not authenticated:** Redirects to Keycloak login.

##### **Response**
| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request is successfully forwarded. |
| `302 Found` | Redirects unauthenticated users to Keycloak login. |
| `404 Not Found` | No matching backend service found. |

##### **Example Request**
```http
GET /api/data HTTP/1.1
Host: proxy.example.com
Cookie: access_token=ey123...
```

##### **Example Response**
- **Success:** The request is forwarded to the backend service.
- **Failure:** If the user is not authenticated, they are redirected to Keycloak.

---

## **Authentication Mechanism**
- **Access tokens** are stored in HTTP-only cookies for security.
- **All requests** are authenticated before being forwarded.
- **CORS policies** are enforced to prevent unauthorized cross-origin requests.

---

## **Logging**
- Every request is logged with details such as:
  - **Method**, **URL**, and **authentication status**.
- Failed authentication attempts and missing backend services are **logged as warnings**.

---

## **Error Handling**
- **400 Bad Request** → Invalid authentication parameters.
- **404 Not Found** → No matching service for the requested path.
- **302 Found** → Redirects for authentication or logout flows.
