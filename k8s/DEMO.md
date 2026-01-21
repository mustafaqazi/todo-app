# Phase IV Kubernetes Deployment Guide: End-to-End Demo

**Purpose**: Step-by-step walkthrough for deploying Todo AI Chatbot to local Minikube cluster.

**Status**: Complete deployment instructions (T013, T061, T085, T135)

**Target**: Get working demo in <5 minutes after prerequisites are met

---

## Prerequisites

Ensure you have installed:
- [ ] Docker Desktop (with Docker daemon running)
- [ ] Minikube (`minikube version` should show installed)
- [ ] kubectl (`kubectl version` should show client version)
- [ ] Helm (`helm version` should show v3+)
- [ ] Image built: `docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .`
- [ ] Image built: `docker build -f docker/backend.Dockerfile -t todo-backend:latest .`
- [ ] Environment variables: DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY (from `.env`)

---

## Demo Walkthrough: <5 Minutes

### Step 1: Start Minikube Cluster (1 minute)

```bash
# Start Minikube with sufficient resources
minikube start --driver=docker --cpus=4 --memory=8192

# Verify cluster is running
minikube status
```

**Expected Output**:
```
minikube: Running
profile: minikube
driver: docker
apiserver: Running
kubeconfig: Configured
```

### Step 2: Load Docker Images into Minikube (1 minute)

```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest

# Verify images are loaded
minikube image ls | grep todo-
```

**Expected Output**:
```
docker.io/library/todo-backend:latest
docker.io/library/todo-frontend:latest
```

### Step 3: Create Kubernetes Secret (30 seconds)

```bash
# Create app-secrets with your environment values
# Replace YOUR_DATABASE_URL, YOUR_BETTER_AUTH_SECRET, YOUR_COHERE_API_KEY with actual values

kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL="YOUR_DATABASE_URL" \
  --from-literal=BETTER_AUTH_SECRET="YOUR_BETTER_AUTH_SECRET" \
  --from-literal=COHERE_API_KEY="YOUR_COHERE_API_KEY"

# Verify secret created
kubectl get secrets
```

**Expected Output**:
```
NAME           TYPE     DATA   AGE
app-secrets    Opaque   3      2s
```

### Step 4: Deploy Backend with Helm (30 seconds)

```bash
# Deploy backend service
helm install todo-backend k8s/helm-charts/todo-backend \
  --set image.pullPolicy=Never

# Verify deployment
kubectl get deployments
```

**Expected Output**:
```
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
todo-backend    1/1     1            1           5s
```

### Step 5: Deploy Frontend with Helm (30 seconds)

```bash
# Deploy frontend service
helm install todo-frontend k8s/helm-charts/todo-frontend \
  --set image.pullPolicy=Never

# Verify deployment
kubectl get deployments
```

**Expected Output**:
```
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
todo-backend     1/1     1            1           10s
todo-frontend    1/1     1            1           5s
```

### Step 6: Wait for Pods Ready (1 minute)

```bash
# Wait for backend pod to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-backend --timeout=60s

# Wait for frontend pod to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-frontend --timeout=60s

# Check all pods
kubectl get pods
```

**Expected Output**:
```
NAME                            READY   STATUS    RESTARTS   AGE
todo-backend-xxx-yyy            1/1     Running   0          5s
todo-frontend-xxx-yyy           1/1     Running   0          5s
```

### Step 7: Access Frontend (30 seconds)

```bash
# Open frontend in browser
minikube service todo-frontend

# Or manually get the URL
minikube service todo-frontend --url
```

**Expected**: Browser opens to http://<minikube-ip>:30000 showing Todo app login page

---

## Validation Steps (E2E Testing)

### Health Checks

```bash
# Check backend health endpoint
kubectl port-forward svc/todo-backend 8000:8000 &
curl http://localhost:8000/health
# Expected: {"status": "ok"} or similar

# Check frontend health
kubectl port-forward svc/todo-frontend 80:80 &
curl http://localhost/health
# Expected: 200 OK
```

### User Interaction Test

1. **Login/Signup**:
   - Visit http://<minikube-ip>:30000
   - Create account with email: `test@example.com`
   - Set password: `TestPassword123!`
   - Verify redirect to task dashboard

