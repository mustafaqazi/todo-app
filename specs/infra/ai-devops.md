# AI-Assisted DevOps Specification: kubectl-ai & Kagent Patterns

**Purpose**: Document kubectl-ai and Kagent usage for generating and validating Kubernetes manifests and Helm charts.

**Status**: To be completed during Phase 2 (Foundational) & Phase 5 (User Story 3)

---

## Helm Chart Structure Patterns (T008: Research)

### Standard Helm Directory Structure

```
k8s/helm-charts/todo-backend/
├── Chart.yaml              # Metadata (name, version, description, appVersion)
├── values.yaml             # Default configuration values (replicaCount, image, service, resources)
├── values-prod.yaml        # (Optional) Production value overrides
├── templates/
│   ├── deployment.yaml     # Deployment spec (uses .Values for all parameters)
│   ├── service.yaml        # Service spec (ClusterIP for backend)
│   ├── configmap.yaml      # (Optional) Non-sensitive configuration
│   ├── _helpers.tpl        # Helpers for labels, selectors, naming
│   └── NOTES.txt           # (Optional) Post-install instructions
└── .helmignore             # Files to exclude from chart

k8s/helm-charts/todo-frontend/
├── Chart.yaml              # Metadata
├── values.yaml             # Configuration values  (service: NodePort, replicas, resources)
├── templates/
│   ├── deployment.yaml     # Deployment spec with ingress/routing
│   ├── service.yaml        # Service spec (NodePort for browser access)
│   ├── _helpers.tpl        # Helpers
│   └── NOTES.txt
└── .helmignore
```

### Key Principles (T008)

1. **values.yaml-Driven**: All parameters in values.yaml; NO hardcoded values in templates
   - Example: `replicaCount: {{ .Values.replicaCount }}` NOT `replicaCount: 1`
   - Benefit: Helm install with `--values custom.yaml` or `--set` overrides all parameters

2. **_helpers.tpl Template Helpers**: Reduces duplication across deployment/service templates
   ```
   {{- define "todo-backend.labels" -}}
   app.kubernetes.io/name: {{ .Chart.Name }}
   app.kubernetes.io/instance: {{ .Release.Name }}
   {{- end }}
   ```

3. **Probe Configuration**: Readiness and liveness probes parameterized
   ```yaml
   # values.yaml
   probes:
     readiness:
       enabled: true
       initialDelaySeconds: 10
       timeoutSeconds: 3
       periodSeconds: 30
     liveness:
       enabled: true
       initialDelaySeconds: 15
       timeoutSeconds: 3
       periodSeconds: 30
   ```

4. **Secret Reference Pattern**: Don't embed secrets in templates
   ```yaml
   # deployment.yaml template
   envFrom:
   - secretRef:
       name: {{ .Values.secrets.name }}  # e.g., "app-secrets"
   ```

5. **Resource Limits & Requests**: Always include for production
   ```yaml
   # values.yaml
   resources:
     requests:
       cpu: 100m
       memory: 256Mi
     limits:
       cpu: 500m
       memory: 512Mi
   ```

---

## kubectl-ai & Kagent Usage Patterns (T010: Research & Documentation)

### kubectl-ai Prompts for Helm Chart Generation

#### Prompt 1: Backend Helm Chart Structure

```
Generate a Kubernetes-ready Helm chart for a FastAPI backend service:

Requirements:
- Chart name: todo-backend (version 1.0.0)
- Service type: ClusterIP (internal cluster communication)
- Port: 8000 (HTTP API)
- Default replicas: 1 (configurable via values.yaml)
- Image: todo-backend:latest (pull from local Minikube, Never policy)
- Non-root user: UID 1000
- Readiness probe: HTTP GET /health (delay 10s, timeout 3s)
- Liveness probe: HTTP GET /health (delay 15s, timeout 3s)
- Resource requests: 100m CPU, 256Mi memory
- Resource limits: 500m CPU, 512Mi memory
- Env vars: DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY (from Kubernetes Secret)

Output structure:
- Chart.yaml (metadata with name, version, description)
- values.yaml (all configurable parameters, NO hardcoded secrets)
- templates/deployment.yaml (uses .Values for all params)
- templates/service.yaml (ClusterIP service)
- templates/_helpers.tpl (label/selector templates)

Validate:
- helm lint passes with no errors
- helm template produces valid YAML
- All values referenced via .Values.*
- No plain-text secrets in templates or values.yaml
```

#### Prompt 2: Frontend Helm Chart Structure

