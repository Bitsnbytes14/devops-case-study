# Monitoring and logging

Docker Compose runs the API, Prometheus, and Grafana. Prometheus scrapes `/metrics`; Grafana uses the provisioned Prometheus datasource and RoomFit Service dashboard. The dashboard covers availability, uptime, error rate, request rate, latency, and allocation metrics.

The real chaos run used `FAULT_RATE=0.2`, produced 155 successful requests and 45 failures, measured a 22.28 percent error rate, and placed the error alert in pending state. Recovery returned `FAULT_RATE` to zero. See [monitoring evidence](evidence/monitoring_03_chaos.txt), [normal dashboard](screenshots/grafana_dashboard_normal.png), and [chaos dashboard](screenshots/grafana_dashboard_chaos.png).

Gunicorn writes access logs to standard output. Use `docker compose logs api` locally or `kubectl logs` in Kubernetes. The Ansible host includes a logrotate policy.
