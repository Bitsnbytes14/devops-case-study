# Architecture

RoomFit allocation service is a single purpose Python API. Students call the Flask endpoints, which apply hard compatibility constraints and deterministic allocation logic. Prometheus scrapes application metrics and Grafana displays service health and allocation signals. Kubernetes runs three replicas behind a Service. Ansible supports a systemd deployment on WSL Ubuntu.

![RoomFit architecture](diagrams/architecture.png)

The supplied CA II PDF also includes a four-service platform diagram. It is preserved as [reference material](diagrams/ca-ii-reference/page-21-1.png), but it is not the architecture implemented by this standalone Flask service.
