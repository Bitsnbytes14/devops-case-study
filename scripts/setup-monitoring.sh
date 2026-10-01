#!/usr/bin/env bash
set -euo pipefail
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace -f monitoring/kube-prometheus-values.yaml
kubectl apply -f monitoring/servicemonitor.yaml -f monitoring/prometheus-rules.yaml -f monitoring/grafana-configmap.yaml
