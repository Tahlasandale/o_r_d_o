# ==============================================
# Script d'automatisation Git (PowerShell)
# Auteur : Jooo
# Repo   : https://github.com/Tahlasandale/o_r_d_o
# Branche : main
# ==============================================

param(
    [Parameter(Mandatory = $true)]
    [string]$Message
)

# Configuration
$RemoteUrl = "https://github.com/Tahlasandale/o_r_d_o.git"
$Branch = "main"
$UserName = "Tahlasandale"
$UserEmail = "mixjojo2006@gmail.com"

# Configuration de l'encodage pour la console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# Configuration Git
try {
    git config --global core.quotepath off
    git config --global i18n.logoutputencoding utf8
    git config --global i18n.commitencoding utf8
    git config user.name $UserName
    git config user.email $UserEmail
} catch {
    Write-Host "Erreur lors de la configuration Git: $_" -ForegroundColor Red
    exit 1
}

# Fonction pour logger les messages
function Write-Log {
    param([string]$message)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $message"
}

# Verification du remote
Write-Log "Verification du remote..."
try {
    $remote = git remote -v 2>&1
    Write-Log "Remote actuel:`n$remote"
    
    if ($LASTEXITCODE -ne 0) {
        throw $remote
    }
    
    # Vérification plus simple de l'URL distante
    $currentUrl = git config --get remote.origin.url
    if ($currentUrl -ne $RemoteUrl) {
        Write-Log "Mise a jour du remote..."
        git remote set-url origin $RemoteUrl
    }
} catch {
    Write-Host "Erreur lors de la verification du remote: $_" -ForegroundColor Red
    exit 1
}

# Vérification des modifications non commitées
$stashApplied = $false
try {
    $status = git status --porcelain 2>&1
    if ($LASTEXITCODE -eq 0 -and $status) {
        Write-Log "Modifications non commitées détectées. Tentative de stash..."
        $stashOutput = git stash push -m "Auto-stash by git_auto_push.ps1" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Erreur lors du stash des modifications: $stashOutput" -ForegroundColor Red
            exit 1
        }
        $stashApplied = $true
    }
} catch {
    Write-Host "Erreur lors de la vérification des modifications: $_" -ForegroundColor Red
    exit 1
}

# Mise a jour du depot
Write-Log "Mise a jour du depot..."
try {
    $pullOutput = git pull --rebase origin $Branch 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erreur lors du pull: $pullOutput" -ForegroundColor Red
        exit 1
    }
    
    # Récupération des modifications stashées si nécessaire
    if ($stashApplied) {
        $stashPopOutput = git stash pop 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Avertissement: Impossible de réappliquer les modifications stashées: $stashPopOutput" -ForegroundColor Yellow
        } else {
            Write-Log "Modifications stashées réappliquées avec succès"
        }
    }
    
    Write-Log "Dernier commit: $(git log -1 --pretty=format:'%h - %s')"
} catch {
    Write-Host "Erreur lors de la mise a jour: $_" -ForegroundColor Red
    exit 1
}

# Ajout des fichiers
Write-Log "Ajout des modifications..."
try {
    $addOutput = git add -A 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw $addOutput
    }
} catch {
    Write-Host "Erreur lors de l'ajout des fichiers: $_" -ForegroundColor Red
    exit 1
}

# Commit des modifications
Write-Log "Creation du commit..."
try {
    $commitOutput = git commit -m $Message 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw $commitOutput
    }
    Write-Log $commitOutput
} catch {
    Write-Host "Erreur lors du commit: $_" -ForegroundColor Red
    exit 1
}

# Push des modifications
Write-Log "Envoi des modifications vers $Branch..."
try {
    $pushOutput = git push -u origin $Branch 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw $pushOutput
    }
    Write-Log "$pushOutput"
} catch {
    Write-Host "Erreur lors du push: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Operation terminee avec succes!" -ForegroundColor Green
