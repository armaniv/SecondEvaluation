import networkx as nx
import collections as col


def BrandesCutPoint(g):
    n_nodes = len(g.nodes())
    ap = set([x for x in nx.articulation_points(g)])
    bconn = list(nx.biconnected_component_subgraphs(g))

    cp_dict = {}

    for p in ap:
        cp_dict[p] = [b for b in bconn if p in b]

    bc = col.defaultdict(int)

    for p, bconns in cp_dict.items():
        for bcs in bconns:
            h = nx.Graph(g)
            for altrebcs in bconns:
                if(altrebcs != bcs):
                    rimuovi = altrebcs.nodes()
                    rimuovi.remove(p)
                    h.remove_nodes_from(rimuovi)
            b = nx.betweenness_centrality(h, weight='weight', endpoints=False,
                                          normalized=False)[p]
            bc[p] += b
        bc[p] += (n_nodes - 1)
    for n, b in nx.betweenness_centrality(g, weight='weight', endpoints=True,
                                          normalized=False).iteritems():
        if n not in ap:
            bc[n] = b
    return bc


def BC_CutPoint_Interf(g, nodiespansicut, NodiEspansi):
    n_nodes = len(g.nodes())
    bconn = list(nx.biconnected_component_subgraphs(g))

    cp_dict = dict.fromkeys(nodiespansicut, [])

    for p in nodiespansicut:
        cp_dict[p] = [b for b in bconn if p in b]

    bc = col.defaultdict(int)

    for p, bconns in cp_dict.items():
        for bcs in bconns:
            h = nx.Graph(g)
            for altrebcs in bconns:
                if(altrebcs != bcs):
                    rimuovi = altrebcs.nodes()
                    rimuovi.remove(p)
                    h.remove_nodes_from(rimuovi)
            if (AltriNodiDentroBiconnesso(bcs, p, NodiEspansi) == True):
                continue
            else:
                b = nx.betweenness_centrality(h, weight='weight', endpoints=False,
                                              normalized=False)[p]
                bc[p] += b

    return bc


def AltriNodiDentroBiconnesso(b, p, NodiEspansi):
    retval = False
    for nodo in b:
        if (nodo != p) and (nodo in NodiEspansi):
            retval = True
    return False
