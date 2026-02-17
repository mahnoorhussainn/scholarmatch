# Script to install dependencies in the correct venv
# Run with: .\install-deps.ps1

Write-Host "Installing dependencies..." -ForegroundColor Yellow

# Navigate to project directory
$projectDir = "C:\Users\PC\Downloads\scholarmatch - dbs\scholarmatch - dbs"
Set-Location $projectDir

# Find venv
$venvPath = $null
if (Test-Path "..\venv\Scripts\python.exe") {
    $venvPath = "..\venv"
    Write-Host "✅ Found venv in parent directory" -ForegroundColor Green
} elseif (Test-Path "venv\Scripts\python.exe") {
    $venvPath = "venv"
    Write-Host "✅ Found venv in current directory" -ForegroundColor Green
} else {
    Write-Host "❌ venv not found!" -ForegroundColor Red
    Write-Host "Creating venv..." -ForegroundColor Yellow
    python -m venv venv
    $venvPath = "venv"
}

# Install dependencies using venv's Python
Write-Host "Installing dependencies in venv..." -ForegroundColor Yellow
& "$venvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$venvPath\Scripts\python.exe" -m pip install -r requirements.txt

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
& "$venvPath\Scripts\python.exe" -m pip list | Select-String -Pattern "Django|cors|psycopg|decouple|Pillow"

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To use Django, activate venv:" -ForegroundColor Cyan
if ($venvPath -eq "..\venv") {
    Write-Host "  cd .." -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  cd 'scholarmatch - dbs'" -ForegroundColor White
} else {
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
}
Write-Host ""
Write-Host "Or use venv's Python directly:" -ForegroundColor Cyan
Write-Host "  $venvPath\Scripts\python.exe manage.py runserver" -ForegroundColor White

