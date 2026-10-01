# Containers and Kubernetes

The [Dockerfile](../Dockerfile) uses Python 3.12 slim, a non root user, cached dependency installation, Gunicorn with one worker and four threads, and a health check. Kubernetes files in [k8s](../k8s) run three replicas with readiness and liveness probes, resource limits, read only root filesystem, dropped capabilities, and rolling update settings of surge one and unavailable zero.

The real Kind result built `roomfit-api:v1` and `roomfit-api:v2`, deployed three Ready replicas, updated from v1 to v2, then rolled back to v1. See [deployment evidence](evidence/k8s_01_deploy_v1.txt), [rollout history](evidence/k8s_03_rollout_history.txt), and [rollback evidence](evidence/k8s_05_rollback.txt).
