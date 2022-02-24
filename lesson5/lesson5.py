#!/usr/local/python/bin/python3

import sys
import json
import argparse
from cfg import CFG
from dominator import Dominator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--cfg",
        action="store_true",
        help="display cfg in dot"
    )
    parser.add_argument(
        "-d",
        "--dom",
        action="store_true",
        help="compute dominators"
    )
    arguments = parser.parse_args()

    program = json.load(sys.stdin)
    for func in program["functions"]:
        cfg = CFG(func["name"], func["instrs"])
        if arguments.cfg:
            print(cfg.dot())
            print()
        
        d = Dominator(cfg)
        if arguments.dom:
            print(d.dom)

        
    #json.dump(program, sys.stdout)
    print()

if __name__ == "__main__":
    main()