# ==============================================
# 🔧 Script d'automatisation Git (PowerShell)
# Auteur : Jooo
# Repo   : https://github.com/Tahlasandale/preprodhub
# Branche : main
# ==============================================

param(
    [Parameter(Mandatory = $true)]
    [string]$Message
)

$RemoteUrl = "https://github.com/Tahlasandale/preprodhub"
$Branch = "main"
$UserName = "Jooo"
$UserEmail = "mixjojo2006@gmail.com"

# Configuration Git
git config user.name "$UserName"
git config user.email "$UserEmail"

# Verification du remote
Write-Host "🔍 Verification du remote..."
$remote = git remote -v | Select-String $RemoteUrl
if (-not $remote) {
    Write-Host "🔄 Remote incorrect, mise a jour..."
    git remote set-url origin $RemoteUrl
}

# Affichage du remote
git remote -v

# Pull avec rebase
Write-Host "⬇️  Pull (rebase) depuis $Branch..."
git pull --rebase origin $Branch

# Ajout, commit et push
Write-Host "📦 Ajout et commit..."
git add -A
git commit -m "$Message"

Write-Host "🚀 Push vers $Branch..."
git push -u origin $Branch

Write-Host "✅ Commit et push termines avec succes !"