```
Generate a Kubernetes-ready Helm chart for a Next.js frontend service:

Requirements:
- Chart name: todo-frontend (version 1.0.0)
- Service type: NodePort (external browser access)
- Port: 80 (HTTP) on NodePort 30000
- Default replicas: 1 (configurable)
- Image: todo-frontend:latest (pull from local Minikube, Never policy)
- Non-root user: UID 1000
- Readiness probe: HTTP GET / (delay 10s, timeout 3s)
- Liveness probe: HTTP GET / (delay 15s, timeout 3s)
- Resource requests: 100m CPU, 128Mi memory
- Resource limits: 200m CPU, 256Mi memory
- Env var: NEXT_PUBLIC_API_URL (backend service URL for internal communication)

Output structure:
- Chart.yaml (metadata)
- values.yaml (configurable parameters, no hardcoded env values)
- templates/deployment.yaml (uses .Values, mounts API_URL as env)
- templates/service.yaml (NodePort on 30000)
- templates/_helpers.tpl (helpers)

Validate:
- helm lint passes
- helm template produces valid YAML
- Service type is NodePort with nodePort: 30000
- All parameterized via .Values.*
```

### kubectl-ai Capabilities (T010)

kubectl-ai will assist with:
- ✅ Generate Chart.yaml with correct metadata
- ✅ Create values.yaml with all configurable parameters
- ✅ Generate deployment.yaml using .Values templating
- ✅ Create service.yaml with correct type and port configuration
- ✅ Generate _helpers.tpl with label and selector templates
- ✅ Validate Helm syntax and structure
- ✅ Suggest best practices (secrets mounting, probe configuration, resource limits)

### Kagent Usage Patterns

#### Prompt 1: Cluster Health Analysis

```
Analyze the health of this Minikube Kubernetes cluster:
- Check all pods in default namespace (status, readiness, restarts)
- Verify all services are running (endpoints, traffic routing)
- Check resource usage (CPU, memory per pod)
- Identify any pods in error states (Pending, CrashLoopBackOff, etc.)
- Recommend optimizations for local development

Output:
- Pods status table (name, status, ready/total, restarts, age)
- Services status (name, type, cluster IP, ports)
- Resource utilization (requests vs limits, headroom)
- Any issues detected with recommendations
```

#### Prompt 2: Deployment Troubleshooting

```
Debug why this pod is not reaching Ready state:
- Pod: <pod-name>
- Deployment: <deployment-name>
- Namespace: default

Provide:
1. Current pod status (phase, conditions)
2. Recent events (why pod is pending/not ready)
3. Readiness probe output (if available)
4. Liveliness probe output (if available)
5. Suggestions to fix (check image loaded, secrets mounted, ports available)
```

### Kagent Capabilities (T010)

Kagent will assist with:
- ✅ Cluster health checks (pod status, service connectivity)
- ✅ Resource usage analysis (CPU, memory utilization)
- ✅ Pod debugging (logs, events, probe failures)
- ✅ Performance recommendations (scaling, resource allocation)
- ✅ Security validation (non-root containers, secrets mounted)

---

## kubectl-ai Patterns

### Helm Chart Generation

Example prompts:
- "Generate a Helm Chart.yaml for a FastAPI backend service named todo-backend"
- "Create values.yaml with configurable replicaCount, image, service type, and resource limits"
- "Generate deployment.yaml template with readiness/liveness probes, env var mounting, port 8000"

### Kubernetes Manifest Generation

Example prompts:
- "Create a Kubernetes Deployment for Next.js frontend with non-root user, resource limits, and health checks"
- "Generate a Kubernetes Secret template for sensitive environment variables"
- "Create a NodePort service for frontend (port 80, nodePort 30000)"

---

## Kagent Patterns

### Cluster Analysis

Example prompts:
- "Analyze this Minikube cluster for health: pod status, service connectivity, resource usage"
- "Check if all pods have passed readiness probes and are receiving traffic"
- "Recommend optimization: memory/CPU allocation, pod distribution, restart policies"

### Debugging & Troubleshooting

Example prompts:
- "Why is this pod stuck in Pending state? Check events and recommendations"
- "Analyze pod logs and suggest root cause for CrashLoopBackOff"
- "Validate network connectivity between frontend and backend pods"

---

## Traceability

All AI-assisted artifacts will be traced via:
1. Commit messages mentioning tool used (kubectl-ai, Kagent)
2. Sanitized prompts documented in specs/infra/PROMPTS.md
3. Generated artifacts linked to their specifications
4. Validation results recorded for audit trail

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Docker Patterns: `/specs/infra/docker-gordon.md`
- Minikube Deployment: `/specs/infra/minikube-deployment.md`
