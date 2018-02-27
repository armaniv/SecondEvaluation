#!/usr/bin/env python
from librerie.compute_theoretical_values import *
from librerie.EspandiTuttiNodi import *
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import warnings


warnings.filterwarnings("ignore")
graph_kind = set(["erdos", "waxman", "caveman"])


def GeneraGrafoRandom(kind, seed=None):
    if kind not in graph_kind:
        print "Unknown graph type"
        exit()
    if kind == "caveman":
        g = nx.relaxed_caveman_graph(8, 7, 0.12, seed=seed)
    if kind == "waxman":
        g = nx.waxman_graph(200, alpha=0.9)
    if kind == "erdos":
        g = nx.gnp_random_graph(60, 0.08, seed=seed)

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
        print "Graph not connected, exit."
        exit()

    mapping = {}
    for x in g.nodes():
        mapping[x] = str(x)

    g = nx.relabel_nodes(g, mapping, copy=False)

    return g


def SommaPerditePerNodi(b, cut, interf, inter_cut):

    candidates = b.select_node_to_fail()

    lossHPop = 0
    lossHNonPop = 0
    lossLSAPop = 0
    lossLSANonPop = 0
    for cc in candidates:
        h, tc = b.compute_loss(cc[0], pop=True)
        hnp, tcnp = b.compute_loss(cc[0], pop=False)
        lossHPop += h
        lossHNonPop += hnp
        lossLSAPop += tc
        lossLSANonPop += tcnp

    print "Pop-Ruting:{ L_h= ", 1.0 - (lossHNonPop / lossHPop), ", L_LSA= ", \
        1.0 - (lossLSANonPop / lossLSAPop), "}"

    lossHCut = 0
    lossHNonCut = 0
    lossLSACut = 0
    lossLSANonCut = 0
    for cc2 in candidates:
        h, tc = cut.compute_loss(cc2[0], pop=True)
        hnp, tcnp = cut.compute_loss(cc2[0], pop=False)
        lossHCut += h
        lossHNonCut += hnp
        lossLSACut += tc
        lossLSANonCut += tcnp

    print "Pop-R  cut:{ L_h= ", 1.0 - (lossHNonCut / lossHCut), ", L_LSA= ", \
        1.0 - (lossLSANonCut / lossLSACut), "}"

    lossHInt = 0
    lossHNonInt = 0
    lossLSAInt = 0
    lossLSANonInt = 0
    for cc3 in candidates:
        h, hnp, tc, tcnp = interf.compute_loss_interfacce(cc3[0])
        lossHInt += h
        lossHNonInt += hnp
        lossLSAInt += tc
        lossLSANonInt += tcnp

    print "Pop-R inter:{ L_h= ", 1.0 - (lossHNonInt / lossHInt), ", L_LSA= ", \
        1.0 - (lossLSANonInt / lossLSAInt), "}"

    lossHIntCut = 0
    lossHNonIntCut = 0
    lossLSAIntCut = 0
    lossLSANonIntCut = 0
    for cc4 in candidates:
        h, hnp, tc, tcnp = inter_cut.compute_loss_interfacce(cc4[0])
        lossHIntCut += h
        lossHNonIntCut += hnp
        lossLSAIntCut += tc
        lossLSANonIntCut += tcnp

    print "Pop-R int+cut:{ L_h= ", 1.0 - (lossHNonIntCut / lossHIntCut),\
        ", L_LSA= ", 1.0 - (lossLSANonIntCut / lossLSAIntCut), "}"


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
        for i in range(3):
            graph = GeneraGrafoRandom(kind=args.type, seed=args.seed)
            nx.write_graphml(graph, 'temp.graphml')
            b = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5)
            cut = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5, cent="Cut-point")
            interf = ComputeTheoreticalValues(
                graph_file='temp.graphml', cH=2, cTC=5, cent="Interfacce")
            inter_cut = ComputeTheoreticalValues(
                graph_file='temp.graphml', cH=2, cTC=5, cent="Inter-cut")

            SommaPerditePerNodi(b, cut, interf, inter_cut)
            print "------------------------------------------------------------"
        exit()
    else:
        exit()

if args.type:
    graph = GeneraGrafoRandom(kind=args.type, seed=args.seed)
    nx.write_graphml(graph, 'temp.graphml')  # necessario per permettere ripetibilita' dei test
    b = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5)
    cut = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5, cent="Cut-point")
    interf = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5, cent="Interfacce")
    inter_cut = ComputeTheoreticalValues(graph_file='temp.graphml', cH=2, cTC=5, cent="Inter-cut")

else:
    if args.graph:
        b = ComputeTheoreticalValues(graph_file=args.graph, cH=2, cTC=5)
        cut = ComputeTheoreticalValues(graph_file=args.graph, cH=2, cTC=5, cent="Cut-point")
        interf = ComputeTheoreticalValues(graph_file=args.graph, cH=2, cTC=5, cent="Interfacce")
        inter_cut = ComputeTheoreticalValues(graph_file=args.graph, cH=2, cTC=5, cent="Inter-cut")

SommaPerditePerNodi(b, cut, interf, inter_cut)

if args.outfile:
    nx.write_graphml(b.G, args.outfile)
if args.view:
    nx.draw(b.G)
    plt.show()
