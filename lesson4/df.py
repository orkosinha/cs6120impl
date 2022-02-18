COMMUTATIVE = ["add", "sub", "mul", "div", "eq", "and", "or"]
FOLDABLE = COMMUTATIVE + ["lt", "gt", "le", "ge", "not"]
fold = {
    'add' : lambda x, y: x + y,
    'sub' : lambda x, y: x - y,
    'mul' : lambda x, y: x * y,
    'div' : lambda x, y: int(x / y),
    'eq'  : lambda x, y: x == y,
    'and' : lambda x, y: x and y,
    'or'  : lambda x, y: x or y,
    'lt'  : lambda x, y: x < y,
    'gt'  : lambda x, y: x > y,
    'le'  : lambda x, y: x <= y,
    'ge'  : lambda x, y: x > y,
}

def cp_transfer(block, in_b):
    out = in_b
    for instr in block:
        if 'dest' in instr:
            if instr['op'] == 'const':
                out[instr['dest']] = instr['value']
            elif 'args' in instr:
                if len(instr['args']) == 2 and instr['op'] in FOLDABLE:
                    argl = instr['args'][0]
                    argr = instr['args'][1]

                    if argl in out and out[argl] != '?' and argr in out and out[argr] != '?':
                        out[instr['dest']] = fold[instr['op']](out[argl], out[argr])
                elif instr['op'] == 'id':
                    if instr['args'][0] in out:
                     out[instr['dest']] = out[instr['args'][0]]
                else:
                    out[instr['dest']] = '?'
            else:
                out[instr['dest']] = '?'
    return out
        

def cp_merge(preds):
    out = {}

    for p in preds:
        for var, val in p.items():
            if var in out:
                if out[var] != val:
                    out[var] = '?'
            else:
                out[var] = val

    return out


def run_worklist(cfg, name2block):
    worklist = list(name2block.keys())
    wl_in = {}
    wl_out = {}

    for i in range(len(worklist)):
        if i == 0:
            wl_in[worklist[i]] = {}
        wl_out[worklist[i]] = {}

    while worklist:
        # b = pick any block from worklist
        name = worklist.pop()

        # in[b] = merge(out[p] for every predecessor p of b)
        # merge = set()
        # for pred in cfg.predecessors[name]:
        #     merge.update(wl_out[pred])

        wl_in[name] = cp_merge(wl_out[p] for p in cfg.predecessors[name])

        # out[b] = transfer(b, in[b])
        # transfer = set()
        # for instr in name2block[name]:
        #     if "dest" in instr:
        #         transfer.add(instr["dest"])
        # transfer = transfer.union(set(wl_in[name]))
        transfer = cp_transfer(name2block[name], wl_in[name])

        # if out[b] changed
        if wl_out[name] != transfer:
            wl_out[name] = transfer
            worklist += cfg.successors[name]

    for name in name2block:
        print_analysis(name, wl_in, wl_out)


def format_vars(var_lst):
    if var_lst:
        return ", ".join(f"{var}: {val}" for var, val in var_lst.items())
    


def print_analysis(name, wl_in, wl_out):
    print(f"\n{name}:")
    print("  in:", format_vars(wl_in[name]))
    print("  out:", format_vars(wl_out[name]))
