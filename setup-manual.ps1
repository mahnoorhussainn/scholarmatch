# Manual Setup Script (Without Docker)
# Run with: .\setup-manual.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ScholarMatch Manual Setup (No Docker)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed!" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✅ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PostgreSQL not found in PATH" -ForegroundColor Yellow
    Write-Host "Make sure PostgreSQL is installed and running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 1: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Step 3: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "Step 4: Creating .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
} else {
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

Write-Host ""
Write-Host "Step 5: Copying static files..." -ForegroundColor Yellow
if (-not (Test-Path "static")) {
    New-Item -ItemType Directory -Path "static" | Out-Null
}
if (Test-Path "scholarmatch\assets") {
    Copy-Item -Path "scholarmatch\assets" -Destination "static\assets" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Assets copied" -ForegroundColor Green
}
if (Test-Path "scholarmatch\images") {
    Copy-Item -Path "scholarmatch\images" -Destination "static\images" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Images copied" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps (run these manually):" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Make sure PostgreSQL is running" -ForegroundColor White
Write-Host "2. Create database in pgAdmin 4:" -ForegroundColor White
Write-Host "   - Database name: scholarmatch_db" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run migrations:" -ForegroundColor White
Write-Host "   python manage.py makemigrations" -ForegroundColor Gray
Write-Host "   python manage.py migrate" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Create superuser:" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Collect static files:" -ForegroundColor White
Write-Host "   python manage.py collectstatic --noinput" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Start server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "Then access: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""

