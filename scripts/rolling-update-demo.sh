#!/usr/bin/env bash
set -euo pipefail
kind create cluster --name roomfit --config scripts/kind-config.yaml || true
docker build -t roomfit-allocation-service:v1 --build-arg APP_VERSION=v1 .
docker build -t roomfit-allocation-service:v2 --build-arg APP_VERSION=v2 .
kind load docker-image roomfit-allocation-service:v1 --name roomfit
kind load docker-image roomfit-allocation-service:v2 --name roomfit
kubectl apply -f k8s
kubectl rollout status deployment/roomfit -n roomfit
kubectl get pods -n roomfit
kubectl set image deployment/roomfit api=roomfit-allocation-service:v2 -n roomfit
kubectl rollout status deployment/roomfit -n roomfit
kubectl rollout history deployment/roomfit -n roomfit
kubectl rollout undo deployment/roomfit -n roomfit
kubectl rollout status deployment/roomfit -n roomfit
