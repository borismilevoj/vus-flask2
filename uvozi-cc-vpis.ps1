$code = @'
# uvozi-cc-delta.ps1 — izvozi SAMO nove/spremenjene vrstice
[CmdletBinding()]
param(
    [string]$CsvPath      = ".\out\cc_clues_ANSI.csv",
    [string]$OutDeltaPath = ".\out\cc_delta.csv",
    [string]$StatePath    = ".\out\cc_sync_state.json",
    [string]$KeyColumn    = "Word",
    [string]$Keyword      = "",
    [char]  $Delimiter    = ',',   # privzeto vejica (tvoj CSV)
    [string[]]$HashColumns = @("Word","Clue"),  # primerjaj le te stolpce
    [switch]$CopyToVarData
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RowHash([string]$text) {
    $sha1 = [System.Security.Cryptography.SHA1]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
    ($sha1.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ''
}

Write-Host "CSV: $CsvPath"
Write-Host "State: $StatePath"
Write-Host "Out: $OutDeltaPath"
Write-Host "Delimiter: '$Delimiter'"
Write-Host "KeyColumn: $KeyColumn"
Write-Host "HashColumns: $($HashColumns -join ', ')"
if ($Keyword) { Write-Host "Keyword filter: '$Keyword'" }

if (-not (Test-Path -LiteralPath $CsvPath)) { throw "CSV ne obstaja: $CsvPath" }

# Uvoz CSV (najprej CP1250, nato UTF-8)
try {
    $rows = Import-Csv -Path $CsvPath -Delimiter $Delimiter -Encoding Default
} catch {
    Write-Warning "Default/CP1250 ni uspel -> UTF8"
    $rows = Import-Csv -Path $CsvPath -Delimiter $Delimiter -Encoding UTF8
}
if (-not $rows -or $rows.Count -eq 0) { throw "CSV je prazen ali neberljiv." }

# Kolone
$colNames = $rows[0].PSObject.Properties.Name
if ($colNames -notcontains $KeyColumn) {
    $KeyColumn = $colNames[0]
    Write-Warning "Ključna kolona ni najdena. Uporabljam prvo: '$KeyColumn'."
} else {
    Write-Host "Uporabljam ključno kolono: '$KeyColumn'"
}

# Validiraj HashColumns
$HashColumns = $HashColumns | Where-Object { $colNames -contains $_ }
if (-not $HashColumns -or $HashColumns.Count -eq 0) {
    $HashColumns = $colNames   # fallback: vse kolone
    Write-Warning "Nobena izmed navedenih HashColumns ne obstaja – hešam vse kolone."
}

# Naloži state (mapa key -> hash)
$state = @{}
if (Test-Path -LiteralPath $StatePath) {
    try {
        $json = Get-Content -Raw -LiteralPath $StatePath | ConvertFrom-Json
        if ($json) { foreach ($p in $json.PSObject.Properties) { $state[$p.Name] = [string]$p.Value } }
    } catch { Write-Warning "State JSON je poškodovan – začnem na novo." }
}

# Izračun delte
$delta = New-Object System.Collections.Generic.List[object]
$cntAll = 0; $cntDelta = 0

foreach ($r in $rows) {
    $cntAll++

    if ($Keyword) {
        $hit = $false
        foreach ($n in $colNames) {
            $v = [string]$r.$n
            if ($v -match [Regex]::Escape($Keyword)) { $hit = $true; break }
        }
        if (-not $hit) { continue }
    }

    $key = ([string]$r.$KeyColumn).Trim()

    # heš samo izbranih stolpcev (npr. Word|Clue)
    $concat = ($HashColumns | ForEach-Object { [string]$r.$_ }) -join '|'
    $hash = Get-RowHash $concat

    if (-not $state.ContainsKey($key)) {
        $delta.Add($r) | Out-Null
        $state[$key] = $hash
        $cntDelta++
    } elseif ($state[$key] -ne $hash) {
        $delta.Add($r) | Out-Null
        $state[$key] = $hash
        $cntDelta++
    }

    if ($cntAll % 5000 -eq 0) { Write-Host ("… obdelanih: {0} | novosti/sprememb: {1}" -f $cntAll, $cntDelta) }
}

Write-Host "Skupaj prebranih: $cntAll"
Write-Host "Novih/spremenjenih: $cntDelta"

# Zapiši delta
$dir = Split-Path -Parent $OutDeltaPath
if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }

if ($cntDelta -gt 0) {
    $delta | Export-Csv -Path $OutDeltaPath -Delimiter $Delimiter -NoTypeInformation -Encoding UTF8
    Write-Host "✓ Zapisano: $OutDeltaPath"
    if ($CopyToVarData) {
        $var = ".\var\data"
        if (-not (Test-Path -LiteralPath $var)) { New-Item -ItemType Directory -Path $var | Out-Null }
        $dest = Join-Path $var (Split-Path -Leaf $OutDeltaPath)
        Copy-Item -LiteralPath $OutDeltaPath -Destination $dest -Force
        Write-Host "✓ Kopirano v $dest"
    }
} else {
    Write-Host "Ni novosti – delta CSV ni ustvarjen."
}

# Shrani state
$state | ConvertTo-Json | Set-Content -LiteralPath $StatePath -Encoding UTF8
Write-Host "✓ State posodobljen: $StatePath"
'@

$path = ".\uvozi-cc-delta.ps1"
$code | Set-Content -Path $path -Encoding UTF8
