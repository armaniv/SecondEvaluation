import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import warnings
import itertools
import random
from librerie.Bet_cutpoint import BrandesCutPoint, BC_CutPoint_Interf
from librerie.Brandes_Salta import betweenness_centrality as BC_salta_nodi

aggiunti = []


def ConnettiInterfacce(graph):
    H = nx.Graph()
    archi = {}

    for n, d in graph.nodes_iter(data=True):
        num_int = d['n_interf']
        interf = {}

        for x in range(num_int):
            interf[x] = []

        H.add_node(str(n), n_interf=d['n_interf'], interfacce=interf)

        i = 0
        for a, b, y in graph.edges_iter(n, data=True):
            archi[y['ID']] = []
            archi[y['ID']].append(str(a))
            archi[y['ID']].append(str(b))
            archi[y['ID']].append(y['weight'])
            if(i >= num_int):
                i = 0
                interf[i].append(y['ID'])
            else:
                interf[i].append(y['ID'])
            i += 1

    return H, archi


def ConnettiNodiStandard(G, archi, UnicoNodoDaEspandere):
    for n in G.nodes():
        if(n in set(aggiunti)):
            continue

        num_int = G.node[n]['n_interf']
        interf = G.node[n]['interfacce']

        for key, value in interf.iteritems():
            for q in value:
                to = archi[q][0]
                da = archi[q][1]
                G.add_edge(da, to, weight=archi[q][2])

        G.remove_nodes_from([UnicoNodoDaEspandere])


def ModificaGrafo(G, archi, UnicoNodoDaEspandere, grafo_origne):
    numnodiorginale = len(G.nodes())

    rimuovi = []
    for n in G.nodes():
        if (n != UnicoNodoDaEspandere):
            continue

        rimuovi.append(n)
        num_int = G.node[n]['n_interf']
        elem = []  # i nuovi nodi
        for i in range(num_int):
            if(i != 0):
                z = round((float(n) + 0.1 + float(i) / 10), 2)
            else:
                z = float(n) + 0.1
            G.add_node(str(z))  # !!! id nodi string, es '4.1'
            elem.append(str(z))

        for x, y in itertools.combinations(elem, 2):
            G.add_edge(x, y, weight=0.00001)

        interf = G.node[n]['interfacce']

        for key, value in interf.iteritems():
            w = elem[key]
            for q in value:  # ad un interfaccia possono essere attacatti + edge
                if(archi[q][0] != n):
                    to = archi[q][0]
                    G.add_edge(w, to, weight=archi[q][2])  # no nome i nuovi archi
                else:
                    to = archi[q][1]
                    G.add_edge(w, to, weight=archi[q][2])
                aggiunti.append(w)

    G.remove_nodes_from(rimuovi)

    ConnettiNodiStandard(G, archi, UnicoNodoDaEspandere)

    tempBC = ContaCammini(G, grafo_origne, rimuovi[0])

    return tempBC


def ContaCammini(G, grafo_origne, nodo11):
    GrafoOrigine = grafo_origne
    startingNodes = list(GrafoOrigine.nodes())

    ap = set([x for x in nx.articulation_points(G)])

    NodiDopoEspansione = list(G.nodes())

    nodiInalterati = list(set(startingNodes) & set(NodiDopoEspansione))

    NodiEspansi = set(NodiDopoEspansione) - set(nodiInalterati)
    BC = dict.fromkeys(NodiEspansi, (len(startingNodes) - 1))

    NodiEspansiCutPoint = []
    NodiEspansiNonCut = []

    for i in NodiEspansi:
        if i in ap:
            NodiEspansiCutPoint.append(i)
        else:
            NodiEspansiNonCut.append(i)

    if len(NodiEspansiNonCut) > 0:
        BCprimo = BC_salta_nodi(G, NodiEspansi, weight='weight', endpoints=False,
                                normalized=False)
        BCsecondo = BC_salta_nodi(G, nodiInalterati, weight='weight',
                                  endpoints=False, normalized=False)
        BCClique = {}

        for key, value in BCprimo.items():
            BCClique[key] = value - BCsecondo[key]

        for k in NodiEspansiNonCut:
            BC[k] += BCClique[k]

    if len(NodiEspansiCutPoint) > 0:
        bc_cut_temp = BC_CutPoint_Interf(G, NodiEspansiCutPoint, NodiEspansi)
        for i in NodiEspansiCutPoint:
            BC[i] += bc_cut_temp[i]

    return BC


def BC_interfacce_cutpoint(graph, grafo_espanso):
    bet_cent = dict.fromkeys(grafo_espanso.nodes(), 1.0)

    BC_origin = BrandesCutPoint(graph)

    g, archi = ConnettiInterfacce(graph)

    for n, d in graph.nodes_iter(data=True):
        if d['n_interf'] != 1:
            g2 = g.copy()
            bc_temp = ModificaGrafo(g2, archi, str(n), graph)  # !!! id nodi string
            for key, value in bc_temp.items():
                bet_cent[key] = value
        else:
            bet_cent[str(n)] = BC_origin[n]

    return bet_cent
