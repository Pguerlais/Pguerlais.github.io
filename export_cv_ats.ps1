# export_cv_ats.ps1
# Regenere cv_pierre_guerlais_DA_DE.pdf avec du texte ATS-extractible
# via Chrome headless (print-to-pdf avec police CPU, pas GPU-raster)

$chrome  = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$dir     = Split-Path -Parent $MyInvocation.MyCommand.Path
$htmlIn  = Join-Path $dir "cv_pierre_guerlais_DA_DE.html"
$pdfOut  = Join-Path $dir "cv_pierre_guerlais_DA_DE.pdf"
$tmpDir  = Join-Path $env:TEMP "chrome_pdf_tmp"

# Dossier user-data isole pour eviter conflit avec Chrome ouvert
if (-not (Test-Path $tmpDir)) { New-Item -ItemType Directory -Path $tmpDir | Out-Null }

$fileUrl = "file:///" + $htmlIn.Replace("\", "/").TrimStart("/")

Write-Output "Export en cours..."
Write-Output "Source  : $htmlIn"
Write-Output "Sortie  : $pdfOut"

& $chrome `
  --headless=new `
  --disable-gpu `
  --no-sandbox `
  --run-all-compositor-stages-before-draw `
  --virtual-time-budget=5000 `
  --print-to-pdf="$pdfOut" `
  --print-to-pdf-no-header `
  --user-data-dir="$tmpDir" `
  $fileUrl 2>$null

Start-Sleep -Milliseconds 1500

if (Test-Path $pdfOut) {
    $sz = [int]((Get-Item $pdfOut).Length / 1024)
    Write-Output "OK  cv_pierre_guerlais_DA_DE.pdf regenere ($sz Ko)"
    Write-Output "    -> texte embarque, lisible par les ATS et Indeed"
} else {
    Write-Output "ERREUR : le PDF n'a pas ete cree. Verifiez que Chrome est bien ferme."
}