2. **Create Task**:
   - Click "Add Task" button
   - Enter title: "Test Task"
   - Click "Create"
   - Verify task appears in list

3. **Edit Task**:
   - Click edit icon on task
   - Change title to "Updated Task"
   - Save
   - Verify title updated

4. **Mark Complete**:
   - Click checkbox next to task
   - Verify visual state changes (strikethrough)
   - Verify backend persists state

5. **Delete Task**:
   - Click delete icon
   - Confirm deletion
   - Verify task removed from list

6. **Test Chatbot** (if Cohere API is configured):
   - Click chatbot button (bottom-right)
   - Send message: "Show me my tasks"
   - Verify response from Cohere API
   - Verify chatbot can access user's tasks

7. **User Isolation**:
   - In separate browser/incognito: Create new account
   - Verify User B cannot see User A's tasks
   - Verify User B can only see their own tasks

---

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Pod stuck in Pending | `kubectl describe pod <pod>` | Check image loaded: `minikube image ls` |
| Pod in CrashLoopBackOff | `kubectl logs <pod>` | Check app startup errors, health endpoint |
| Cannot access frontend | `minikube service todo-frontend` | Verify NodePort 30000 is open |
| Backend communication error | `kubectl logs <frontend-pod>` | Verify `NEXT_PUBLIC_API_URL` env var set correctly |
| Secrets not mounted | `kubectl exec <pod> -- env` | Verify secret created: `kubectl get secrets` |

### Detailed Debugging

```bash
# Get detailed pod info
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Stream pod logs
kubectl logs -f <pod-name>

# Get pod events
kubectl get events --sort-by='.lastTimestamp'

# Execute shell in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port-forward to pod for manual testing
kubectl port-forward pod/<pod-name> 8000:8000
```

---

## Cleanup

### Remove Deployments

```bash
# Uninstall Helm releases
helm uninstall todo-backend
helm uninstall todo-frontend

# Verify deleted
kubectl get deployments
```

### Remove Secrets

```bash
# Delete secret
kubectl delete secret app-secrets

# Verify deleted
kubectl get secrets
```

### Stop Minikube

```bash
# Stop cluster (keeps disk state)
minikube stop

# Delete cluster (full cleanup)
minikube delete
```

---

## Advanced: Scaling & Monitoring

### Scale Frontend to 3 Replicas

```bash
# Update Helm values
helm upgrade todo-frontend k8s/helm-charts/todo-frontend \
  --set replicaCount=3 \
  --set image.pullPolicy=Never

# Verify 3 pods running
kubectl get pods -l app.kubernetes.io/name=todo-frontend
```

### Monitor Cluster Health

```bash
# Dashboard
minikube dashboard

# Resource usage
kubectl top pods

# Watch deployments
kubectl get deployments -w
```

### View All Resources

```bash
# All pods
kubectl get pods -A

# All services
kubectl get svc

# All deployments
kubectl get deployments

# All secrets
kubectl get secrets
```

---

## Rollback

### If Deployment Fails

```bash
# Check Helm release history
helm history todo-backend

# Rollback to previous version
helm rollback todo-backend 1

# Verify rollback
kubectl get pods
```

---

## Docker Build Reference

### Build Frontend Image

```bash
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
```

### Build Backend Image

```bash
docker build -f docker/backend.Dockerfile -t todo-backend:latest .
```

### Verify Image Sizes

```bash
docker images | grep todo-
# Expected:
# todo-frontend  latest  xxxxx  ~180MB  (target: <200MB)
# todo-backend   latest  xxxxx  ~350MB  (target: <400MB)
```

---

## References

- Helm Documentation: https://helm.sh/docs/
- Kubernetes Documentation: https://kubernetes.io/docs/
- Minikube Documentation: https://minikube.sigs.k8s.io/docs/
- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Research & Decisions: `/specs/5-k8s-deployment/research.md`
- Quickstart: `/specs/5-k8s-deployment/quickstart.md`

---

**Status**: Ready for hackathon demo
**Last Updated**: 2026-01-21
**Maintainer**: Todo Project Team
