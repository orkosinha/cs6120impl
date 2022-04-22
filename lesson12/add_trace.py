#!/usr/local/python/bin/python3

import sys
import json

def main():
    traced_program = json.load(sys.stdin)
    program = traced_program["program"]
    trace = traced_program["trace"]
    main_func = list(filter(lambda x: x["name"] == "main", program["functions"]))[0]
    main_func["instrs"] = trace + [{"label": "bail_function"}] + main_func["instrs"]

    json.dump(program, sys.stdout)

if __name__ == '__main__':
    main()