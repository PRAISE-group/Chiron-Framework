def CNF_To_SMTLIB(cnf, literal_map):
    
    def clause_to_smtlib(clause):
        if not clause:
            raise ValueError("Empty clause is not allowed in CNF.")

        literals = []
        for literal in clause:
            if literal in literal_map:
                literals.append(literal_map[literal])
            elif literal.startswith("~"):
                negated_literal = literal[1:]
                if negated_literal in literal_map:
                    literals.append(f"(not {literal_map[negated_literal]})")
                else:
                    raise ValueError(f"Unknown literal: {literal}")
            else:
                raise ValueError(f"Unknown literal: {literal}")

        def nest_or(exprs):
            if len(exprs) == 1:
                return exprs[0]
            elif len(exprs) == 2:
                return f"(or {exprs[0]} {exprs[1]})"
            else:
                return f"(or {exprs[0]} {nest_or(exprs[1:])})"

        return nest_or(literals)

    clauses = [clause_to_smtlib(clause) for clause in cnf]

    def nest_and(exprs):
        if len(exprs) == 1:
            return exprs[0]
        elif len(exprs) == 2:
            return f"(and {exprs[0]} {exprs[1]})"
        else:
            return f"(and {exprs[0]} {nest_and(exprs[1:])})"
    
    def wrap_with_assert(s):
        return f"(assert{s})"
    
    expression = nest_and(clauses)
    expression = wrap_with_assert(expression)
    
    return expression


