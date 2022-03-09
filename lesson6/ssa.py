from ast import Or
from cfg import CFG
from dominator import Dominator
from collections import OrderedDict


def rename(block):
    return


def to_ssa(func):
    cfg = CFG(func["name"], func["instrs"])
    d = Dominator(cfg)

    # Generate defs and initialize phi_to_add
    defs = {}
    # Map of label to vars that track which vars need phi nodes in a given label for a block
    label2phi = {}
    # Map of vars to types
    types = {}

    for arg in func.get("args", []):
        defs[arg["name"]] = {cfg.entry}

    for label, block in cfg.label2block.items():
        label2phi[label] = {}

        for instr in block:
            if "dest" in instr:
                if instr["dest"] in defs:
                    defs[instr["dest"]].add(label)
                    types[instr["dest"]] = instr["type"]
                else:
                    defs[instr["dest"]] = {label}

    frontier = d.frontier()
    for var, var_defs in defs.items():
        for label in list(var_defs):
            for f in frontier[label]:
                if var not in label2phi[f]:
                    label2phi[f][var] = {"op": "phi", "args": [], "labels": []}
                    defs[var].add(f)

    stack = {}
    counter = {}
    for var in defs.keys():
        stack[var] = []
        counter[var] = 0

    for arg in func.get("args", []):
        stack[arg["name"]] = [arg["name"]]

    def fresh(var):
        new_var = f"{var}" + (f"_{counter[var]}" if counter[var] else "")
        stack[var].append(new_var)
        counter[var] += 1
        return new_var

    def rename(label):
        pushes = {}

        for var, phi in label2phi[label].items():
            phi["dest"] = fresh(var)

        for instr in cfg.block(label):
            if "args" in instr:
                new_args = [stack[arg][-1] for arg in instr["args"]]
                instr["args"] = new_args

            if "dest" in instr:
                pushes[instr["dest"]] = pushes.get(instr['dest'], 0) + 1
                instr["dest"] = fresh(instr["dest"])

        for succ in cfg.graph[label].successors:
            for var in set(label2phi[succ].keys()):
                if stack[var]: #and types.get(var):
                    label2phi[succ][var]["args"].append(stack[var][-1])
                    label2phi[succ][var]["labels"].append(label)
                    label2phi[succ][var]["type"] = types.get(var)
                else:
                    label2phi[succ].pop(var)
                    
        tree = d.dom_tree()

        for next in tree[label]:
            rename(next)

        # restore stack
        for var, count in pushes.items():
            for i in range(count):
                stack[var].pop()


    rename(cfg.entry)

    for label, block in cfg.label2block.items():
        for var, phi in label2phi[label].items():
            block.insert(0, phi)

    return cfg.to_bril()


def from_ssa(func):
    cfg = CFG(func)

    for label, block in cfg.label2block.items():
        for instr in block:
            if instr.get('op') == 'phi':

                for i, phi_label in enumerate(instr['labels']):
                        new_instr = {
                            'op': 'id',
                            'type': instr['type'],
                            'args': [instr['args'][i]],
                            'dest': instr['dest']
                        }
                        cfg.label2block[label].append(new_instr)
            
        cfg.label2block[label] = filter(lambda i: i.get('op') != 'phi', cfg.label2block[label])
    
    return cfg.to_bril()
    
