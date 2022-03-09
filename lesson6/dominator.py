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

        return tree_builder(self.cfg.entry), dom_inv

    def frontier(self):
        frontier = {label: set() for label in self.cfg.graph.keys()}

        for label in self.cfg.graph.keys():
            # Get dominators of this nodes predecessors
            pred_dom = set()
            for pred in self.cfg.graph[label].predecessors:
                pred_dom |= self.dom[pred]
            pred_dom -= self.dom[label] - {label}

            for pred in pred_dom:
                frontier[pred] |= {label}

        return frontier
