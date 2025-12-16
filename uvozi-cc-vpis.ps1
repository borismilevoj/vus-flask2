# uvozi-cc-vpis.ps1
# Uvoz CC CSV → MASTER VUS.db, samo Citation vsebuje "vpis"

[CmdletBinding()]
param(
    # CSV export iz Crossword Compilerja (Desktop je pri tebi v OneDrive)
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

$python = "python"

# argumenti za python importer (VPIS-only)
$arguments = @(
    ".\uvozi_cc_delta_v_sqlite.py",
    $CsvPath,
    $DbPath,
    "--only-citation-contains",
    "vpis"
)

# če je bil podan -Verbose, dodaj python --verbose
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
Write-Host "✓ Uvoz (VPIS-only) v MASTER VUS.db uspešno zaključen." -ForegroundColor Green
Read-Host "Končano. Pritisni Enter za izhod..."
