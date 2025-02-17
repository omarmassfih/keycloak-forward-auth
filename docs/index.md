# Keycloak Forward Auth

A FastAPI-based Forward Authentication (Forward Auth) service that secures backend services using Keycloak authentication. It integrates with a reverse proxy (Traefik, Nginx, or Envoy) to validate requests before forwarding them to backend services. Supports dynamic routing via Kubernetes/OpenShift DNS.

## 🚀 Features

- **Keycloak authentication enforcement** with JWT
- **Asynchronous request forwarding** via `httpx`
- **Dynamic routing** using DNS & environment variables
- **Secure session management** including logout handling
- **Containerized with Podman & Docker**
- **Supports OpenShift/Kubernetes deployments**

## 📖 Documentation Sections

- **Installation** → Setting up dependencies and local development
- **Configuration** → Managing environment variables & OpenShift setup
- **Authentication** → Keycloak integration, login, and logout handling
- **Deployment** → Running with Podman, Docker, and Kubernetes
- **API Reference** → Proxy and authentication endpoints

🔗 **Source Code**: [GitHub Repository](https://github.com/omarmassfih/keycloak-forward-auth)
