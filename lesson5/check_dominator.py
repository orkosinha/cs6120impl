def check_dom(cfg, dom, print_paths=False):
    for label, doms in dom.items():
        paths = []
        visited = set()

        def dfs(label, target, path):
            visited.add(label)

            if label == target:
                path += [target]
                paths.append(path)
                return
            
            for succ in cfg.graph[label].successors:
                if succ not in visited:
                    dfs(succ, target, path + [label])
        dfs(cfg.entry, label, [])
     
        if print_paths:
            print(f'Available paths from {cfg.entry} to {label}\n  {paths}')
        
        for d in doms:
            for path in paths:
                if d not in path:
                    return False
        
    return True

