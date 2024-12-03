# Virginia DMV Practice Test Development Setup Script
# Run this script in PowerShell with administrator privileges

# Set execution policy for this process
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Function to check if running as administrator
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($user)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check if running as administrator
if (-not (Test-Administrator)) {
    Write-Host "Please run this script as Administrator" -ForegroundColor Red
    exit
}

# Create and activate virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Add firewall rule for port 3022
$ruleName = "Flask Virginia DMV Practice Test"
$ruleExists = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if (-not $ruleExists) {
    Write-Host "Adding firewall rule for port 3022..." -ForegroundColor Yellow
    New-NetFirewallRule -DisplayName $ruleName `
        -Direction Inbound `
        -Action Allow `
        -Protocol TCP `
        -LocalPort 3022 `
        -Program "$pwd\venv\Scripts\python.exe"
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "1. Make sure you're in the virtual environment (should see (venv) in your prompt)"
Write-Host "2. Run: python app.py"
Write-Host "3. Access the application at: http://127.0.0.1:3022"
