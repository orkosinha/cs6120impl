class CFG:
    def __init__(self, name2block):
        preds = {}
        succs = {}

        for name in name2block.keys():
            preds[name] = []
            succs[name] = []

        for i, (name, block) in enumerate(name2block.items()):
            last = block[-1] if block else None

            if block and last["op"] in ["jmp", "br"]:
                for succ in last["labels"]:
                    succs[name].append(succ)
                    preds[succ].append(name)
            elif block and last["op"] == "ret":
                continue
            else:
                if i < len(name2block) - 1:
                    for succ in [list(name2block.keys())[i + 1]]:
                        succs[name].append(succ)
                        preds[succ].append(name)

        self.predecessors = preds
        self.successors = succs
