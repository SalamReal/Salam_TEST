from urllib.request import urlopen

# Funktion zum Herunterladen einer KiCad-Schaltplan-Datei von einer URL
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

local_datei = "helloworld.py"
github_url = "https://raw.githubusercontent.com/SalamReal/Salam_TEST/main/KiCad/helloworld.py"
download_datei(github_url, local_datei)