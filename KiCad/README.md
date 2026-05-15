## Verwendung des Parameters `-w`

Mit dem Parameter `-w` kann die lokale Version einer `.kicad_sch`-Datei mit der entsprechenden Remote-Version im Git-Repository verglichen werden. Dabei wird die Anzahl der geloeschten und hinzugefuegten Wires ermittelt.

### Voraussetzungen

- Der Parameter `-w` kann nur fuer Dateien vom Typ `.kicad_sch` verwendet werden.
- Die Dateien `cli.py`, `parser.py` und `diff_netcount.py` muessen sich im selben Ordner wie die zu untersuchende lokale Datei befinden.
- Die lokale Datei und die Remote-Datei muessen dieselbe Schaltplandatei repraesentieren.
- Der zweite Parameter muss den Pfad der Datei relativ zum Root des Git-Repositories angeben.
- Das Verzeichnis muss Teil eines Git-Repositories sein.
- Git muss auf dem System installiert und im Terminal verfuegbar sein.

### Aufruf

```bash
python cli.py -w <dateiname> <dateipfad_im_repository>