# Architecture

RoomFit allocation service is a single purpose Python API. Students call the Flask endpoints, which apply hard compatibility constraints and deterministic allocation logic. Prometheus scrapes application metrics and Grafana displays service health and allocation signals. Kubernetes runs three replicas behind a Service. Ansible supports a systemd deployment on WSL Ubuntu.

![RoomFit architecture](diagrams/architecture.png)
