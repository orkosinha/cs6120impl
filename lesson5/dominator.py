class Dominator:
    
    def __init__(self, cfg):
        order = cfg.reverse_post_order()
        
        # dom = {every block -> all blocks}
        dominator = {label: set(order) for label in order}

        # while dom is still changing:
        changed = True
        while changed:
            changed = False

            # for vertex in CFG:
            for label, node in cfg.graph.items():
                # dom[vertex] = {vertex} ∪ ⋂(dom[p] for p in vertex.preds}
                dom = { label }
                pred_lst = [set(dominator[pred]) for pred in node.predecessors]
                if len(pred_lst) > 0:
                    dom |= pred_lst[0].intersection(*pred_lst[1:])

                changed = dom != dominator[label]
                dominator[label] = dom
        print(dominator)
        self.dom = dominator