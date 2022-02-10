#!/usr/local/python/bin/python3

import json
import sys
import argparse
import tdce

TERMINATORS = ["jmp", "br", "ret"]

# form_blocks based on Lesson 2, Video #2
# https://www.cs.cornell.edu/courses/cs6120/2022sp/lesson/2/
def form_blocks(body):
    block = []

    for instr in body:
        if "op" in instr:
            block.append(instr)

            if instr["op"] in TERMINATORS:
                yield block
                block = []
        else:
            yield block
            block = [instr]

    yield block


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--lvn",
        action="store_true",
        help="perform optimizations using local value numbering",
    )
    parser.add_argument(
        "-d",
        "--dce",
        action="store_true",
        help="perform trivial dead code elimination optimization and dce pass",
    )
    arguments = parser.parse_args()

    program = json.load(sys.stdin)

    blocks = []
    for func in program["functions"]:
        processed_blocks = []
        for block in form_blocks(func["instrs"]):
            if arguments.lvn:
                processed_blocks += tdce.local_dce(block)
            elif arguments.dce:
                processed_blocks += tdce.local_dce(block)
            else:
                processed_blocks += block
        func["instrs"] = processed_blocks
        if arguments.dce:
            meme = tdce.global_dce(func["instrs"])

    json.dump(program, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
