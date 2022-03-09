class Dominator:
    def __init__(self, cfg):
        self.cfg = cfg
        order = cfg.reverse_post_order()

        # dom = {every block -> all blocks}
        dominator = {label: set(cfg.graph.keys()) for label in cfg.graph.keys()}

        # while dom is still changing:
        changed = True
        while changed:
            changed = False

            # for vertex in CFG:
            for label, node in cfg.graph.items():
                # dom[vertex] = {vertex} ∪ ⋂(dom[p] for p in vertex.preds}
                dom = {label}
                pred_lst = [set(dominator[pred]) for pred in node.predecessors]

                if len(pred_lst) == 1:
                    dom |= pred_lst[0]
                elif len(pred_lst) > 1:
                    dom |= pred_lst[0].intersection(*pred_lst[1:])

                changed = dom != dominator[label]
                if cfg.entry != label:
                    dominator[label] = dom
                else:
                    dominator[label] = {label}
                    changed = False

        self.dom = dominator

    def tree(self):
        dom_inv = {label: set() for label in self.cfg.graph.keys()}
        # Compute post dominance with strict and immediate
        for label, doms in self.dom.items():
            for dom_by in doms:
                if dom_by != label:
                    dom_inv[dom_by].add(label)
        for label1 in dom_inv.keys():
            for label2 in dom_inv.keys():
                if label1 != label2:
                    dom_inv[label1] = dom_inv[label1].difference(dom_inv[label2])

        def tree_builder(label):
            if dom_inv[label]:
                return (label, [tree_builder(l) for l in dom_inv[label]])
            return (label, [])

        return tree_builder(self.cfg.entry)

    def dom_tree(self):
        dom_inv = {key: [] for key in self.dom}
        for p, ss in self.dom.items():
            for s in ss:
                dom_inv[s].append(p)

        dom_inv_strict = {a: {b for b in bs if b != a} for a, bs in dom_inv.items()}
        dom_inv_strict_2x = {
            a: set().union(*(dom_inv_strict[b] for b in bs))
            for a, bs in dom_inv_strict.items()
        }
        return {
            a: {b for b in bs if b not in dom_inv_strict_2x[a]}
            for a, bs in dom_inv_strict.items()
        }

    def frontier(self):
        dom_inv = {key: [] for key in self.dom}
        for p, ss in self.dom.items():
            for s in ss:
                dom_inv[s].append(p)

        frontier = {}
        for block in self.dom:
            dominated_succs = set()
            for dominated in dom_inv[block]:
                dominated_succs.update(self.cfg.graph[dominated].successors)

            frontier[block] = [
                b for b in dominated_succs if b not in dom_inv[block] or b == block
            ]

        return frontier
