# Screenshot checklist

Capture the following live evidence.

1. A green GitHub Actions workflow run at the repository Actions page.
2. `kubectl get pods -n roomfit` after `scripts/rolling-update-demo.ps1`.
3. `kubectl rollout history deployment/roomfit -n roomfit`.
4. `kubectl rollout undo deployment/roomfit -n roomfit` output.
5. Grafana dashboard at `http://localhost:3000` showing uptime, latency, and error rate.
6. Prometheus targets at `http://localhost:9090/targets`.
7. Successful `ansible-playbook playbook.yml --ask-become-pass` output in WSL.
