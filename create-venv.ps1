# Script to create virtual environment with error handling
# Run with: .\create-venv.ps1

Write-Host "Creating virtual environment..." -ForegroundColor Yellow

# Remove existing venv if exists
if (Test-Path "venv") {
    Write-Host "Removing existing venv folder..." -ForegroundColor Yellow
    Remove-Item -Path "venv" -Recurse -Force -ErrorAction SilentlyContinue
}

# Try different Python commands
$pythonCommands = @("python", "py", "python3")

foreach ($cmd in $pythonCommands) {
    Write-Host "Trying: $cmd -m venv venv" -ForegroundColor Cyan
    try {
        & $cmd -m venv venv 2>&1 | Out-Null
        if (Test-Path "venv") {
            Write-Host "✅ Virtual environment created successfully using: $cmd" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "❌ Failed with: $cmd" -ForegroundColor Red
        continue
    }
}

# Verify venv was created
if (Test-Path "venv") {
    Write-Host ""
    Write-Host "Virtual environment created!" -ForegroundColor Green
    Write-Host "To activate, run:" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try these solutions:" -ForegroundColor Yellow
    Write-Host "1. Run PowerShell as Administrator" -ForegroundColor White
    Write-Host "2. Check folder permissions" -ForegroundColor White
    Write-Host "3. Use: pip install virtualenv && virtualenv venv" -ForegroundColor White
}

