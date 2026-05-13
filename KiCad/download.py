from urllib.request import urlopen
import os

# Funktion zum Herunterladen einer KiCad-Schaltplan-Datei von einer URL
def download_datei(url, dateiname):
    original_datei = dateiname.replace(".py", "_original.py")
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
github_datei =download_datei(github_url, local_datei)

with open(local_datei, "r", encoding="utf-8") as datei:
    local_inhalt = datei.read()
with open(github_datei, "r", encoding="utf-8") as datei:
    github_inhalt = datei.read()

print(local_inhalt)
print(github_inhalt)

os.remove(github_datei)
