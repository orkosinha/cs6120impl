#!/usr/local/python/bin/python3

import json
import sys
import argparse
from cfg import CFG
import uuid
from collections import OrderedDict
import df

TERMINATORS = ["jmp", "br", "ret"]

# form_blocks from on Lesson 2, Video #2
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
            if block:
                yield block
            block = [instr]

    if block:
        yield block


# block_map from on Lesson 2, Video #2
# https://www.cs.cornell.edu/courses/cs6120/2022sp/lesson/2/
def block_map(blocks):
    out = OrderedDict()

    for block in blocks:
        if "label" in block[0]:
            name = block[0]["label"]
            block = block[1:]
        else:
            # Generate fresh name from uuid library
            name = f"b.{uuid.uuid4().hex}"

        out[name] = block

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--lvn",
        action="store_true",
        help="perform optimizations using local value numbering and pass of dce",
    )
    arguments = parser.parse_args()

    program = json.load(sys.stdin)

    for func in program["functions"]:
        name2block = block_map(form_blocks(func["instrs"]))
        cfg = CFG(name2block)
        df.run_worklist(cfg, name2block)
    # json.dump(program, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
