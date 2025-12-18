# uvozi-cc-all.ps1
# Uvoz CC CSV → MASTER VUS.db (Documents\VUS\VUS.db) - ALL mode

[CmdletBinding()]
param(
    [string]$CsvPath = "$([Environment]::GetFolderPath('Desktop'))\cc_clues_DISPLAY_UTF8.csv",
    [string]$DbPath  = "$env:USERPROFILE\Documents\VUS\VUS.db",
    [switch]$Pause
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host ">>> uvozi-cc-all.ps1 SE JE ZAGNAL" -ForegroundColor Yellow
Write-Host "CSV: $CsvPath"
Write-Host "DB:  $DbPath"

if (-not (Test-Path -LiteralPath $CsvPath)) { throw "CSV ne obstaja: $CsvPath" }

$dir = Split-Path -Parent $DbPath
if ($dir -and -not (Test-Path -LiteralPath $dir)) {
    New-Item -ItemType Directory -Path $dir | Out-Null
    Write-Host "✓ Ustvarjena mapa za DB: $dir"
}

# uporabi python iz trenutnega okolja (bolj ziher kot "python")
$python = (Get-Command python -ErrorAction Stop).Source

$arguments = @(
    ".\uvozi_cc_delta_v_sqlite.py",
    $CsvPath,
    $DbPath,
    "--all",
    "--verbose"
)

Write-Host ""
Write-Host "Kličem:" -ForegroundColor Cyan
Write-Host "$python $($arguments -join ' ')" -ForegroundColor Cyan
Write-Host ""

# PowerShell 5.1 safe logging (da dobiš tudi stderr v log)
$logPath = Join-Path $PSScriptRoot "uvoz-all.log"

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.ArgumentList.Add(".\uvozi_cc_delta_v_sqlite.py")
$psi.ArgumentList.Add($CsvPath)
$psi.ArgumentList.Add($DbPath)
$psi.ArgumentList.Add("--all")
$psi.ArgumentList.Add("--verbose")
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError  = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$p = New-Object System.Diagnostics.Process
$p.StartInfo = $psi
[void]$p.Start()

$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()
$p.WaitForExit()

$stdout + $stderr | Set-Content -Encoding UTF8 $logPath
Get-Content $logPath -Tail 80

if ($p.ExitCode -ne 0) {
    throw "Uvoz ni uspel (exit $($p.ExitCode)). Poglej log: $logPath"
}


Write-Host ""
Write-Host "✓ Uvoz (ALL) zaključen. Log: $logPath" -ForegroundColor Green

# sanity-check (ker uvoznik piše v 'slovar')
sqlite3 $DbPath "SELECT 'slovar_total', COUNT(*) FROM slovar;
                 SELECT 'slovar_sortiran_total', COUNT(*) FROM slovar_sortiran;"

if ($Pause) {
    Read-Host "Končano. Pritisni Enter za izhod..."
}
