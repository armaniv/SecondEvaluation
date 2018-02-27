import networkx as nx
import itertools
import random


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


# funzione ausiliaria per modificare grafo
def CercaNodoCorrispondente(origine, destinazione, nome_arco, grafo):
    ret = float(destinazione) + 0.1
    interf = grafo.node[destinazione]['interfacce']
    for key, value in interf.iteritems():
        for q in value:
            if(q == nome_arco):
                if(key != 0):
                    ret += float(key) / 10
    return str(ret)


# Modifica un grafo generando per ogni nodo una clique di nodi in base al suo
# numero di interfacce
def ModificaGrafo(G, archi):
    rimuovi = []
    nodiConUnInterfaccia = []

    for n in G.nodes():
        rimuovi.append(n)
        num_int = G.node[n]['n_interf']
        elem = []

        if(num_int == 1):
            nodiConUnInterfaccia.append(n)

        for i in range(num_int):
            if(i != 0):
                z = (float(n) + 0.1 + float(i) / 10)
            else:
                z = float(n) + 0.1
            G.add_node(str(z))
            elem.append(str(z))

        for x, y in itertools.combinations(elem, 2):
            G.add_edge(x, y, weight=0.00001)

        interf = G.node[n]['interfacce']

        for key, value in interf.iteritems():
            w = elem[key]
            for q in value:  # ad un interfaccia possono essere attacatti + edge
                if(archi[q][0] != n):
                    to = CercaNodoCorrispondente(n, (archi[q][0]), q, G)
                    G.add_edge(w, to, weight=archi[q][2])  # no nome i nuovi archi
                else:
                    to = CercaNodoCorrispondente(n, (archi[q][1]), q, G)
                    G.add_edge(w, to, weight=archi[q][2])

    G.remove_nodes_from(rimuovi)

    mapping = {}
    for single in nodiConUnInterfaccia:
        mapping[single + '.1'] = single

    G = nx.relabel_nodes(G, mapping, copy=False)


# funzione ausiliaria per i test
def EspandiNodiAll(graph):
    g, archi = ConnettiInterfacce(graph)
    ModificaGrafo(g, archi)
    return g
