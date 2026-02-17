# Quick Start Script for ScholarMatch
# Run with: .\start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting ScholarMatch Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import django" 2>&1 | Out-Null
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating..." -ForegroundColor Yellow
    @"
SECRET_KEY=django-insecure-change-this-in-production-12345
DEBUG=True
DB_NAME=scholarmatch_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "✅ .env file created" -ForegroundColor Green
}

# Check if static files exist
if (-not (Test-Path "static\assets")) {
    Write-Host "⚠️  Static files not found. Copying..." -ForegroundColor Yellow
    if (-not (Test-Path "static")) {
        New-Item -ItemType Directory -Path "static" | Out-Null
    }
    if (Test-Path "scholarmatch\assets") {
        Copy-Item -Path "scholarmatch\assets" -Destination "static\assets" -Recurse -Force
    }
    if (Test-Path "scholarmatch\images") {
        Copy-Item -Path "scholarmatch\images" -Destination "static\images" -Recurse -Force
    }
    Write-Host "✅ Static files copied" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Django Development Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Yellow
Write-Host "  Web: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  Admin: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start Django server
python manage.py runserver

