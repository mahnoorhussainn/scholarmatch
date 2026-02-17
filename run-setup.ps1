# ScholarMatch Setup Script
# Run with: .\run-setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ScholarMatch Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not running!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Stopping any existing containers..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "Building and starting containers..." -ForegroundColor Yellow
docker-compose up --build -d

Write-Host ""
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "Checking container status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create superuser: docker-compose exec web python manage.py createsuperuser" -ForegroundColor White
Write-Host "2. Access application: http://localhost:8000" -ForegroundColor White
Write-Host "3. Access admin: http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "Stop containers: docker-compose down" -ForegroundColor White
Write-Host ""

