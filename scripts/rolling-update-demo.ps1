$ErrorActionPreference = 'Stop'
function Show-Health {
  for ($attempt = 0; $attempt -lt 10; $attempt++) {
    curl.exe -fsS http://127.0.0.1:30500/health
    if ($LASTEXITCODE -eq 0) { return }
    Start-Sleep -Seconds 1
  }
  throw 'RoomFit health check did not succeed'
}
if (-not (kind get clusters | Select-String '^roomfit$')) {
  kind create cluster --name roomfit --config scripts/kind-config.yaml
}
docker build -t roomfit-api:v1 --build-arg APP_VERSION=v1 .
docker build -t roomfit-api:v2 --build-arg APP_VERSION=v2 .
kind load docker-image roomfit-api:v1 --name roomfit
kind load docker-image roomfit-api:v2 --name roomfit
kubectl apply -f k8s
kubectl rollout status deployment/roomfit -n roomfit
Show-Health
kubectl set image deployment/roomfit api=roomfit-api:v2 -n roomfit
kubectl rollout status deployment/roomfit -n roomfit
Show-Health
kubectl rollout history deployment/roomfit -n roomfit
kubectl rollout undo deployment/roomfit -n roomfit
kubectl rollout status deployment/roomfit -n roomfit
Show-Health
