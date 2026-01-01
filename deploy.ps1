# deploy.ps1

Write-Host "Setting up Minikube Docker Environment..." -ForegroundColor Cyan
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set up Minikube Docker environment. Is Minikube running?"
    exit 1
}

Write-Host "Building Docker Image (flask-task-master:latest)..." -ForegroundColor Cyan
docker build -t flask-task-master:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed."
    exit 1
}

Write-Host "Applying Kubernetes Manifests..." -ForegroundColor Cyan
kubectl apply -f k8s/

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to apply Kubernetes manifests."
    exit 1
}

Write-Host "Waiting for pods to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
kubectl get pods

Write-Host "Opening Service..." -ForegroundColor Green
minikube service flask-service
