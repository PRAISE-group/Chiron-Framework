#!/usr/bin/python3

import sys
#sys.path.insert(0, '../ChironAST/')

from cfg.ChironCFG import *
import ChironAST.ChironAST as ChironAST
import ChironTAC.ChironTAC as ChironTAC
import ChironSSA.ChironSSA as ChironSSA

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

# from graphviz import Source
# import pydot

# import matplotlib
# import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')


def buildCFG(ir, cfgName="", isSingle=False):

    startBB = BasicBlock('START')
    endBB = BasicBlock('END')
    leaderIndices = {0, len(ir)}
    leader2IndicesMap = {startBB : 0, endBB : len(ir)}
    indices2LeadersMap = {0: startBB, len(ir): endBB}

    # finding leaders in the IR
    for idx, item in enumerate(ir):
        #print(idx, item)
        if isinstance(item[0], ChironAST.ConditionCommand) or isinstance(item[0], ChironTAC.ConditionCommand) or isinstance(item[0], ChironSSA.ConditionCommand) or isSingle:
            # updating then branch meta data
            if idx + 1 < len(ir) and (idx + 1 not in leaderIndices):
                leaderIndices.add(idx + 1)
                thenBranchLeader = BasicBlock(str(idx + 1))
                leader2IndicesMap[thenBranchLeader] = idx + 1
                indices2LeadersMap[idx + 1] = thenBranchLeader

            if idx + item[1] < len(ir) and (idx + item[1] not in leaderIndices) and (isinstance(item[0], ChironAST.ConditionCommand) or isinstance(item[0], ChironTAC.ConditionCommand) or isinstance(item[0], ChironSSA.ConditionCommand)):
                leaderIndices.add(idx + item[1])
                elseBranchLeader = BasicBlock(str(idx + item[1]))
                leader2IndicesMap[elseBranchLeader] = idx + item[1]
                indices2LeadersMap[idx + item[1]] = elseBranchLeader


    # adding nodes to Chiron graph
    cfg = ChironCFG(cfgName)
    for leader in leader2IndicesMap.keys():
        cfg.add_node(leader)

    # partitioning the ir list
    # and adding statements to corresponding BasicBlock node
    for currLeader in leader2IndicesMap.keys():
        leaderIdx = leader2IndicesMap[currLeader]
        currIdx = leaderIdx
        while (currIdx < len(ir)):
            currLeader.append((ir[currIdx][0], currIdx))
            currIdx += 1
            if currIdx in leaderIndices: break

    # adding edges
    for node in cfg:
        listSize = len(node.instrlist)
        if listSize:
            irIdx = (node.instrlist[-1])[1]
            lastInstr = (node.instrlist[-1])[0]
            # print (irIdx, lastInstr, type(lastInstr), isinstance(lastInstr, ChironAST.ConditionCommand))
            if isinstance(lastInstr, ChironAST.ConditionCommand) or isinstance(lastInstr, ChironTAC.ConditionCommand) or isinstance(lastInstr, ChironSSA.ConditionCommand):
                if not (isinstance(lastInstr.cond, ChironAST.BoolFalse) or isinstance(lastInstr.cond, ChironTAC.BoolFalse) or isinstance(lastInstr.cond, ChironSSA.BoolFalse)):
                    thenIdx = irIdx + 1 if (irIdx + 1 < len(ir)) else len(ir)
                    thenBB = indices2LeadersMap[thenIdx]
                    cfg.add_edge(node, thenBB, label='Cond_True', color='green')

                if not (isinstance(lastInstr.cond, ChironAST.BoolTrue) or isinstance(lastInstr.cond, ChironTAC.BoolTrue) or isinstance(lastInstr.cond, ChironSSA.BoolTrue)):
                    elseIdx = irIdx + ir[irIdx][1] if (irIdx + ir[irIdx][1] < len(ir)) else len(ir)
                    elseBB = indices2LeadersMap[elseIdx]
                    cfg.add_edge(node, elseBB, label='Cond_False', color='red')
            else:
                nextBB = indices2LeadersMap[irIdx + 1] if (irIdx + 1 < len(ir)) else endBB
                cfg.add_edge(node, nextBB, label='flow_edge', color='blue')

    line2BlockMap = {}
    last_block = None

    for line in range(len(ir)):
        if line in indices2LeadersMap.keys():
            last_block = indices2LeadersMap[line]
        line2BlockMap[line] = last_block
    line2BlockMap[len(ir)] = endBB

    return cfg, line2BlockMap


def dumpCFG(cfg, filename="out"):
    G = cfg.nxgraph

    # generating custom labels for graph nodes
    labels = {}
    for node in cfg:
        labels[node] = node.label()
        # print("bb name : " + node.name + ", ir Id = " + str(node.irID))

    G = nx.relabel_nodes(G, labels)
    A = to_agraph(G)
    A.layout('dot')
    A.draw(filename + ".png")
