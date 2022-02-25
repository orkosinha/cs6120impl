from collections import OrderedDict
import uuid

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
    
    counter = 0
    for block in blocks:
        if "label" in block[0]:
            label = block[0]["label"]
            block = block[1:]
        else:
            # Generate fresh name from uuid library
            label = f"b{counter}"
            counter += 1

        out[label] = block

    return out

class Node:
    def __init__(self, succs, preds):
        self.successors = succs
        self.predecessors = preds

class CFG:
    def __init__(self, name, body):
        preds = {}
        succs = {}
        self.name = name
        label2block = block_map(form_blocks(body))
        label2node = {}

        for label in label2block.keys():
            label2node[label] = Node([], [])
            preds[label] = []
            succs[label] = []

        for i, (label, block) in enumerate(label2block.items()):
            last = block[-1] if block else None

            if block and last["op"] in ["jmp", "br"]:
                for succ in last["labels"]:
                    succs[label].append(succ)
                    preds[succ].append(label)
                    label2node[label].successors.append(succ)
                    label2node[succ].predecessors.append(label)
            elif block and last["op"] == "ret":
                continue
            else:
                if i < len(label2block) - 1:
                    for succ in [list(label2block.keys())[i + 1]]:
                        succs[label].append(succ)
                        preds[succ].append(label)

                        label2node[label].successors.append(succ)
                        label2node[succ].predecessors.append(label)

        self.predecessors = preds
        self.successors = succs
        self.entry = label2block.popitem(last=False)[0]
        self.graph = label2node

    def reverse_post_order(self):
        visited = set()
        order = []

        def dfs(label):
            visited.add(label)
            for succ in self.graph[label].successors:
                if succ not in visited:
                    dfs(succ)
            order.append(label)

        entry = list(self.graph.keys())[0]
        dfs(entry)
        order.reverse()
        return order

    def dot(self):
        s = f"digraph {self.name} {{\n"

        for label, _ in self.graph.items():
            s += f"  {label.replace('.', '_')}\n"

        for label, node in self.graph.items():
            for succ in node.successors:
                s += f"  {label.replace('.', '_')} -> {succ.replace('.', '_')}\n"

        s += "}\n"
        return s
