# Data Model: Phase IV Kubernetes Deployment Entities

**Purpose**: Define core entities and their relationships for Phase IV Kubernetes deployment.

**Status**: Foundational Data Model (T005)

---

## Entity Definitions

### 1. Docker Image

**Definition**: Compiled, layered filesystem snapshot of an application (frontend or backend) ready to run in a container.

**Properties**:
- `name`: Image name (e.g., `todo-frontend`, `todo-backend`)
- `tag`: Image version/identifier (e.g., `latest`, `v1.0.0`)
- `registry`: Source registry (local Minikube, Docker Hub, etc.)
- `baseImage`: Base image used (e.g., `node:20-alpine`, `python:3.12-slim`)
- `size`: Compressed image size (target: <200MB frontend, <400MB backend)
- `layers`: Ordered list of filesystem layers
- `entrypoint`: Command executed when container starts
- `ports`: Exposed ports (80 for frontend, 8000 for backend)
- `nonRootUser`: UID 1000 (appuser) for security
- `buildDate`: When image was built (for audit trail)
- `vcsRef`: Git commit SHA image was built from

**Example**:
```yaml
Docker Image (Frontend):
  name: todo-frontend
  tag: latest
  baseImage: node:20-alpine (build) → nginx:alpine (final)
  size: 185MB
  ports: [80]
  nonRootUser: 1000 (appuser)
```

**Relationships**:
- Multiple versions of same image (tag variation)
- Referenced by Kubernetes Deployment (deployment.spec.containers[0].image)

---

### 2. Kubernetes Deployment

**Definition**: Declarative specification for running replicated pods of an image in the cluster.

**Properties**:
- `name`: Deployment name (e.g., `todo-backend`, `todo-frontend`)
- `namespace`: Kubernetes namespace (e.g., `default`)
- `replicas`: Desired pod count (typically 1 for Minikube, 2+ for production)
- `image`: Docker image reference (e.g., `todo-frontend:latest`)
- `imagePullPolicy`: How to obtain image (Never for Minikube, IfNotPresent for registry)
- `ports`: Container ports exposed (80, 8000)
- `env`: Environment variables (mounted from Secrets)
- `resources`: CPU/memory requests and limits
- `readinessProbe`: Determines if pod ready for traffic
- `livenessProbe`: Determines if pod should be restarted
- `labels`: Key-value pairs for identification (app=todo-frontend)
- `selector`: Which pods this deployment manages

**Example**:
```yaml
Kubernetes Deployment (Backend):
  name: todo-backend
  namespace: default
  replicas: 1
  image: todo-backend:latest
  imagePullPolicy: Never
  ports: [8000]
  env: [DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY] (from Secrets)
  resources:
    requests: {cpu: 100m, memory: 256Mi}
    limits: {cpu: 500m, memory: 512Mi}
  readinessProbe: HTTP GET /health (10s timeout, 3s delay)
  livenessProbe: HTTP GET /health (30s timeout, 15s delay)
  labels: {app: todo-backend, version: v1}
```

**Relationships**:
- Owns multiple Pod replicas (via selector matching)
- References Docker Image (by tag)
- Mounts Kubernetes Secret (envFrom.secretRef)
- Exposed by Kubernetes Service

---

### 3. Kubernetes Service

**Definition**: Stable network endpoint for accessing pods (load balancer for pod replicas).

**Properties**:
- `name`: Service name (e.g., `todo-frontend`, `todo-backend`)
- `type`: Service type (ClusterIP, NodePort, LoadBalancer)
- `selector`: Pods this service targets (e.g., `app: todo-backend`)
- `ports`: Port mappings (service port → container port)
- `clusterIP`: Internal cluster IP (auto-assigned for ClusterIP)
- `nodePort`: External port on each node (for NodePort type, e.g., 30000)

**Example**:
```yaml
Kubernetes Service (Frontend):
  name: todo-frontend
  type: NodePort
  selector: {app: todo-frontend}
  ports:
    - name: http
      port: 80
      targetPort: 80
      nodePort: 30000
  clusterIP: 10.96.0.1

Kubernetes Service (Backend):
  name: todo-backend
  type: ClusterIP
  selector: {app: todo-backend}
  ports:
    - name: http
      port: 8000
      targetPort: 8000
  clusterIP: 10.96.0.2
```

**Relationships**:
- Routes traffic to Pods via selector
- Created by Helm Service template (service.yaml)
- Referenced by frontend deployment (BACKEND_SERVICE_HOST env var)

---

### 4. Kubernetes Secret

**Definition**: Encrypted or encoded key-value store for sensitive configuration data.

**Properties**:
- `name`: Secret name (e.g., `app-secrets`)
- `namespace`: Kubernetes namespace
- `type`: Secret type (Opaque for generic key-value)
- `data`: Base64-encoded key-value pairs

**Contents** (3 required secrets):
- `DATABASE_URL`: PostgreSQL connection string (Neon)
- `BETTER_AUTH_SECRET`: JWT signing secret
- `COHERE_API_KEY`: Cohere API key for chatbot

