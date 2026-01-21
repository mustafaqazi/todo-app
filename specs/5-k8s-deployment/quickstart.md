# Quickstart: Phase IV Kubernetes Deployment Reference

**Purpose**: Quick reference guide for deploying Todo AI Chatbot to local Minikube cluster.

**Status**: Foundational Quickstart (T006)

---

## 60-Second Deployment Flow

```bash
# 1. Prerequisites
minikube start --driver=docker --cpus=4 --memory=8192

# 2. Build Docker Images
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
docker build -f docker/backend.Dockerfile -t todo-backend:latest .

# 3. Load into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# 4. Create Kubernetes Secret
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=BETTER_AUTH_SECRET="your-secret" \
  --from-literal=COHERE_API_KEY="cohere-api-key"

# 5. Deploy with Helm
helm install todo-backend k8s/helm-charts/todo-backend --set image.pullPolicy=Never
helm install todo-frontend k8s/helm-charts/todo-frontend --set image.pullPolicy=Never

# 6. Wait for Ready
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=60s
kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=60s

# 7. Access Frontend
minikube service todo-frontend
# Browser opens at: http://<minikube-ip>:30000
```

---

## Key Commands Reference

### Cluster Management

```bash
# Start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Check cluster status
minikube status

# Get cluster IP
minikube ip

# Access dashboard
minikube dashboard

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

### Docker Image Management

```bash
# Build frontend image
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .

# Build backend image
docker build -f docker/backend.Dockerfile -t todo-backend:latest .

# List local images
docker images | grep todo-

# Load image into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# List images in Minikube
minikube image ls | grep todo-
```

### Kubernetes Secret Management

```bash
# Create secret
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL="value1" \
  --from-literal=BETTER_AUTH_SECRET="value2" \
  --from-literal=COHERE_API_KEY="value3"

# List secrets
kubectl get secrets

# View secret (base64 decoded)
kubectl get secret app-secrets -o yaml

# Delete secret
kubectl delete secret app-secrets

# Recreate secret (after delete)
kubectl create secret generic app-secrets --from-literal=...
```

### Helm Chart Management

```bash
# Lint frontend chart
helm lint k8s/helm-charts/todo-frontend

# Lint backend chart
helm lint k8s/helm-charts/todo-backend

# Template frontend (preview output)
helm template todo-frontend k8s/helm-charts/todo-frontend

# Template backend (preview output)
helm template todo-backend k8s/helm-charts/todo-backend

# Install backend
helm install todo-backend k8s/helm-charts/todo-backend --set image.pullPolicy=Never

# Install frontend
helm install todo-frontend k8s/helm-charts/todo-frontend --set image.pullPolicy=Never

# List releases
helm list

# Upgrade deployment (change values)
helm upgrade todo-backend k8s/helm-charts/todo-backend --set replicaCount=2

# Rollback deployment
helm rollback todo-backend 1

# Uninstall deployment
helm uninstall todo-backend
helm uninstall todo-frontend
```

### Pod & Service Management

```bash
# List pods
kubectl get pods

# List pods with details
kubectl get pods -o wide

# Describe pod (troubleshooting)
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Execute command in pod
kubectl exec <pod-name> -- /bin/sh

# Port forward to pod
kubectl port-forward pod/<pod-name> 8000:8000

# List services
kubectl get svc

# Describe service
kubectl describe svc todo-backend

# Access frontend via Minikube
minikube service todo-frontend

# Wait for pod to be ready
kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=60s

# Check pod readiness/liveness probes
kubectl get pod <pod-name> -o yaml | grep -A20 "probes:"
```

### Verification & Health Checks

```bash
# Check all pods Running
kubectl get pods -o wide

# Check services accessible
kubectl get svc

# Backend health check
kubectl port-forward svc/todo-backend 8000:8000 &
curl http://localhost:8000/health

# Frontend health check (via Minikube)
minikube service todo-frontend
# Browser: open http://<minikube-ip>:30000

# Check readiness probe status
kubectl get pods -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")]}'

