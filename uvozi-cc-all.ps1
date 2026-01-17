# uvozi-cc-all.ps1
# Uvoz CC CSV → MASTER VUS.db (Documents\VUS\VUS.db) - ALL mode
# PS 5.1 compatible (brez ArgumentList)

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

$python = (Get-Command python -ErrorAction Stop).Source

Write-Host ""
Write-Host "Kličem:" -ForegroundColor Cyan
Write-Host "$python .\uvozi_cc_delta_v_sqlite.py `"$CsvPath`" `"$DbPath`" --all --verbose" -ForegroundColor Cyan
Write-Host ""

$logPath = Join-Path $PSScriptRoot "uvoz-all.log"

# ProcessStartInfo (PS 5.1): uporablja .Arguments (string)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.Arguments = ".\uvozi_cc_delta_v_sqlite.py `"$CsvPath`" `"$DbPath`" --all --verbose"
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError  = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$p = New-Object System.Diagnostics.Process
$p.StartInfo = $psi
[void]$p.Start()

$sw = [System.IO.StreamWriter]::new($logPath, $false, [System.Text.Encoding]::UTF8)

try {
    while (-not $p.HasExited) {
        while (-not $p.StandardOutput.EndOfStream) {
            $line = $p.StandardOutput.ReadLine()
            if ($null -ne $line) { Write-Host $line; $sw.WriteLine($line) }
        }
        while (-not $p.StandardError.EndOfStream) {
            $eline = $p.StandardError.ReadLine()
            if ($null -ne $eline) { Write-Host $eline -ForegroundColor Red; $sw.WriteLine($eline) }
        }
        Start-Sleep -Milliseconds 200
    }

    while (-not $p.StandardOutput.EndOfStream) {
        $line = $p.StandardOutput.ReadLine()
        if ($null -ne $line) { Write-Host $line; $sw.WriteLine($line) }
    }
    while (-not $p.StandardError.EndOfStream) {
        $eline = $p.StandardError.ReadLine()
        if ($null -ne $eline) { Write-Host $eline -ForegroundColor Red; $sw.WriteLine($eline) }
    }
}
finally {
    $sw.Flush()
    $sw.Close()
}

if ($p.ExitCode -ne 0) {
    throw "Uvoz ni uspel (exit $($p.ExitCode)). Poglej log: $logPath"
}

Write-Host ""
Write-Host "✓ Uvoz (ALL) zaključen. Log: $logPath" -ForegroundColor Green

if ($Pause) { Read-Host "Končano. Pritisni Enter za izhod..." }
