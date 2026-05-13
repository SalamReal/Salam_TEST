from urllib.request import urlopen
import json

def hole_branch_sha(owner, repo, branch="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    with urlopen(url) as antwort:
        daten = json.load(antwort)
    return daten["commit"]["sha"]


def lade_datei_aus_commit(owner, repo, commit_sha, dateipfad):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit_sha}/{dateipfad}"
    with urlopen(url) as antwort:
        return antwort.read().decode("utf-8")


def lese_datei(dateiname):
    with open(dateiname, "r", encoding="utf-8") as datei:
        return datei.read()


owner = "SalamReal"
repo = "Salam_TEST"
branch = "main"
dateipfad_im_repo = "KiCad/helloworld.py"
lokale_datei = "helloworld.py"

commit_sha = hole_branch_sha(owner, repo, branch)
github_inhalt = lade_datei_aus_commit(owner, repo, commit_sha, dateipfad_im_repo)
local_inhalt = lese_datei(lokale_datei)

print(local_inhalt)
print(github_inhalt)
print(local_inhalt == github_inhalt)
print(f"Verglichen mit Commit: {commit_sha}")