import sys
from ChironAST import ChironAST
from cfg import ChironCFG
import networkx as nx

def traverse_cfg(cfg: ChironCFG):
    irList = []
    visited_blocks = set()  # Keep track of visited blocks
    
    start_node = next(node for node in cfg.nodes() if node.irID == "START")
    traversal_order = nx.dfs_preorder_nodes(cfg.nxgraph, source=start_node)
    
    for node in traversal_order:
        if isinstance(node, ChironCFG.BasicBlock):
            if node in visited_blocks:
                continue  # Skip already visited blocks
            visited_blocks.add(node)
            if node.irID == "END":
                # Skip the END node
                continue
            if len(node.instrlist) == 0:
                continue 
            for stmt in node.instrlist:
                if isinstance(stmt[0], ChironAST.BoolTrue) or isinstance(stmt[0], ChironAST.BoolFalse):
                    continue
                
                elif isinstance(stmt[0], ChironAST.AssignmentCommand):
                    if str(stmt[0]).startswith(":__rep_counter_1 = (:__rep_counter_1 - 1)"):
                        irList.append((str(stmt[0]), "loop-end"))
                        continue
                    if str(stmt[0]).startswith(":__rep_counter_1"):
                        irList.append((str(stmt[0]), "loop-init"))
                        continue
                    irList.append((str(stmt[0]), "assign"))
                
                elif isinstance(stmt[0], ChironAST.ConditionCommand):
                    condition = str(stmt[0])
                    if(condition == "True" or condition == "False"):
                        continue
                    elif(condition.startswith("(:__rep_counter_1")):
                        irList.append((condition, "loop-condition"))
                        continue
                    successor = list(cfg.successors(node))
                    if len(successor) != 2:
                        raise ValueError(f"Condition must have exactly two successors: Node: {node}, Statement: {stmt[0]}, Line: {stmt[1]}")
                    trueBranch = successor[0]
                    falseBranch = successor[1]

                    # Mark the true and false branches as visited
                    visited_blocks.add(trueBranch)
                    visited_blocks.add(falseBranch)

                    if len(trueBranch.instrlist) != 2 or len(falseBranch.instrlist) != 1:
                        raise ValueError(f"If-Else branches must have exactly one instruction : Node: {node}, Statement: {stmt[0]}, Line: {stmt[1]}")
                    true_branch_stmt = trueBranch.instrlist[0][0]
                    false_branch_stmt = falseBranch.instrlist[0][0]
                    if not isinstance(true_branch_stmt, ChironAST.AssignmentCommand) or not isinstance(false_branch_stmt, ChironAST.AssignmentCommand):
                        raise ValueError(f"If-Else branches must have assignment statements: Node: {node}, Statement: {stmt[0]}, Line: {stmt[1]}")
                    true_branch_stmt = str(true_branch_stmt)
                    false_branch_stmt = str(false_branch_stmt)
                    true_branch_var = true_branch_stmt.split('=')[0].strip()
                    false_branch_var = false_branch_stmt.split('=')[0].strip()
                    true_branch_expr = true_branch_stmt.split('=')[1].strip()
                    false_branch_expr = false_branch_stmt.split('=')[1].strip()
                    if true_branch_var != false_branch_var:
                        raise ValueError(f"If-Else branches must assign to the same variable: Node: {node}, Statement: {stmt[0]}, Line: {stmt[1]}")
                    ite_stmt = f"{true_branch_var} = ({condition}, {true_branch_expr}, {false_branch_expr})"
                    irList.append((ite_stmt, "ite"))
                
                elif isinstance(stmt[0], ChironAST.AnalysisCommand):
                    analysis_stmt = str(stmt[0])
                    # print(analysis_stmt)
                    if analysis_stmt.startswith("assert"):
                        analysis_stmt = analysis_stmt.split("assert")[-1].strip()
                        irList.append((analysis_stmt, "assert"))
                    elif analysis_stmt.startswith("assume"):
                        analysis_stmt = analysis_stmt.split("assume")[-1].strip()
                        irList.append((analysis_stmt, "assume"))
                    elif analysis_stmt.startswith("invariant"):
                        analysis_stmt = analysis_stmt.split("invariant")[-1].strip()
                        irList.append((analysis_stmt, "invariant"))
                    else:
                        raise ValueError(f"Unsupported analysis command: Node: {node}, Statement: {stmt[0]}, Line: {stmt[1]}")
                else:
                    raise ValueError(f"Unsupported statement type : Node: {node}, Statement: {stmt[0]}, Line: {stmt[1]}")

    return irList