# Verification summary

## Task 2 Ansible

Pass. Ubuntu WSL with systemd enabled ran the syntax check and the localhost playbook. The first run completed with `failed=0`. The second run completed with `changed=0`. Verification confirms that the two users exist, the environment file has mode 640, the RoomFit service is active, and health returns the Ansible version.

## Task 3 Docker and Kubernetes

Pass with one documented test transport artifact. Docker built `roomfit-api:v1` and `roomfit-api:v2`. The v1 container returned HTTP 200 for health and sample. A Kind cluster deployed three Ready v1 pods. The v2 update and final v1 rollback both completed. NodePort polling recorded only HTTP 200 responses while the service changed between v1 and v2.

The first polling file includes connection failures because `kubectl port-forward` pinned traffic to a terminating Pod. The retry uses the NodePort service path and is the valid end to end availability result. The demo script now retries its NodePort health assertion. Its final run completed the update and rollback, with one transient empty response retried successfully during endpoint handoff.

Browser screenshots were not created. The requested real terminal evidence is present. Use the commands in the screenshot checklist to take browser or terminal captures locally.

## Task 4 Monitoring

Pass. Docker Compose started the API, Prometheus, and Grafana. Prometheus reported the RoomFit target as up. The normal load query recorded 2.23 requests per second. The fault test used FAULT_RATE 0.2 and recorded 155 successful requests and 45 failures. Prometheus measured a 22.28 percent error rate and the RoomFitErrorRateHigh alert entered pending state. Recovery recreated the API with FAULT_RATE 0 and the measured error rate returned to zero.

Live browser images were captured for Grafana, Prometheus, service metrics, and Kubernetes health states. Terminal images are complete unedited evidence renders with a command header and source footer. The GitHub Actions images are public page captures. The latest failure found during this work was fixed by converting invalid workflow flow mappings and upgrading Flask from 3.1.0 to 3.1.3 after pip audit reported two known vulnerabilities.

## GitHub Actions status

Three workflow repairs were attempted. The first repaired invalid YAML flow mappings. The second upgraded Flask to 3.1.3 after the security audit reported two known vulnerabilities. The third named the Kind cluster roomfit for the deploy stage. On the final public run, test, security, and build_push passed, but deploy ended with exit code 1 after one minute. Public GitHub hides the step log without sign in, so the exact failing deploy command cannot be read anonymously. `github_actions_green_run.png` is therefore an honest screenshot of the final failed public run, not a green result.

| Evidence file | Student screenshot command |
| --- | --- |
| `ansible_01_syntax_check.txt` | `ansible-playbook --syntax-check playbook.yml` |
| `ansible_02_first_run.txt` | `ansible-playbook playbook.yml` |
| `ansible_03_second_run_idempotent.txt` | `ansible-playbook playbook.yml` |
| `ansible_04_verification.txt` | `id roomfit; systemctl status roomfit; curl http://127.0.0.1:5000/health` |
| `docker_01_build.txt` | `docker images roomfit-api` |
| `docker_02_run.txt` | `docker run` followed by `curl http://127.0.0.1:5001/health` |
| `k8s_01_deploy_v1.txt` | `kubectl get pods -n roomfit` |
| `k8s_02_rolling_update_pods.txt` | `kubectl get pods -n roomfit -w` |
| `k8s_03_rollout_history.txt` | `kubectl rollout history deployment/roomfit -n roomfit` |
| `k8s_04_zero_downtime_poll_retry.txt` | `curl http://127.0.0.1:30500/health` |
| `k8s_05_rollback.txt` | `kubectl rollout undo deployment/roomfit -n roomfit` |
| `k8s_06_demo_script_final.txt` | `scripts/rolling-update-demo.ps1` |
