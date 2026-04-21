"""
Regression test for phase-6 SSA renaming metadata.

Bug shape: a join block where variable x has a phi-def and the block's
instruction also defines x. The old representation stored both in a single
`var_version_def[(var, block)]` map, so the second def silently overwrote
the first. The new representation keeps them in separate maps
(`phi_version_def` and `instr_version_def`).

This test builds the CFG for

    :y = 1
    if (:y > 0) [ :x = 1 ] else [ :x = 2 ]
    :x = :x + 1
    forward :x

constructs the SSA side-tables, locates the join block whose instruction is
`:x = :x + 1`, and asserts that phi-def and instruction-def versions for x
are both recorded, are different, and point to the correct def sites.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Match the import layout ssa.py uses so downstream modules resolve the
# same way they do when invoked from chiron.py.
sys.path.insert(0, os.path.join(ROOT, "ChironCore"))
sys.path.insert(0, HERE)

import ChironAST.ChironAST as AST
import cfg.cfgBuilder as cfgB
from ChironAST.builder import astGenPass
from irhandler import getParseTree
from ssa import SSAInfo, get_block_instr, var_defined_by, vars_used_in


PROGRAM = """:y = 1
if (:y > 0) [
    :x = 1
] else [
    :x = 2
]
:x = :x + 1
forward :x
"""


def build_ssa_for_program(src):
    prog_path = os.path.join(HERE, "_ssa_collision_tmp.tl")
    with open(prog_path, "w") as f:
        f.write(src)
    try:
        parse_tree = getParseTree(prog_path)
        ast_gen = astGenPass()
        ir = ast_gen.visitStart(parse_tree)
    finally:
        try:
            os.remove(prog_path)
        except OSError:
            pass
    cfg = cfgB.buildCFG(ir, "test_cfg", isSingle=True)
    ssa = SSAInfo(cfg)
    ssa.build()
    return cfg, ssa


def find_block_with_instr_def(ssa, var):
    """Return any block whose instruction assigns to `var`."""
    for block in ssa.rpo:
        instr = get_block_instr(block)
        if instr is None:
            continue
        if var_defined_by(instr) == var and isinstance(
            instr, AST.AssignmentCommand
        ):
            # Filter down to the one that reads :x (i.e. :x = :x + 1).
            if var in vars_used_in(instr):
                return block
    return None


def main():
    _cfg, ssa = build_ssa_for_program(PROGRAM)

    # Locate the join block: the one whose instruction is :x = :x + 1.
    join_block = find_block_with_instr_def(ssa, ":x")
    assert join_block is not None, "did not find a block with :x = :x + :x"

    # Precondition: the join block must actually have a phi for x — otherwise
    # this test isn't exercising the bug shape.
    assert ":x" in ssa.phi_nodes.get(join_block, {}), (
        f"expected phi for x at join block {join_block.name}, "
        f"got phis={list(ssa.phi_nodes.get(join_block, {}))}"
    )

    phi_ver = ssa.get_phi_def_version(join_block, ":x")
    instr_ver = ssa.get_instr_def_version(join_block, ":x")

    assert phi_ver is not None, (
        f"phi-def version for x at {join_block.name} is missing"
    )
    assert instr_ver is not None, (
        f"instr-def version for x at {join_block.name} is missing"
    )
    assert phi_ver != instr_ver, (
        f"phi-def and instr-def collapsed to the same version "
        f"(phi_ver={phi_ver}, instr_ver={instr_ver}) — metadata is ambiguous"
    )

    # def_site must agree with both maps.
    assert ssa.def_site.get((":x", phi_ver)) is join_block, (
        "def_site disagrees with phi_version_def"
    )
    assert ssa.def_site.get((":x", instr_ver)) is join_block, (
        "def_site disagrees with instr_version_def"
    )

    # The instruction's RHS use of :x must read the phi version, not the
    # instruction-def version (the def is produced AFTER the uses).
    use_ver = ssa.var_version_use.get((":x", join_block))
    assert use_ver == phi_ver, (
        f"expected instruction use to see phi version {phi_ver}, "
        f"got {use_ver}"
    )

    # block_has_phi_def helper sanity-check.
    assert ssa.block_has_phi_def(join_block, ":x")
    assert not ssa.block_has_phi_def(join_block, "nonexistent_var")

    print("OK: phi-def and instr-def for x coexist without metadata collision")
    print(f"    join block: {join_block.name}")
    print(f"    phi-def version:   x_v{phi_ver}")
    print(f"    instr-def version: x_v{instr_ver}")
    print(f"    instruction-use version: x_v{use_ver} (== phi_ver)")


if __name__ == "__main__":
    main()
