#!/usr/bin/env python
from librerie.compute_theoretical_values import *
from librerie.EspandiTuttiNodi import *
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import warnings
import numpy


warnings.filterwarnings("ignore")
graph_kind = set(["erdos", "waxman", "caveman", "barabasi"])


def GeneraGrafoRandom(kind, seed=None, dim=60, prob=0.09):
    if kind not in graph_kind:
        print "Unknown graph type"
        exit()
    if kind == "caveman":
        if dim <= 15:
            g = nx.relaxed_caveman_graph(dim, 10, p=prob, seed=seed)
        else:
            g = nx.relaxed_caveman_graph(10, dim, p=prob, seed=seed)
    if kind == "waxman":
        g = nx.waxman_graph(dim, alpha=1.05, beta=prob)
    if kind == "erdos":
        g = nx.gnp_random_graph(dim, p=prob, seed=seed)
    if kind == "barabasi":
        g = nx.barabasi_albert_graph(dim, m=prob, seed=seed)

    rapportoespansione = [False] * 75 + [True] * 25
    maxinterfacce = 8

    g.remove_nodes_from(nx.isolates(g))

    nx.set_node_attributes(g, 'n_interf', 0)
    nx.set_edge_attributes(g, 'ID', '')

    for n, d in g.nodes_iter(data=True):
        if kind == "waxman":
            del d['pos']

        MenoInterf = random.choice(rapportoespansione)
        if(MenoInterf == False):
            d['n_interf'] = 1
        else:
            d['n_interf'] = random.randint(1, min(g.degree(n), maxinterfacce))

    i = 0
    for u, v, d in g.edges(data=True):
        d['ID'] = 'e' + str(i)
        d['weight'] = float(np.random.uniform(1.0, 1.1))
        i += 1

    if nx.is_connected(g) == False:
        g = GeneraGrafoRandom(kind=kind, seed=seed, dim=dim, prob=prob)

    mapping = {}
    for x in g.nodes():
        mapping[x] = str(x)

    g = nx.relabel_nodes(g, mapping, copy=False)

    return g


def SommaPerditePerNodi(b, cut, interf, inter_cut):

    candidates = []
    candidates = b.select_node_to_fail()

    lossHPop = lossHNonPop = lossLSAPop = lossLSANonPop = L_HPop = L_LSAPop = 0.0
    for cc in candidates:
        h, tc = b.compute_loss(cc[0], pop=True)
        hnp, tcnp = b.compute_loss(cc[0], pop=False)
        lossHPop += h
        lossHNonPop += hnp
        lossLSAPop += tc
        lossLSANonPop += tcnp

    L_HPop = 1.0 - (lossHPop / lossHNonPop)
    L_LSAPop = 1.0 - (lossLSAPop / lossLSANonPop)
    # print "Pop-Ruting:{ L_h= ", 1.0 - (lossHPop / lossHNonPop), ", L_LSA= ", \
    #    1.0 - (lossLSAPop / lossLSANonPop), "}"

#------------------------------------------------------------------------------

    lossHCut = lossHNonCut = lossLSACut = lossLSANonCut = L_HCut = L_LSACut = 0.0
    for cc2 in candidates:
        h, tc = cut.compute_loss(cc2[0], pop=True)
        hnp, tcnp = cut.compute_loss(cc2[0], pop=False)
        lossHCut += h
        lossHNonCut += hnp
        lossLSACut += tc
        lossLSANonCut += tcnp

    L_HCut = 1.0 - (lossHCut / lossHNonCut)
    L_LSACut = 1.0 - (lossLSACut / lossLSANonCut)
    # print "Pop-R  cut:{ L_h= ", 1.0 - (lossHCut / lossHNonCut), ", L_LSA= ", \
    #    1.0 - (lossLSACut / lossLSANonCut), "}"

#------------------------------------------------------------------------------

    lossHInt = lossHNonInt = lossLSAInt = lossLSANonInt = L_HInt = L_LSAInt = 0
    for cc3 in candidates:
        h, hnp, tc, tcnp = interf.compute_loss_interfacce(cc3[0])
        lossHInt += h
        lossHNonInt += hnp
        lossLSAInt += tc
        lossLSANonInt += tcnp

    L_HInt = 1.0 - (lossHInt / lossHNonInt)
    L_LSAInt = 1.0 - (lossLSAInt / lossLSANonInt)
    # print "Pop-R inter:{ L_h= ", 1.0 - (lossHInt / lossHNonInt), ", L_LSA= ", \
    #    1.0 - (lossLSAInt / lossLSANonInt), "}"

#------------------------------------------------------------------------------

    lossHIntCut = lossHNonIntCut = lossLSAIntCut = lossLSANonIntCut = L_HIntCut = L_LSAIntCut = 0
    for cc4 in candidates:
        h, hnp, tc, tcnp = inter_cut.compute_loss_interfacce(cc4[0])
        lossHIntCut += h
        lossHNonIntCut += hnp
        lossLSAIntCut += tc
        lossLSANonIntCut += tcnp

    L_HIntCut = 1.0 - (lossHIntCut / lossHNonIntCut)
    L_LSAIntCut = 1.0 - (lossLSAIntCut / lossLSANonIntCut)
    # print "Pop-R int+cut:{ L_h= ", 1.0 - (lossHIntCut / lossHNonIntCut),\
    #    ", L_LSA= ", 1.0 - (lossLSAIntCut / lossLSANonIntCut), "}"

#------------------------------------------------------------------------------

    return L_HPop, L_LSAPop, L_HCut, L_LSACut, L_HInt, L_LSAInt, L_HIntCut, L_LSAIntCut


