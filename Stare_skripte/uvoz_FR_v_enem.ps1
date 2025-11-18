Param(
  [string]$CsvDir = ".",
  [string]$Pattern = "mesta_FR_*.csv",
  [string]$DbPath = ".\VUS.db",
  [switch]$GenericCleanup,
  [string]$GenericPhrase = "mesto v Franciji"
)

$ErrorActionPreference = "Stop"

# 0) Backup
New-Item -ItemType Directory -Force -Path .\backups | Out-Null
$ts = Get-Date -Format yyyyMMdd_HHmmss
Copy-Item $DbPath ".\backups\VUS_backup_import_$ts.db"
Write-Host "✅ Backup: backups\VUS_backup_import_$ts.db"

# 1) Štartno št. zapisov + indeks
$startCount = sqlite3 $DbPath "SELECT COUNT(*) FROM slovar;"
sqlite3 $DbPath "CREATE INDEX IF NOT EXISTS idx_slovar_geslo ON slovar(geslo);"

# 2) Zberi CSV in uvozi
$files = Get-ChildItem -Path $CsvDir -Filter $Pattern | Sort-Object Name
if (-not $files) {
  Write-Host "Ni datotek za uvoz (vzorec: $CsvDir\$Pattern)."
  exit 0
}

foreach ($f in $files) {
  Write-Host ">>> Uvažam $($f.FullName) ..."
  python .\scripts\uvozi_csv_vus.py $f.FullName
}

# 3) (opcijsko) čistimo generike, kjer obstaja boljši opis za isto geslo
if ($GenericCleanup) {
  Write-Host ">>> Čiščenje generikov: '$GenericPhrase' ..."
  python .\scripts\odstrani_generic.py --generic "$GenericPhrase" --apply
}

# 4) Povzetek
$endCount = sqlite3 $DbPath "SELECT COUNT(*) FROM slovar;"
$added = [int]$endCount - [int]$startCount

Write-Host "`n---- Povzetek ----"
Write-Host "Začetno št. zapisov : $startCount"
Write-Host "Končno št. zapisov  : $endCount"
Write-Host "Dodano               : $added"
