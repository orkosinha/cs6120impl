from pydoc import plain
import z3
import lark
import sys

GRAMMAR = """
?start: sum
  | sum "?" sum ":" sum -> if
  | "let" CNAME "=" start "in" start -> let

?sum: term
  | sum "+" term        -> add
  | sum "-" term        -> sub

?term: item
  | term "*"  item      -> mul
  | term "/"  item      -> div
  | term ">>" item      -> shr
  | term "<<" item      -> shl

?item: NUMBER           -> num
  | "-" item            -> neg
  | CNAME               -> var
  | "(" start ")"

%import common.NUMBER
%import common.WS
%import common.CNAME
%ignore WS
""".strip()


def interp(tree, lookup, update):
    op = tree.data
    if op in (
        "add",
        "sub",
        "mul",
        "div",
        "shl",
        "shr",
    ):
        lhs = interp(tree.children[0], lookup, update)
        rhs = interp(tree.children[1], lookup, update)
        if op == "add":
            return lhs + rhs
        elif op == "sub":
            return lhs - rhs
        elif op == "mul":
            return lhs * rhs
        elif op == "div":
            return lhs / rhs
        elif op == "shl":
            return lhs << rhs
        elif op == "shr":
            return lhs >> rhs
    elif op == "neg":
        sub = interp(tree.children[0], lookup, update)
        return -sub
    elif op == "num":
        return int(tree.children[0])
    elif op == "var":
        return lookup(tree.children[0])
    elif op == "if":
        cond = interp(tree.children[0], lookup, update)
        true = interp(tree.children[1], lookup, update)
        false = interp(tree.children[2], lookup, update)
        return (cond != 0) * true + (cond == 0) * false
    elif op == "let":
        old = update(tree.children[0], interp(tree.children[1], lookup, update))
        result = interp(tree.children[2], lookup, update)
        update(tree.children[0], interp(tree.children[1], lookup, update), False if old else True)
        return result


def solve(phi):
    s = z3.Solver()
    s.add(phi)
    s.check()
    return s.model()


def z3_expr(tree, vars=None):
    vars = dict(vars) if vars else {}

    def get_var(name):
        if name in vars:
            return vars[name]
        else:
            v = z3.BitVec(name, 8)
            vars[name] = v
            return v

    def update(name, value, delete=False):
        if delete:
            del vars[name]
            return None
    
        if name in vars:
            old = vars[name]
            vars[name] = value
            return old
        vars[name] = value
        return None

    return interp(tree, get_var, update), vars


def main(programs):
    parser = lark.Lark(GRAMMAR)

    prog1, vars1 = z3_expr(tree1 := parser.parse(programs[0]))
    prog2, vars2 = z3_expr(tree2 := parser.parse(programs[1]), vars1)

    plain_vars = {k: v for k, v in vars1.items() if not k.startswith("h")}
    goal = z3.ForAll(list(plain_vars.values()), prog1 == prog2)

    print(solve(goal))


if __name__ == "__main__":
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip())
    main(lines)