**Example**:
```yaml
Kubernetes Secret (app-secrets):
  name: app-secrets
  namespace: default
  type: Opaque
  data:
    DATABASE_URL: cG9zdGdyZXM6Ly8gW2Jhc2U2NCBlbmNvZGVkXQ==
    BETTER_AUTH_SECRET: eW91ci1zZWN1cmUtcmFuZG9tLXNlY3JldC1oZXJl
    COHERE_API_KEY: Y29oLXNrLW... [base64]
```

**Relationships**:
- Mounted in Deployment via `envFrom.secretRef`
- Created manually before Helm install: `kubectl create secret generic`
- Never committed to git (template only in k8s/secrets/app-secrets-template.yaml)

---

### 5. Helm Chart

**Definition**: Templated Kubernetes resource package for deployment and configuration.

**Properties**:
- `name`: Chart name (e.g., `todo-frontend`, `todo-backend`)
- `version`: Chart version (e.g., `1.0.0`)
- `appVersion`: Application version chart deploys (e.g., `3.0.0`)
- `templates`: Jinja2-like templates for Deployment, Service, ConfigMap, etc.
- `values.yaml`: Configuration parameters (image, replicas, resources)
- `Chart.yaml`: Metadata (name, version, description)

**Structure**:
```
k8s/helm-charts/
├── todo-frontend/
│   ├── Chart.yaml                 # Metadata
│   ├── values.yaml                # Configuration parameters
│   └── templates/
│       ├── deployment.yaml        # Deployment template
│       ├── service.yaml           # Service template
│       └── _helpers.tpl           # Template helpers
├── todo-backend/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── _helpers.tpl
```

**Example values.yaml**:
```yaml
# Frontend values
replicaCount: 1
image:
  repository: todo-frontend
  tag: latest
  pullPolicy: Never
service:
  type: NodePort
  port: 80
  nodePort: 30000
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 200m
    memory: 256Mi
env:
  NEXT_PUBLIC_API_URL: http://todo-backend:8000
```

**Relationships**:
- Parametrizes Deployment, Service, ConfigMap
- Deployed with `helm install <chart>`
- References Docker Image (via values.yaml)
- Mounts Kubernetes Secret

---

## Entity Relationships Diagram

```
┌─────────────────────────────────────────────────────┐
│  Helm Chart (todo-frontend)                         │
│  └─ Chart.yaml, values.yaml, templates/           │
└──────────────────┬──────────────────────────────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
       v                       v
  ┌──────────────┐       ┌──────────────┐
  │ Deployment   │       │  Service     │
  │ (frontend)   │       │ (NodePort)   │
  └──────┬───────┘       └──────┬───────┘
         │                      │
         v                      v
   ┌──────────────┐       [External Port 30000]
   │ Pod Replicas │       (NodePort exposes)
   │ (containers) │
   └──────┬───────┘
          │
          v
   ┌──────────────────────────┐
   │ Docker Image             │
   │ (todo-frontend:latest)   │
   │ - Size: 185MB            │
   │ - Ports: [80]            │
   │ - User: UID 1000         │
   └──────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Kubernetes Secret (app-secrets)                    │
│  - DATABASE_URL                                     │
│  - BETTER_AUTH_SECRET                              │
│  - COHERE_API_KEY                                   │
└──────────────────┬──────────────────────────────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
    v                             v
[Frontend Deployment]      [Backend Deployment]
  (envFrom.secretRef)        (envFrom.secretRef)
```

---

## State Transitions

### Deployment Lifecycle

```
Image Build → Image Load → Helm Template → kubectl Apply → Pod Creation → Ready State

1. **Build Phase**:
   - Docker Image built locally (multi-stage)
   - Image tagged and available in Docker daemon

2. **Load Phase**:
   - `minikube image load todo-frontend:latest`
   - Image available inside Minikube cluster

3. **Template Phase**:
   - `helm template` renders Deployment YAML
   - values.yaml merged with templates/deployment.yaml
   - Output: Final Deployment spec

4. **Apply Phase**:
   - `helm install` applies rendered specs to cluster
   - Kubernetes accepts Deployment, Service specs

5. **Pod Phase**:
   - Deployment controller creates Pod replicas
   - Container starts (pulls image from Minikube local storage)

6. **Ready State**:
   - readinessProbe passes → Pod Ready
   - Service sends traffic to Ready pods
```

---

## Validation Checkpoints

| Entity | Validation Checkpoint |
|--------|----------------------|
| Docker Image | Image size <200MB (frontend), <400MB (backend); `docker images` shows correct tag |
| Deployment | `kubectl get deployment` shows desired/ready replicas; `kubectl describe` shows correct image |
| Service | `kubectl get svc` shows correct type (NodePort for frontend, ClusterIP for backend) |
| Secret | `kubectl get secrets app-secrets` exists; `kubectl get secret app-secrets -o yaml` shows 3 keys |
| Helm Chart | `helm lint` passes with no warnings; `helm template` produces valid YAML |

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Docker Patterns: `/specs/infra/docker-gordon.md`
- Helm Patterns: `/specs/infra/helm-charts.md`