# Check if secrets mounted correctly
kubectl exec <pod-name> -- env | grep DATABASE_URL
```

---

## Common Troubleshooting

| Issue | Command to Diagnose | Fix |
|-------|---------------------|-----|
| Pod stuck in Pending | `kubectl describe pod <pod>` | Check image loaded: `minikube image ls \| grep todo-` |
| Pod in CrashLoopBackOff | `kubectl logs <pod>` | Check app health endpoint exists (/health) |
| Secret not mounted | `kubectl exec <pod> -- env \| grep DATABASE_URL` | Recreate secret: `kubectl delete/create secret` |
| Cannot reach frontend | `minikube service todo-frontend` | Check service NodePort: `kubectl get svc todo-frontend` |
| Helm install fails | `helm template todo-backend ...` (check YAML) | Validate: `helm lint k8s/helm-charts/todo-backend` |

---

## Directory Structure

```
Phase IV Deliverables:
├── docker/
│   ├── frontend.Dockerfile        # Multi-stage Next.js build
│   └── backend.Dockerfile         # Multi-stage FastAPI build
├── k8s/
│   ├── helm-charts/
│   │   ├── todo-frontend/
│   │   │   ├── Chart.yaml
│   │   │   ├── values.yaml
│   │   │   └── templates/
│   │   │       ├── deployment.yaml
│   │   │       ├── service.yaml
│   │   │       └── _helpers.tpl
│   │   ├── todo-backend/
│   │   │   ├── Chart.yaml
│   │   │   ├── values.yaml
│   │   │   └── templates/
│   │   │       ├── deployment.yaml
│   │   │       ├── service.yaml
│   │   │       └── _helpers.tpl
│   ├── secrets/
│   │   └── app-secrets-template.yaml    # Template (never commit real values)
│   ├── manifests/                       # Optional raw YAML
│   ├── DEMO.md                          # Step-by-step demo guide
│   ├── TROUBLESHOOTING.md              # Debugging guide
│   ├── ROLLBACK.md                     # Recovery procedures
│   └── HELM-GUIDE.md                   # Helm configuration reference
├── specs/infra/
│   ├── minikube-deployment.md          # Full deployment instructions
│   ├── helm-charts.md                  # Helm design specification
│   ├── docker-gordon.md                # Gordon AI Docker patterns
│   ├── ai-devops.md                    # kubectl-ai/Kagent patterns
│   └── PROMPTS.md                      # AI tool prompts used
└── .env.example                        # Environment variables template
```

---

## Key Files

### Phase IV Implementation

| File | Purpose | Status |
|------|---------|--------|
| `docker/frontend.Dockerfile` | Frontend container build | T015 (to be generated) |
| `docker/backend.Dockerfile` | Backend container build | T016 (to be generated) |
| `k8s/helm-charts/todo-frontend/Chart.yaml` | Frontend Helm metadata | T031 (to be generated) |
| `k8s/helm-charts/todo-frontend/values.yaml` | Frontend configuration | T032 (to be generated) |
| `k8s/helm-charts/todo-frontend/templates/deployment.yaml` | Frontend Deployment spec | T033 (to be generated) |
| `k8s/helm-charts/todo-frontend/templates/service.yaml` | Frontend Service spec | T034 (to be generated) |
| `k8s/helm-charts/todo-backend/Chart.yaml` | Backend Helm metadata | T026 (to be generated) |
| `k8s/helm-charts/todo-backend/values.yaml` | Backend configuration | T027 (to be generated) |
| `k8s/helm-charts/todo-backend/templates/deployment.yaml` | Backend Deployment spec | T028 (to be generated) |
| `k8s/helm-charts/todo-backend/templates/service.yaml` | Backend Service spec | T029 (to be generated) |
| `k8s/secrets/app-secrets-template.yaml` | Secret structure template | T023 (to be created) |
| `specs/infra/minikube-deployment.md` | Full deployment guide | T013, T085 (to be completed) |

---

## Next Steps

1. **Generate Dockerfiles**: Use Gordon AI (T015, T016)
2. **Create Helm Charts**: Use kubectl-ai (T026-T035)
3. **Deploy to Minikube**: Follow 60-second flow
4. **Validate**: Check all pods Running, services accessible
5. **Document**: Complete k8s/DEMO.md with tested walkthrough

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Data Model: `/specs/5-k8s-deployment/data-model.md`
- Research: `/specs/5-k8s-deployment/research.md`
