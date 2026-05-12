
import sys


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

def finde_wires(node):
    wires = []

    if isinstance(node, list) and len(node) > 0:
        if node[0] == "wire":
            wires.append(node)

        for element in node:
            wires.extend(finde_wires(element))

    return wires

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
                    wires.add((start, ende))

        for element in node:
            wires.update(finde_wire_punkte(element))

    return wires

text = sys.argv[1]
with open(text, "r", encoding="utf-8") as datei:
    inhalt = datei.read()
tokens = tokenize(inhalt)
tree = parse(tokens)
wires = finde_wires(tree)
wire_points = finde_wire_punkte(tree)

print(wire_points)