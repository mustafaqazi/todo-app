# Helm Charts Design Specification: Phase IV

**Purpose**: Helm chart structure and design patterns for todo-frontend and todo-backend services.

**Status**: To be completed during Phase 3 (User Story 1)

---

## Placeholder: Helm Chart Architecture

This specification will document:
1. Chart structure (Chart.yaml, values.yaml, templates/)
2. Deployment templates with readiness/liveness probes
3. Service configuration (ClusterIP for backend, NodePort for frontend)
4. Resource requests and limits
5. Environment variable mounting via Kubernetes Secrets
6. Helper templates (_helpers.tpl) for label/selector generation

**To be filled in during T014, T086, T116-T121 (User Story 1 & 5 implementation)**

---

## Key Design Decisions

- **Multi-chart approach**: Separate charts for frontend and backend for independent deployment
- **Secret mounting**: All sensitive env vars via `envFrom.secretRef`
- **Health checks**: Readiness probe checks application health; liveness probe restarts failed pods
- **Resource limits**: Prevent OOM and resource contention on Minikube

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Minikube Deployment: `/specs/infra/minikube-deployment.md`
- AI DevOps Tools: `/specs/infra/ai-devops.md`
