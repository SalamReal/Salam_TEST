import subprocess


# Aktualisiert die Referenzen des angegebenen Remotes, damit origin/main den neuesten Stand kennt.
def git_fetch(remote="origin"):
    subprocess.run(["git", "fetch", remote], check=True)


# Liest die Commit-SHA eines Remote-Refs wie origin/main aus.
def hole_remote_sha(remote_ref="origin/main"):
    result = subprocess.run(
        ["git", "rev-parse", remote_ref],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True
    )
    return result.stdout.strip()


# Liest den Inhalt einer Datei direkt aus einem Git-Ref wie origin/main, ohne sie lokal auszuschreiben.
def lade_datei_aus_git(dateipfad_im_repo, remote_ref="origin/main"):
    result = subprocess.run(
        ["git", "show", f"{remote_ref}:{dateipfad_im_repo}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True
    )
    return result.stdout


# Liest den Inhalt der lokalen Datei aus dem Arbeitsverzeichnis.
def lese_lokale_datei(dateiname):
    with open(dateiname, "r", encoding="utf-8") as datei:
        return datei.read()


lokale_datei = "helloworld.py"
dateipfad_im_repo = "KiCad/helloworld.py"
remote_ref = "origin/main"

git_fetch()

commit_sha = hole_remote_sha(remote_ref)
github_inhalt = lade_datei_aus_git(dateipfad_im_repo, remote_ref)
local_inhalt = lese_lokale_datei(lokale_datei)

print(local_inhalt)
print(github_inhalt)
print(local_inhalt == github_inhalt)
print(f"Verglichen mit Commit: {commit_sha}")