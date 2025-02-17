## Deploying to OpenShift

### 1. Create an OpenShift Project
```bash
oc new-project myproject
```

### 2. Define Configuration via ConfigMap
Create a `ConfigMap` to store environment variables.
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: keycloak-forward-auth-config
data:
  SERVICE_ROUTES_JSON: '{"/": "http://frontend:3000", "/api": "http://backend:8080"}'
  KEYCLOAK_ISSUER: "https://keycloak.example.com/auth/realms/myrealm"
  KEYCLOAK_JWKS_URL: "https://keycloak.example.com/auth/realms/myrealm/protocol/openid-connect/certs"
  KEYCLOAK_CLIENT_ID: "my-client-id"
  KEYCLOAK_CLIENT_SECRET: "my-client-secret"
  KEYCLOAK_LOGIN_URL: "https://keycloak.example.com/login"
  KEYCLOAK_LOGOUT_URL: "https://keycloak.example.com/protocol/openid-connect/logout"
  FRONTEND_URL: "https://frontend.example.com"
  REDIRECT_URL: "https://frontend.example.com/callback"
```
Apply the `ConfigMap`:
```bash
oc apply -f keycloak-forward-auth-config.yaml
```

➡️ **For detailed environment variable setup, see**: [Configuration](../configuration/env.md)

### 3. Deploy the Reverse Proxy
Create a deployment configuration.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keycloak-forward-auth
spec:
  replicas: 2
  selector:
    matchLabels:
      app: keycloak-forward-auth
  template:
    metadata:
      labels:
        app: keycloak-forward-auth
    spec:
      containers:
      - name: keycloak-forward-auth
        image: your-docker-registry/keycloak-forward-auth:latest
        ports:
          - containerPort: 8000
        envFrom:
          - configMapRef:
              name: keycloak-forward-auth-config
```
Apply the deployment:
```bash
oc apply -f keycloak-forward-auth-deployment.yaml
```

### 4. Expose the Reverse Proxy as a Service
Create a service for internal communication.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: keycloak-forward-auth
spec:
  selector:
    app: keycloak-forward-auth
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
```
Apply the service:
```bash
oc apply -f keycloak-forward-auth-service.yaml
```

### 5. Create an OpenShift Route
Expose the service externally using an OpenShift Route.
```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: keycloak-forward-auth-route
spec:
  host: proxy.myproject.com
  to:
    kind: Service
    name: keycloak-forward-auth
  port:
    targetPort: 8000
  tls:
    termination: edge
```
Apply the route:
```bash
oc apply -f keycloak-forward-auth-route.yaml
```
Now, the reverse proxy is accessible at:
```
https://proxy.myproject.com
```