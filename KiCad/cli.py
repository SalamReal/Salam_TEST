import argparse
import os, os.path
import sys
import subprocess

from parser import return_comparison

from diff_netcount import get_diff, parse_diff, interprete_parsed

def main():
    parser = argparse.ArgumentParser(description="A tool to get the diff of KiCad files.")
    parser.add_argument("-w", action="store_true", help="Returns the amount of removed and added wires.")
    parser.add_argument("-d", action="store_true", help="Returns the amount of netlist changes.")
    parser.add_argument("localfile", type=str, help="Name of the local file.")
    parser.add_argument("gitpath", type=str, help="Path of the file in the repository.")
    args = parser.parse_args()

    if args.d == True:
        try:
            l = get_diff()
            p = parse_diff(l)
            i = interprete_parsed(p)
            print("Netlist Änderungen: ",i[0])
            print("-> davon ersetzte Lines: ",i[1])
            return i[0]
        except Exception as e:
            print(f"\033[91mERROR: {e}\033[0m")
    elif args.w == True:
        print(return_comparison(args.localfile, args.gitpath))

if __name__ == "__main__":
    sys.exit(main())
