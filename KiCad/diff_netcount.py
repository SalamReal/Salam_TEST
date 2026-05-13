from git import Repo
from git.exc import InvalidGitRepositoryError
import os


# Holt den Git-Diff der gefundenen .kicad_pcb Datei.
def get_diff():
    """ Entweder Datei muss im selben ordner liegen: """ 
    #script_ordner = os.path.dirname(os.path.abspath(__file__))
    """  Oder relativ zur Skriptausführung: """ 
    script_ordner = os.getcwd()

    try:
        repo = Repo(script_ordner, search_parent_directories=True)
    
    except InvalidGitRepositoryError:
        print()
        e_msg = "Git-Repository wurde in diesem Ordner nicht gefunden. \n"
        e_msg += f"  Skript wurde hier ausgeführt (muss gleich des .git Ordners sein) {str(script_ordner)}"
        raise Exception(e_msg)
        
    pcb_datei = finde_pfad(script_ordner)
    diff_output = repo.git.diff("HEAD","--",pcb_datei)

    return diff_output


# Findet die erste .kicad_pcb Datei im Repo.
def finde_pfad(repo_pfad=".") -> str:
    for root, _, files in os.walk(repo_pfad):
        for file in files:
            if file.endswith(".kicad_pcb"):
                return os.path.relpath(os.path.join(root, file),repo_pfad)

    raise FileNotFoundError("Keine .kicad_pcb Datei gefunden.")


# Bekommt diff text und gibt alle Netlist einträge raus im Format:
# [Nr, change: True/False, content]
def parse_diff(diff_output):
    assert(type(diff_output) == type("string"))
    changed_netlist =[]
    # gehe die diff zeile für zeile durch
    for i in range(len(diff_output.splitlines())):
        # seperiere wie sie verändert wurde, welche zeilennummer sie hat und die zeile selbst
        line = diff_output.splitlines()[i]
        eintrag = line[1:].strip()
        if "(net " in eintrag:
            change = (line[0] == '+')
            line_number = i
            # füge sie zu der netlist hinzu falls sie net beinhaltet
            changed_netlist.append([line_number,change,eintrag])
    return changed_netlist

# Zählt die Netlist veränderungen (Filtert die Veränderten raus (+-) )
# (Netliständerungen, Änderungen(+-) )
def interprete_parsed(parsed_diff):
    max = len(parsed_diff)-1
    netcount = 0
    skipped = 0
    for i in range(max):
        if i != max and i+1 != max:
            a = parsed_diff[i]
            b = parsed_diff[i+1]
            # Wenn a removed wurde und b hinzugefügt wurde und sie direkte nachbarn sind -> Ersetzt
            if a[1] == False and b[1] == True and (a[0]-b[0]) < 2:
                skipped += 1
                continue #skippe zähler
        netcount += 1
    return [netcount, skipped]


def main(should_print=True):
    try:
        l = get_diff()
        p = parse_diff(l)
        i = interprete_parsed(p)
        if should_print:
            print("Netlist Änderungen: ",i[0])
            print("-> davon ersetzte Lines: ",i[1])
        return i[0]
    except Exception as e:
        print(f"\033[91mERROR: {e}\033[0m")