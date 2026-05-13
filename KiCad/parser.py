import subprocess

# Funktion zum Vergleichen der Wire-Punkte zwischen der lokalen Datei und der GitHub-Version. Gibt die Anzahl der gelöschten und hinzugefügten Wires zurück. Ausgabe: (Anzahl gelöschter Wires, Anzahl hinzugefügter Wires)
def return_comparison(local_dateiname, dateipfad_im_repo, remote="origin", branch="main"):
    #Funktion zum Parsen der KiCad-Schaltplan-Datei und Extrahieren der Wire-Punkte. Ausgabe: Set von Wire-Punkten, wobei jeder Punkt als Tupel (Start, Ende) dargestellt wird, und Start/Ende jeweils ein Tupel (x, y) ist.
    def return_setOfWires(code):
        
        def tokenize(text):
            tokens = []
            i = 0

            while i < len(text):
                c = text[i]

                if c.isspace():
                    i += 1

                elif c in "()":
                    tokens.append(c)
                    i += 1

                elif c == '"':
                    i += 1
                    start = i
                    while i < len(text) and text[i] != '"':
                        i += 1
                    tokens.append(text[start:i])
                    i += 1

                else:
                    start = i
                    while i < len(text) and not text[i].isspace() and text[i] not in '()':
                        i += 1
                    tokens.append(text[start:i])

            return tokens

        def parse(tokens):
            def parse_expr(index):
                if index >= len(tokens):
                    raise ValueError("Unerwartetes Dateiende")

                token = tokens[index]

                if token == "(":
                    result = []
                    index += 1

                    while True:
                        if index >= len(tokens):
                            raise ValueError("Fehlende schließende Klammer")
                        if tokens[index] == ")":
                            return result, index + 1

                        element, index = parse_expr(index)
                        result.append(element)

                elif token == ")":
                    raise ValueError("Unerwartete schließende Klammer")

                else:
                    return token, index + 1

            tree, next_index = parse_expr(0)

            if next_index != len(tokens):
                raise ValueError("Zusätzliche Tokens nach dem Ende")

            return tree
        
        def finde_wire_punkte(node):
            wires = set()

            if isinstance(node, list) and len(node) > 0:
                if node[0] == "wire":
                    for element in node:
                        if (
                            isinstance(element, list)
                            and len(element) == 3
                            and element[0] == "pts"
                            and isinstance(element[1], list)
                            and isinstance(element[2], list)
                            and element[1][0] == "xy"
                            and element[2][0] == "xy"
                        ):
                            start = (element[1][1], element[1][2])
                            ende = (element[2][1], element[2][2])
                            wire = tuple(sorted([start, ende]))
                            wires.add(wire)

                for element in node:
                    wires.update(finde_wire_punkte(element))

            return wires

        tokens = tokenize(code)
        tree = parse(tokens)
        wire_points = finde_wire_punkte(tree)

        return wire_points

    # Funktion zum Laden des aktuellen Inhalts einer Datei aus einem Git-Remote-Ref wie origin/main. Gibt den Inhalt der Datei als String zurück.
    def lade_aktuellen_remote_inhalt(dateipfad_im_repo, remote="origin", branch="main"):
        # Aktualisiert zuerst die Remote-Referenzen, damit der neueste Stand abgefragt wird.
        subprocess.run(["git", "fetch", remote], check=True)

        # Baut den vollständigen Ref-Namen wie origin/main zusammen.
        remote_ref = f"{remote}/{branch}"

        # Liest den Dateiinhalt direkt aus dem aktuellen Remote-Ref.
        result = subprocess.run(
            ["git", "show", f"{remote_ref}:{dateipfad_im_repo}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )

        return result.stdout

    #Vergleich der Wire-Mengen. Gibt zurück: (Anzahl an gelöschten Wires, Anzahl an hinzugefügten Wires)
    def vergleiche_wire_mengen(github_menge, lokale_menge):
        geloescht = github_menge - lokale_menge
        hinzugefuegt = lokale_menge - github_menge
        return len(geloescht), len(hinzugefuegt)

    
    with open(local_dateiname, "r", encoding="utf-8") as datei:
        local_code = datei.read()
    github_code = lade_aktuellen_remote_inhalt(dateipfad_im_repo, remote, branch)


    local_wires = return_setOfWires(local_code)

    github_wires = return_setOfWires(github_code)

    vergleich = vergleiche_wire_mengen(github_wires, local_wires)

    return(vergleich)


