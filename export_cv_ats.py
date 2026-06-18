"""
export_cv_ats.py
Regenere tous les CV PDF depuis leurs fichiers HTML sources
via Chrome headless (texte ATS-extractible garanti).

Workflow :
  1. Modifie le HTML du CV
  2. Lance : python export_cv_ats.py
  3. Le PDF correspondant est mis a jour

Usage :
  python export_cv_ats.py          # tous les CV
  python export_cv_ats.py alternance  # filtre sur le nom de fichier
"""
import subprocess, sys, time, os
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE   = Path(__file__).parent
TMP    = Path(os.environ["TEMP"]) / "chrome_pdf_tmp"
TMP.mkdir(exist_ok=True)

# Correspondance HTML -> PDF
CV_MAP = {
    "cv_pierre_guerlais.html":        "cv_pierre_guerlais.pdf",
    "cv_pierre_guerlais_DA_DE.html":  "cv_pierre_guerlais_DA_DE.pdf",
    "cv_alternance_data_engineer.html": "cv_alternance_data_engineer.pdf",
    "cv_manager_crc.html":            "cv_pierre_guerlais_manager.pdf",
}

def export(html_path: Path, pdf_path: Path) -> bool:
    print(f"\n  {html_path.name}  ->  {pdf_path.name}")
    subprocess.run([
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        f"--user-data-dir={TMP}",
        html_path.as_uri(),
    ], capture_output=True)
    time.sleep(1.5)
    if pdf_path.exists():
        sz = pdf_path.stat().st_size // 1024
        print(f"  OK  ({sz} Ko)")
        return True
    print("  ERREUR : PDF non cree. Chrome est peut-etre ouvert sur ce profil.")
    return False

# Filtre optionnel via argument
filtre = sys.argv[1].lower() if len(sys.argv) > 1 else ""

print("=== Export CV (texte ATS-extractible) ===")
ok = err = 0
for html_name, pdf_name in CV_MAP.items():
    if filtre and filtre not in html_name:
        continue
    html = HERE / html_name
    pdf  = HERE / pdf_name
    if not html.exists():
        print(f"\n  IGNORE : {html_name} introuvable")
        continue
    if export(html, pdf):
        ok += 1
    else:
        err += 1

print(f"\n{'='*40}")
print(f"Termine : {ok} OK  |  {err} erreur(s)")
if err == 0:
    print("Tous les PDF sont prets pour Indeed et les ATS.")
