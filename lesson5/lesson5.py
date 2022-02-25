#!/usr/local/python/bin/python3

import sys
import json
import argparse
from cfg import CFG
from dominator import Dominator
from check_dominator import check_dom


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
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="test dominators"
    )
    arguments = parser.parse_args()

    program = json.load(sys.stdin)
    for func in program["functions"]:
        cfg = CFG(func["name"], func["instrs"])

        print(cfg.name)

        if arguments.cfg:
            print(cfg.dot())
            print()
        
        d = Dominator(cfg)
        if arguments.dom:
            print(f"Dominator map for {cfg.name}")
            print(f"  {d.dom}")
        
        if arguments.test:
            print(" ", "Passed" if check_dom(cfg, d.dom) else "Failed", "check_dom")
        
        print()
        
    #json.dump(program, sys.stdout)
    print()

if __name__ == "__main__":
    main()