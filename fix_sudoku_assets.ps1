# fix_sudoku_assets.ps1
# Zaženi iz roota projekta (kjer je mapa "static")

$ErrorActionPreference = "Stop"

$root = Get-Location
$static = Join-Path $root "static"

if (-not (Test-Path $static)) {
  throw "Ne najdem mape 'static' v: $root. Zaženi skripto iz roota projekta."
}

# Najdi "CrosswordCompilerApp" vir (iz mape, kjer Sudoku že dela)
function Find-LibsSource {
  param([string]$StaticPath)

  $candidates = @(
    (Join-Path $StaticPath "Sudoku_very_easy"),
    (Join-Path $StaticPath "Sudoku_hard"),
    (Join-Path $StaticPath "Sudoku_medium"),
    (Join-Path $StaticPath "Sudoku_easy")
  )

  foreach ($base in $candidates) {
    if (Test-Path $base) {
      $libs = Get-ChildItem -Path $base -Directory -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq "CrosswordCompilerApp" } |
        Select-Object -First 1
      if ($libs) { return $libs.FullName }
    }
  }
  return $null
}


$libsSource = Find-LibsSource -StaticPath $static
if (-not $libsSource) {
  throw "Ne najdem nobene mape 'CrosswordCompilerApp' pod static/Sudoku_*. Najprej naj ena težavnost deluje in ima to mapo."
}

Write-Host "LIBS source:" $libsSource

# Iteriraj čez vse Sudoku_* mape in njihove YYYY-MM podmape
$sudokuBases = Get-ChildItem -Path $static -Directory | Where-Object { $_.Name -like "Sudoku_*" }

$copiedLibs = 0
$aliasedJs  = 0

foreach ($base in $sudokuBases) {
  # pričakujemo podmape tipa 2026-01, 2025-12 ...
  $monthDirs = Get-ChildItem -Path $base.FullName -Directory -ErrorAction SilentlyContinue |
               Where-Object { $_.Name -match '^\d{4}-\d{2}$' }

  foreach ($m in $monthDirs) {

    # 1) Ensure CrosswordCompilerApp exists
    $destLibs = Join-Path $m.FullName "CrosswordCompilerApp"
    if (-not (Test-Path $destLibs)) {
      Copy-Item -Recurse -Force $libsSource $destLibs
      $copiedLibs++
      Write-Host "✅ Copied libs -> $destLibs"
    }

    # 2) Fix HTML -> date.js alias problem (največkrat easy)
    $htmls = Get-ChildItem -Path $m.FullName -Filter "*.html" -File -ErrorAction SilentlyContinue
    foreach ($h in $htmls) {
      $content = Get-Content $h.FullName -Raw

      # poišči datum v imenu (YYYY-MM-DD)
      $dateMatch = [regex]::Match($h.Name, '\d{4}-\d{2}-\d{2}')
      if (-not $dateMatch.Success) { continue }
      $date = $dateMatch.Value

      # pričakovani "pravi" JS filename: Sudoku_easy_YYYY-MM-DD.js (ali medium/hard/very_easy)
      # to sestavimo iz imena težavnosti mape (Sudoku_easy, Sudoku_medium ...)
      $expectedJs = "{0}_{1}.js" -f $base.Name, $date
      $expectedJsPath = Join-Path $m.FullName $expectedJs

      # HTML včasih kliče samo YYYY-MM-DD.js (brez prefiksa)
      $dateJs = "$date.js"
      $dateJsPath = Join-Path $m.FullName $dateJs

      # Če HTML referencira date.js, date.js pa ne obstaja, expected pa obstaja -> naredi alias kopijo
      if ($content -match [regex]::Escape($dateJs)) {
        if (-not (Test-Path $dateJsPath) -and (Test-Path $expectedJsPath)) {
          Copy-Item -Force $expectedJsPath $dateJsPath
          $aliasedJs++
          Write-Host "✅ Aliased JS -> $dateJsPath  (from $expectedJs)"
        }
      }

      # Bonus: če expected JS manjka, ampak date.js obstaja, lahko naredimo obratno (da bo konsistentno)
      if (-not (Test-Path $expectedJsPath) -and (Test-Path $dateJsPath)) {
        Copy-Item -Force $dateJsPath $expectedJsPath
        $aliasedJs++
        Write-Host "✅ Backfilled expected JS -> $expectedJsPath (from $dateJs)"
      }
    }
  }
}

Write-Host ""
Write-Host "DONE."
Write-Host "Lib folders copied:" $copiedLibs
Write-Host "JS aliases created:" $aliasedJs
