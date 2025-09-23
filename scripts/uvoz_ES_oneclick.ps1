param(
  [string]$CsvPath = ".\imports\ES\mesta_ES_all.csv",
  [string]$Generic = "mesto v Španiji",
  [string]$DbPath  = ".\VUS.db"
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "$name ni na PATH (namesti ali dodaj v PATH)."
  }
}

function Sql([string]$q) {
  & sqlite3 $DbPath $q
}

# Preveri orodja in datoteke
Require-Cmd python
Require-Cmd sqlite3
if (-not (Test-Path $DbPath)) { throw "Ne najdem baze: $DbPath" }
if (-not (Test-Path $CsvPath)) { throw "Ne najdem CSV: $CsvPath" }

# 1) Backup
New-Item -ItemType Directory -Force .\backups | Out-Null
$ts = Get-Date -Format yyyyMMdd_HHmmss
$backup = ".\backups\VUS_backup_ES_$ts.db"
Copy-Item $DbPath $backup -Force
Write-Host "Backup narejen: $backup"

# 2) Štetje 'pred'
$beforeTotal   = [int](Sql "SELECT COUNT(*) FROM slovar;")
$beforeGeneric = [int](Sql "SELECT COUNT(*) FROM slovar WHERE lower(trim(opis))=lower('$Generic');")
$beforeCanDel  = [int](Sql @"
WITH g AS (
  SELECT geslo FROM slovar WHERE lower(trim(opis))=lower('$Generic')
)
SELECT COUNT(DISTINCT s.geslo)
FROM slovar s JOIN g ON g.geslo=s.geslo
WHERE lower(trim(s.opis))<>lower('$Generic');
"@)

Write-Host "Pred uvozom – vsega: $beforeTotal, generikov '$Generic': $beforeGeneric (od teh z boljšim opisom: $beforeCanDel)"

# 3) Uvoz CSV
Write-Host "=== UVOZ CSV ==="
$uOut = & python .\scripts\uvozi_csv_vus.py $CsvPath
Write-Host $uOut

# 4) Odstrani generike, kjer obstaja boljši opis
Write-Host "=== ČIŠČENJE GENERIKOV ($Generic) ==="
$preview = & python .\scripts\odstrani_generic.py --generic $Generic
Write-Host $preview
$apply   = & python .\scripts\odstrani_generic.py --generic $Generic --apply
Write-Host $apply

# 5) Štetje 'po'
$afterTotal   = [int](Sql "SELECT COUNT(*) FROM slovar;")
$afterGeneric = [int](Sql "SELECT COUNT(*) FROM slovar WHERE lower(trim(opis))=lower('$Generic');")

Write-Host ""
Write-Host "----- POVZETEK -----"
Write-Host "Backup: $backup"
Write-Host ("Vseh zapisov   : {0} -> {1}  (Δ={2})" -f $beforeTotal,$afterTotal,($afterTotal-$beforeTotal))
Write-Host ("Generikov ('{0}'): {1} -> {2}  (Δ={3})" -f $Generic,$beforeGeneric,$afterGeneric,($afterGeneric-$beforeGeneric))
Write-Host "---------------------"