p = argparse.ArgumentParser()

p.add_argument("-g", dest="graph", required=False)
p.add_argument("-s", dest="seed", default=None, required=False)
p.add_argument("-t", dest="type", required=False)
p.add_argument("-p", dest="outfile", default=None, required=False)
p.add_argument("-v", dest="view", default=False, required=False,
               action="store_true")
p.add_argument("-x", dest="evluatioTest", default=False, required=False,
               action="store_true")

args = p.parse_args()
if not args.type and not args.graph:
    p.print_help()
    exit()

if args.evluatioTest:
    if args.type:
        if args.type == "waxman":
            fil = open('waxman.dat', 'w')
            diz = {60: 0.096, 100: 0.077, 150: 0.063, 200: 0.053, 250: 0.044}
        elif args.type == "erdos":
            fil = open('erdos.dat', 'w')
            diz = {60: 0.069, 100: 0.042, 150: 0.031, 200: 0.0247, 250: 0.020}
        elif args.type == "caveman":
            fil = open('caveman.dat', 'w')
            diz = {6: 0.05, 10: 0.05, 15: 0.05, 20: 0.01, 25: 0.005}
        elif args.type == "barabasi":
            fil = open('barabasi.dat', 'w')
            diz = {60: 3, 100: 3, 150: 2, 200: 2, 250: 2}

        for diter in sorted(diz.iterkeys()):
            L_HPop, L_LSAPop, L_HCut, L_LSACut, L_HInt, L_LSAInt, L_HIntCut, L_LSAIntCut = (
                [] for i in range(8))

            print diter
            for i in range(10):
                graph = GeneraGrafoRandom(kind=args.type, seed=args.seed,
                                          dim=diter, prob=diz[diter])
                b = ComputeTheoreticalValues(graph=graph, cH=2, cTC=5)
                cut = ComputeTheoreticalValues(graph=graph, cH=2, cTC=5, cent="Cut-point")
                interf = ComputeTheoreticalValues(graph=graph, cH=2, cTC=5, cent="Interfacce")
                inter_cut = ComputeTheoreticalValues(graph=graph, cH=2, cTC=5, cent="Inter-cut")

                LHPop, LLSAPop, LHCut, LLSACut, LHInt, LLSAInt, LHIntCut, LLSAIntCut = SommaPerditePerNodi(
                    b, cut, interf, inter_cut)

                L_HPop.append(LHPop)
                L_LSAPop.append(LLSAPop)
                L_HCut.append(LHCut)
                L_LSACut.append(LLSACut)
                L_HInt.append(LHInt)
                L_LSAInt.append(LLSAInt)
                L_HIntCut.append(LHIntCut)
                L_LSAIntCut.append(LLSAIntCut)
                # print "------------------------------------------------------------"

            nci = 10
            mhPop = sum(L_HPop) / nci
            mlsaPop = sum(L_LSAPop) / nci
            mhCut = sum(L_HCut) / nci
            mlsaCut = sum(L_LSACut) / nci
            mhInt = sum(L_HInt) / nci
            mlsaInt = sum(L_LSAInt) / nci
            mhIntCut = sum(L_HIntCut) / nci
            mlsaIntCut = sum(L_LSAIntCut) / nci

            sdHPop = numpy.std(L_HPop)
            sdLSAPop = numpy.std(L_LSAPop)
            sdHCut = numpy.std(L_HCut)
            sdLSACut = numpy.std(L_LSACut)
            sdHInt = numpy.std(L_HInt)
            sdLSAInt = numpy.std(L_LSAInt)
            sdHIntCut = numpy.std(L_HIntCut)
            sdLSAIntCut = numpy.std(L_LSAIntCut)

            if args.type != "caveman":
                print >> fil, diter, mhPop, mlsaPop, mhCut, mlsaCut, mhInt, \
                    mlsaInt, mhIntCut, mlsaIntCut, sdHPop, sdLSAPop, sdHCut, \
                    sdLSACut, sdHInt, sdLSAInt, sdHIntCut,  sdLSAIntCut

            else:
                print >> fil, (diter * 10), mhPop, mlsaPop, mhCut, mlsaCut, mhInt, \
                    mlsaInt, mhIntCut, mlsaIntCut, sdHPop, sdLSAPop, sdHCut, \
                    sdLSACut, sdHInt, sdLSAInt, sdHIntCut,  sdLSAIntCut
        fil.close()
        exit()
    else:
        exit()

if args.type:
    graph = GeneraGrafoRandom(kind=args.type, seed=args.seed)
    nx.write_graphml(graph, 'temp.graphml')  # necessario per permettere ripetibilita' dei test
    b = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5)
    cut = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5, cent="Cut-point")
    interf = ComputeTheoreticalValues(graph_file='temp.graphml',
                                      cH=2, cTC=5, cent="Interfacce")
    inter_cut = ComputeTheoreticalValues(
        graph_file='temp.graphml', cH=2, cTC=5, cent="Inter-cut")

else:
    if args.graph:
        b = ComputeTheoreticalValues(graph_file=args.graph, cH=2, cTC=5)
        cut = ComputeTheoreticalValues(graph_file=args.graph, cH=2, cTC=5, cent="Cut-point")
        interf = ComputeTheoreticalValues(graph_file=args.graph,
                                          cH=2, cTC=5, cent="Interfacce")
        inter_cut = ComputeTheoreticalValues(
            graph_file=args.graph, cH=2, cTC=5, cent="Inter-cut")

SommaPerditePerNodi(b, cut, interf, inter_cut)

if args.outfile:
    nx.write_graphml(b.G, args.outfile)
if args.view:
    nx.draw(b.G)
    plt.show()
