def run_worklist(cfg, name2block):
    worklist = list(name2block.keys())
    wl_in = {}
    wl_out = {}

    for i in range(len(worklist)):
        if i == 0:
            wl_in[worklist[i]] = []
        wl_out[worklist[i]] = []

    while worklist:
        # b = pick any block from worklist
        name = worklist.pop()

        # in[b] = merge(out[p] for every predecessor p of b)
        merge = set()
        for pred in cfg.predecessors[name]:
            merge.update(wl_out[pred])

        wl_in[name] = merge

        # out[b] = transfer(b, in[b])
        transfer = set()
        for instr in name2block[name]:
            if "dest" in instr:
                transfer.add(instr["dest"])
        transfer = transfer.union(set(wl_in[name]))

        # if out[b] changed
        if wl_out[name] != transfer:
            wl_out[name] = transfer
            worklist += cfg.successors[name]

    for name in name2block:
        print_analysis(name, wl_in, wl_out)


def format_vars(var_lst):
    if var_lst:
        return ", ".join(var for var in var_lst)


def print_analysis(name, wl_in, wl_out):
    print(f"\n{name}:")
    print("  in:", format_vars(wl_in[name]))
    print("  out:", format_vars(wl_out[name]))
