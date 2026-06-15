"""
export_cv_ats.py
Regenere cv_pierre_guerlais_DA_DE.pdf avec texte ATS-extractible
via Chrome headless. Remplace export_cv_ats.ps1.
Usage : python export_cv_ats.py
"""
import subprocess, sys, time, os
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE   = Path(__file__).parent
HTML   = HERE / "cv_pierre_guerlais_DA_DE.html"
PDF    = HERE / "cv_pierre_guerlais_DA_DE.pdf"
TMP    = Path(os.environ["TEMP"]) / "chrome_pdf_tmp"

TMP.mkdir(exist_ok=True)
file_url = HTML.as_uri()

print(f"Export en cours...")
print(f"Source  : {HTML}")
print(f"Sortie  : {PDF}")

subprocess.run([
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
    f"--print-to-pdf={PDF}",
    "--print-to-pdf-no-header",
    f"--user-data-dir={TMP}",
    file_url,
], capture_output=True)

time.sleep(1.5)

if PDF.exists():
    sz = PDF.stat().st_size // 1024
    print(f"OK  cv_pierre_guerlais_DA_DE.pdf regenere ({sz} Ko)")
    print("    -> texte embarque, lisible par les ATS et Indeed")
else:
    print("ERREUR : PDF non créé. Vérifiez que Chrome est bien fermé.")
    sys.exit(1)
