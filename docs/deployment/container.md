# **Running Keycloak Forward Auth Locally in a Container**

This guide explains how to **build, run, and test** the Keycloak Forward Auth locally using **Podman or Docker**.

---

## **1. Prerequisites**
- **Python 3.8+** (for local testing without a container)
- **Podman or Docker** (for containerized deployment)
- **Uvicorn** (ASGI server for running FastAPI)
- **Keycloak instance** (for authentication)

---

## **2. Clone the Repository**
```bash
git clone https://github.com/omarmassfih/keycloak-forward-auth.git
cd keycloak-forward-auth
```

---

## **3. Configure Environment Variables**
Copy the example `.env` file and update it with your Keycloak and backend service settings.

```bash
cp .env.example .env
```
Edit `.env` with the required values.

➡️ **For detailed environment variable setup, see**: [Configuration](../configuration/env.md)

---

## **4. Run the Application Locally (Without a Container)**
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the FastAPI application:
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```
Verify it's running:
```bash
curl http://localhost:8000
```

---

## **5. Build and Run in a Container**
### **Using Podman or Docker**
#### **5.1 Build the Image**
```bash
podman build -t keycloak-forward-auth .
# OR
docker build -t keycloak-forward-auth .
```

#### **5.2 Run the Container**
```bash
podman run --rm -p 8000:8000 --env-file .env keycloak-forward-auth
# OR
docker run --rm -p 8000:8000 --env-file .env keycloak-forward-auth
```

#### **5.3 Verify Running Container**
Check running containers:
```bash
podman ps
# OR
docker ps
```
Test the proxy:
```bash
curl http://localhost:8000
```
