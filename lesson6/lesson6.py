#!/usr/local/python/bin/python3

import sys
import json
import argparse
from ssa import to_ssa


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--to-ssa", action="store_true", help="convert bril program to ssa"
    )
    parser.add_argument(
        "--from-ssa", action="store_true", help="convert bril program from ssa"
    )
    arguments = parser.parse_args()

    program = json.load(sys.stdin)
    for func in program["functions"]:
        if arguments.to_ssa:
            instrs = to_ssa(func)
            func['instrs'] = instrs

    json.dump(program, sys.stdout)

if __name__ == "__main__":
    main()
