# Screenshot checklist

Capture real terminal or browser evidence after opening Docker Desktop.

1. Run `wsl -d Ubuntu -u root -- bash -lc "cd /mnt/d/devopscasestudy/devops-case-study/ansible && ansible-playbook -i inventory.ini playbook.yml"` twice. Capture the second recap showing `changed=0`.
2. Run `wsl -d Ubuntu -u root -- bash -lc "systemctl status roomfit; curl http://127.0.0.1:5000/health"`. Capture the active service and health response.
3. Run `docker images roomfit-api`, then `docker run` with port 5001. Capture the health and sample responses.
4. Run `kubectl get pods -n roomfit` and capture the three Ready replicas.
5. Run `scripts/rolling-update-demo.ps1` and capture the v1, v2, and final v1 health responses.
6. Run `kubectl rollout history deployment/roomfit -n roomfit` and `kubectl rollout undo deployment/roomfit -n roomfit`.
7. Open `http://127.0.0.1:30500/health` during v1, v2, and final v1. Open `http://127.0.0.1:30500/metrics` for the metrics page.
8. Capture a green GitHub Actions run from the repository Actions page.
