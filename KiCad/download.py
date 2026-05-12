from urllib.request import urlopen
import sys

#Diese Datei lädt eine Roh-Datei direkt von Github herunter und speichert sie lokal ab
def download_datei(url, dateiname):
    original_datei = dateiname.replace(".kicad_sch", "_original.kicad_sch")
    try:
        with urlopen(url) as antwort:
            inhalt = antwort.read().decode("utf-8")

        with open(original_datei, "w", encoding="utf-8") as datei:
            datei.write(inhalt)
        
        return original_datei
    except Exception as e:
        print(f"Fehler beim Herunterladen der Datei: {e}")

alterd_datei = sys.argv[1]
github_repository = sys.argv[2]
original_datei = download_datei(sys.argv[2], sys.argv[1])
