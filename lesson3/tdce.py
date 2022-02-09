# Perform dce on a single block
def local_dce(block):
    changed = True

    while changed:
        changed = False
        last_def = {}
        to_delete = []

        for i, instr in enumerate(block):
            # Check for uses
            for arg in instr.get("args", []):
                if arg in last_def:
                    last_def.pop(arg)
            # Check for defs
            if "dest" in instr:
                if instr['dest'] in last_def:
                    # Hasn't been used since redef, so can delete
                    to_delete.append(last_def[instr['dest']])
                last_def[instr['dest']] = i

        for i in reversed(to_delete):
            changed = True
            block.pop(i)
    
    return block


# Perform dce function wide
def global_dce(body):
    used = set()
    prev_inst_count = -1

    while prev_inst_count != len(body):
        for instr in body:
            used.update(instr.get("args", []))
        prev_inst_count = len(body)
        # Removes variables not used as args
        body = list(
            filter(lambda inst: not ("dest" in inst and inst["dest"] not in used), body)
        )
    return body
