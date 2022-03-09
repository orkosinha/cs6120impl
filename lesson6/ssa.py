from cfg import CFG
from dominator import Dominator


def rename(block):
    return


def to_ssa(func):
    cfg = CFG(func["name"], func["instrs"])
    d = Dominator(cfg)

    # Generate defs and initialize phi_to_add
    defs = {}
    # Map of label to vars that track which vars need phi nodes in a given label for a block
    label2phi = {}

    for arg in func.get("args", []):
        defs[arg["name"]] = {cfg.entry}

    for label, block in cfg.label2block.items():
        label2phi[label] = {}

        for instr in block:
            if "dest" in instr:
                if instr["dest"] in defs:
                    defs[instr["dest"]].add(label)
                else:
                    defs[instr["dest"]] = {label}

    frontier = d.frontier()
    for var, var_defs in defs.items():
        for label in list(var_defs):
            for f in frontier[label]:
                block = cfg.block(f)
                if var not in label2phi[f]:
                    label2phi[label][var] = {
                        'op': 'phi',
                        'args': [],
                        'labels': []
                    }
                    defs[var].add(f)

    stack = {}
    counter = {}
    for var in defs.keys():
        stack[var] = []
        counter[var] = 0

    for arg in func.get("args", []):
        stack[arg["name"]] = [arg["name"]]

    def fresh(var):
        new_var = f"{var}" + (f".{counter[var]}" if counter[var] else "")
        stack[var].append(new_var)
        counter[var] += 1
        return new_var
    
    def rename(label, stack):
        prev_stack = stack.copy()

        for var, phi in label2phi[label].items():
            phi['dest'] = fresh(var)

        for instr in cfg.block(label):
            if 'args' in instr:
                new_args = [stack[arg][-1] for arg in instr['args']]
                instr['args'] = new_args
            
            if 'dest' in instr:
                instr['dest'] = fresh(instr['dest'])

        for succ in cfg.graph[label].successors:
            for var in set(label2phi[succ].keys()):
                if not stack[var]:
                    label2phi[succ].pop(var)
                else:
                    label2phi[succ][var]['args'].append(stack[var][-1])
                    label2phi[succ][var]['labels'].append(label)
        
        _, imm_dom = d.tree()

        for next in imm_dom[label]:
            rename(next, prev_stack)
    
    rename(cfg.entry, stack)

    for label, block in cfg.label2block.items():
        for var, phi in label2phi[label].items():
            block.insert(0, phi)
    
    return cfg.to_bril()

def from_ssa(cfg):
    return
