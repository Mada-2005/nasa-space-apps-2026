# Run a second Claude account on the same laptop.
# Runs a SECOND Claude Code login on the same laptop, in its own git worktree.
#
# CLAUDE_CONFIG_DIR points Claude Code at a separate settings/login folder, so this
# session logs in with account 2 while your normal terminal stays on account 1.
# The git worktree is a second checkout of the repo on another branch, so the two
# sessions never edit the same files on disk.
#
# Usage (PowerShell, from the repo root):
#   .\scripts\second_account.ps1 lane/b-app
#   First time only: run /login inside the session and sign in with account 2.
# If PowerShell blocks the script:  Set-ExecutionPolicy -Scope Process Bypass

param([string]$Branch = "lane/b-app")

$repoName = Split-Path -Leaf (Get-Location)
$wt = "..\$repoName-" + ($Branch -replace "/", "-")

git show-ref --verify --quiet "refs/heads/$Branch"
if ($LASTEXITCODE -ne 0) { git branch $Branch main }
if (-not (Test-Path $wt)) { git worktree add $wt $Branch }

$env:CLAUDE_CONFIG_DIR = Join-Path $HOME ".claude-account2"
New-Item -ItemType Directory -Force -Path $env:CLAUDE_CONFIG_DIR | Out-Null
Set-Location $wt
Write-Host "Worktree: $wt  (branch $Branch)  config: $env:CLAUDE_CONFIG_DIR"
claude
