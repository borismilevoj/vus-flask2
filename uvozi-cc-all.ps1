# uvozi-cc-vpis.ps1
# Uvoz CC CSV → MASTER VUS.db (Documents\VUS\VUS.db)

[CmdletBinding()]
param(
    # CSV export iz Crossword Compilerja (tvoj Desktop je v OneDrive)
    [string]$CsvPath = "$([Environment]::GetFolderPath('Desktop'))\cc_clues_DISPLAY_UTF8.csv",

    # MASTER baza
    [string]$DbPath  = "$env:USERPROFILE\Documents\VUS\VUS.db"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host ">>> uvozi-cc-vpis.ps1 SE JE ZAGNAL" -ForegroundColor Yellow
Write-Host "CSV: $CsvPath"
Write-Host "DB:  $DbPath"

if (-not (Test-Path -LiteralPath $CsvPath)) {
    throw "CSV ne obstaja: $CsvPath"
}

# poskrbi, da obstaja mapa za bazo
$dir = Split-Path -Parent $DbPath
if ($dir -and -not (Test-Path -LiteralPath $dir)) {
    New-Item -ItemType Directory -Path $dir | Out-Null
    Write-Host "✓ Ustvarjena mapa za DB: $dir"
}

# izberi python
$python = "python"  # če kdaj ne dela, poskusi "py"

# argumenti za python importer
$arguments = @(
    ".\uvozi_cc_delta_v_sqlite.py"
    $CsvPath
    $DbPath
    "--all"          # ALL mode (brez Citation filtra)
)

# če je bil podan -Verbose, dodaj še python --verbose
if ($PSBoundParameters.ContainsKey('Verbose')) {
    $arguments += "--verbose"
}

Write-Host ""
Write-Host "Kličem:" -ForegroundColor Cyan
Write-Host "$python $($arguments -join ' ')" -ForegroundColor Cyan
Write-Host ""

& $python @arguments
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    throw "Uvoz ni uspel, Python je vrnil kodo $exitCode."
}

Write-Host ""
Write-Host "✓ Uvoz v MASTER VUS.db uspešno zaključen." -ForegroundColor Green
Read-Host "Končano. Pritisni Enter za izhod..."
