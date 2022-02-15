TERMINATORS = ["jmp", "br", "ret"]
COMMUTATIVE = ["add", "mul", "eq", "and", "or"]
FOLDABLE = COMMUTATIVE + ["lt", "gt", "le", "ge", "not"]


def canonical_value(instr, var2num):
    if instr["op"] == "const":
        return (instr["op"], instr["type"], instr["value"])

    # Instructions should have at least one argument
    # CSE exploiting commutativity
    if instr["op"] in COMMUTATIVE:
        args = sorted(instr["args"])
    else:
        args = instr["args"]

    # Get the numbering associated with the variable
    lvn_args = []
    for arg in args:
        lvn_args.append(var2num[arg])

    if "type" in instr:
        return (instr["op"], instr["type"], *lvn_args)

    return (instr["op"], *lvn_args)


def existing_vars(block):
    used = set()
    declared = set()
    existing = set()
    for instr in block:
        for arg in instr.get("args", []):
            if arg not in declared:
                existing.add(arg)
        declared.update(instr.get("dest", []))
    return existing


def lvn(block):
    # `table` and `var2num` in pseudocode
    # from `https://www.cs.cornell.edu/courses/cs6120/2022sp/lesson/3/

    # Maps value tuple to lvn number
    val2num = {}
    # Maps a var to the associated lvn number
    var2num = {}

    # Maps a number to the var containing the canonical value
    num2var = {}

    # Keeps track of available consts
    consts = {}

    # Keep track of the next lvn next number
    numbering = 1

    for var in existing_vars(block):
        var2num[var] = numbering
        num2var[numbering] = var
        numbering += 1

    for i, instr in enumerate(block):

        var = instr.get("dest")

        args = instr.get("args", []).copy()
        lvn_args = [var2num[var] for var in args]

        if var and instr.get("op") and instr["op"] != "call":
            value = canonical_value(instr, var2num)

            # Find the lvn num of this value
            num = 0

            if instr["op"] == "id":
                # If it's an id, we can get it from the map
                # Copy Propagation
                num = var2num[instr["args"][0]]
                var2num[var] = num
            elif value in val2num:
                # Default way of looking from table
                num = val2num[value]
                var2num[var] = num
            if num != 0:
                # Found a lvn num for the value, so replace it with id and exit loop
                instr["op"] = "id"
                instr["args"] = [num2var[num]]
            else:
                for j in range(i + 1, len(block)):
                    if var == block[j].get("dest"):
                        var2num[var] = numbering
                        var = f"lvn.{var}"
                        break

                instr["dest"] = var

                # Didn't find the value in the table, so add a new number
                var2num[var] = numbering
                num2var[numbering] = var
                val2num[value] = numbering

                numbering += 1

        if args:
            instr["args"] = [num2var[n] for n in lvn_args]

    return block
