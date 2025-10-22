# PowerShell script to setup Dorothy bot for GitHub
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Dorothy Bot GitHub Setup" -ForegroundColor Cyan  
Write-Host "==================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "dosecurity.py")) {
    Write-Host "ERROR: dosecurity.py not found. Please run this script from C:/bot/Dorothy" -ForegroundColor Red
    exit 1
}

# Check if Git is installed
try {
    git --version | Out-Null
    Write-Host "`n✅ Git is installed" -ForegroundColor Green
} catch {
    Write-Host "`n❌ Git is not installed!" -ForegroundColor Red
    Write-Host "   Please install Git from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

# Check if .env file exists and warn user
if (Test-Path ".env") {
    Write-Host "`n⚠️  WARNING: .env file detected" -ForegroundColor Yellow
    Write-Host "   Your tokens will be stored as GitHub Secrets instead." -ForegroundColor Yellow
}

# Initialize Git repository
if (Test-Path ".git") {
    Write-Host "`n✅ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "`n📝 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Check Git configuration
$gitUser = git config user.name
$gitEmail = git config user.email

if (-not $gitUser -or -not $gitEmail) {
    Write-Host "`nPlease enter your Git configuration:" -ForegroundColor Yellow
    
    if (-not $gitUser) {
        $userName = Read-Host "Enter your name (e.g., John Doe)"
        git config user.name "$userName"
    }
    
    if (-not $gitEmail) {
        $userEmail = Read-Host "Enter your email (GitHub email)"
        git config user.email "$userEmail"
    }
    
    Write-Host "✅ Git configured" -ForegroundColor Green
} else {
    Write-Host "`n✅ Git already configured as: $gitUser <$gitEmail>" -ForegroundColor Green
}

# Stage all files
Write-Host "`n📝 Staging files for commit..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files staged" -ForegroundColor Green

# Show what will be committed
Write-Host "`n📋 Files to be committed:" -ForegroundColor Cyan
git status --short

# Commit
$commitMessage = "Initial commit: Dorothy bot with GitHub Actions"
Write-Host "`n📝 Creating commit: $commitMessage" -ForegroundColor Yellow
git commit -m "$commitMessage" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit created successfully" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No changes to commit or already committed" -ForegroundColor Yellow
}

# Instructions for next steps
Write-Host "`n==================================" -ForegroundColor Green
Write-Host "✅ Local Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Create a new PRIVATE repository on GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Yellow

Write-Host "`n2. Add repository secrets in GitHub Settings > Secrets:" -ForegroundColor White
Write-Host "   - DOROTHY_BOT_TOKEN (required)" -ForegroundColor Yellow
Write-Host "   - DOROTHY_OWNER_ID (optional)" -ForegroundColor Yellow  
Write-Host "   - DISCORD_WEBHOOK_URL (optional)" -ForegroundColor Yellow

Write-Host "`n3. Connect and push to GitHub:" -ForegroundColor White
Write-Host "   Replace YOUR_USERNAME with your GitHub username:" -ForegroundColor Gray
Write-Host "   " -NoNewline
Write-Host "git remote add origin https://github.com/YOUR_USERNAME/dorothy-bot.git" -ForegroundColor Cyan
Write-Host "   " -NoNewline
Write-Host "git branch -M main" -ForegroundColor Cyan
Write-Host "   " -NoNewline
Write-Host "git push -u origin main" -ForegroundColor Cyan

Write-Host "`n4. Dorothy bot will start automatically after pushing!" -ForegroundColor Green
Write-Host "   Or manually trigger from Actions tab in GitHub" -ForegroundColor Gray

Write-Host "`n📖 Full guide: GITHUB_SETUP.md" -ForegroundColor Magenta
Write-Host "==================================" -ForegroundColor Cyan

# Ask if user wants to open GitHub in browser
$openGitHub = Read-Host "`nOpen GitHub.com to create repository? (Y/N)"
if ($openGitHub -eq "Y" -or $openGitHub -eq "y") {
    Start-Process "https://github.com/new"
}
