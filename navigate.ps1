# Script to navigate to correct directory
# Run with: .\navigate.ps1

Write-Host "Finding manage.py..." -ForegroundColor Yellow

# Find manage.py
$managePath = Get-ChildItem -Path "C:\Users\PC\Downloads\scholarmatch - dbs" -Filter "manage.py" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($managePath) {
    $projectDir = Split-Path $managePath.FullName
    Write-Host "✅ Found manage.py at: $($managePath.FullName)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Navigating to project directory..." -ForegroundColor Yellow
    Set-Location $projectDir
    Write-Host "✅ Now in: $(Get-Location)" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run Django commands:" -ForegroundColor Cyan
    Write-Host "  python manage.py runserver" -ForegroundColor White
} else {
    Write-Host "❌ manage.py not found!" -ForegroundColor Red
    Write-Host "Please check the project structure." -ForegroundColor Yellow
}

