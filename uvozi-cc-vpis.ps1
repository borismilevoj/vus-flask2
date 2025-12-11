# uvozi-cc-vpis.ps1
# Uvoz CC CSV → VUS.db, CSV na namizju

[CmdletBinding()]
param(
    # CSV, ki ga exportaš iz Crossword Compilerja na namizje
    [string]$CsvPath = "$env:USERPROFILE\Desktop\cc_clues_DISPLAY_UTF8.csv",

    # SQLite baza, ki jo uporablja tvoj VUS admin
    [string]$DbPath  = ".\data\VUS.db"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host ">>> uvozi-cc-vpis.ps1 SE JE ZAGNAL" -ForegroundColor Yellow
Write-Host "CSV: $CsvPath"
Write-Host "DB:  $DbPath"

if (-not (Test-Path -LiteralPath $CsvPath)) {
    throw "CSV ne obstaja: $CsvPath"
}

if (-not (Test-Path -LiteralPath $DbPath)) {
    Write-Warning "Baza ne obstaja – Python skripta jo bo po potrebi ustvarila: $DbPath"
}

# izberi ime Python exe-ja
$python = "python"   # če ti ne dela, poskusi "py"

# sestavi argumente za uvozi_cc_delta_v_sqlite.py
$arguments = @(
    ".\uvozi_cc_delta_v_sqlite.py"  # Python skripta
    $CsvPath                        # pot do CSV (namizje)
    $DbPath                         # pot do baze
    "--all"                         # uvozi VSE vrstice, ignorira Citation filter
)

# če je bil PowerShellu podan -Verbose, dodamo še Python --verbose
if ($PSBoundParameters.ContainsKey('Verbose')) {
    $arguments += "--verbose"
}

Write-Host ""
Write-Host "Kličem:"
Write-Host "$python $($arguments -join ' ')" -ForegroundColor Cyan
Write-Host ""

& $python @arguments
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    throw "Uvoz ni uspel, Python je vrnil kodo $exitCode."
} else {
    Write-Host ""
    Write-Host "✓ Uvoz iz CC v VUS.db uspešno zaključen." -ForegroundColor Green
}

Read-Host "Končano. Pritisni Enter za izhod..."
