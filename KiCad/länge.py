#Programm um eine kicad_sch-Datei zu lesen und die Anzahl an Zeichen zu zählen
import sys
from urllib.request import urlopen
import os

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

if len(sys.argv) < 3:
    print("Benutzung: python zaehler.py <datei> <github_repository_url>")
    sys.exit(1)


alterd_datei = sys.argv[1]
github_repository = sys.argv[2]
original_datei = download_datei(sys.argv[2], sys.argv[1])

with open(original_datei, "r", encoding="utf-8") as datei:
    original_inhalt = datei.read()

with open(alterd_datei, "r", encoding="utf-8") as datei:
    alterd_inhalt = datei.read()

alterd_anzahl = len(alterd_inhalt)
original_anzahl = len(original_inhalt)


print(f"Die originale Datei hat {original_anzahl} Zeichen.\nDie veränderte Datei hat {alterd_anzahl} Zeichen.")

os.remove(original_datei)