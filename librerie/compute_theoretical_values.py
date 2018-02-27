#!/usr/bin/env python
import sys
sys.path.append('../')
import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import glob
import numpy as np
import math
import json
from librerie.Bet_cutpoint import BrandesCutPoint
from librerie.EspandiTuttiNodi import EspandiNodiAll
from librerie.Bet_interfacce import BC_interfacce, ListaNodiInalterati
from librerie.Bet_InterCut import BC_interfacce_cutpoint


class ComputeTheoreticalValues():

    def __init__(self, graph_file=None, graph=None, cent="B", cH=2.0, cTC=5.0):

        if graph_file:
            try:
                if (cent == "Interfacce") or (cent == "Inter-cut"):
                    self.G_ori = nx.read_weighted_edgelist(graph_file, nodetype=int)
                    self.G = EspandiNodiAll(self.G_ori)
                else:
                    self.G = nx.read_weighted_edgelist(graph_file, nodetype=int)
            except TypeError:
                if (cent == "Interfacce") or (cent == "Inter-cut"):
                    self.G_ori = nx.read_graphml(graph_file)
                    self.G = EspandiNodiAll(self.G_ori)
                else:
                    self.G = nx.read_graphml(graph_file)
            except:
                print "Can not read files, tried with edge_list and graphml"
                raise
        elif graph:
            if (cent == "Interfacce") or (cent == "Inter-cut"):
                self.G_ori = graph
                self.G = EspandiNodiAll(self.G_ori)
            else:
                self.G = graph

        self.cent = cent
        self.cH = cH
        self.cTC = cTC
        self.decimal_values = 3
        if (cent == "Interfacce") or (cent == "Inter-cut"):
            self.normalization = 2.0 / (nx.number_of_nodes(self.G_ori) *
                                        (nx.number_of_nodes(self.G_ori) - 1))  # 2 perche norlazed=False di networkx normalizza comunque per 1/2
        else:
            self.normalization = 2.0 / (nx.number_of_nodes(self.G) *
                                        (nx.number_of_nodes(self.G) - 1))

        if cent == "B":
            self.bet_dict = nx.betweenness_centrality(self.G, weight='weight', endpoints=True,
                                                      normalized=False)
            self.bet_dict.update((x, y * self.normalization) for x, y in
                                 self.bet_dict.items())

            ap = set([x for x in nx.articulation_points(self.G)])
            print "Nodi cutpoint:", ap

        elif cent == "Cut-point":
            self.bet_dict = BrandesCutPoint(self.G)
            self.bet_dict.update((x, y * self.normalization) for x, y in
                                 self.bet_dict.items())

        elif cent == "Interfacce":
            self.bet_dict = BC_interfacce(self.G_ori, self.G)
            self.bet_dict.update((x, y * self.normalization) for x, y in
                                 self.bet_dict.items())

            self.bet_dict_ori = nx.betweenness_centrality(self.G_ori, weight='weight', endpoints=True,
                                                          normalized=False)
            self.bet_dict_ori.update((x, y * self.normalization) for x, y in
                                     self.bet_dict_ori.items())

        elif cent == "Inter-cut":
            self.bet_dict = BC_interfacce_cutpoint(self.G_ori, self.G)
            self.bet_dict.update((x, y * self.normalization) for x, y in
                                 self.bet_dict.items())

            self.bet_dict_ori = BrandesCutPoint(self.G_ori)
            self.bet_dict_ori.update((x, y * self.normalization) for x, y in
                                     self.bet_dict_ori.items())

        self.deg_dict = self.G.degree()
        self.node_list = filter(lambda x: self.deg_dict[x] > 0, self.G)

        if (cent == "Interfacce") or (cent == "Inter-cut"):
            self.R = len(self.G_ori.edges())
        else:
            self.R = len(self.G.edges())
        self.compute_constants(cent)
        # self.print_constants()
        self.compute_timers()
        # self.check_consistency()

    def compute_constants(self, cent):
        if (cent == "Interfacce") or (cent == "Inter-cut"):
            self.deg_dict_ori = self.G_ori.degree()
            self.node_list_ori = filter(lambda x: self.deg_dict_ori[x] > 0, self.G_ori)
            self.O_H = sum([self.deg_dict_ori[l] for l in self.node_list_ori]) / self.cH
            self.O_TC = len(self.node_list_ori) * self.R / self.cTC
            sqrt_sum = 0
            for node in self.node_list_ori:
                sqrt_sum += math.sqrt(self.deg_dict_ori[node] * self.bet_dict_ori[node])
            self.sq_lambda_H = sqrt_sum / self.O_H
            sqrt_sum = 0
            for node in self.node_list_ori:
                sqrt_sum += math.sqrt(self.R * self.bet_dict_ori[node])
            self.sq_lambda_TC = sqrt_sum / self.O_TC
        else:
            self.O_H = sum([self.deg_dict[l] for l in self.node_list]) / self.cH
            self.O_TC = len(self.node_list) * self.R / self.cTC
            sqrt_sum = 0
            for node in self.node_list:
                sqrt_sum += math.sqrt(self.deg_dict[node] * self.bet_dict[node])
            self.sq_lambda_H = sqrt_sum / self.O_H
            sqrt_sum = 0
            for node in self.node_list:
                sqrt_sum += math.sqrt(self.R * self.bet_dict[node])
            self.sq_lambda_TC = sqrt_sum / self.O_TC

    def compute_timers(self):
        self.Hi = {}
        self.TCi = {}
        for node in self.node_list:
            self.Hi[node] = \
                math.sqrt(self.deg_dict[node] / self.bet_dict[node]) * self.sq_lambda_H
            self.TCi[node] = \
                math.sqrt(self.R / self.bet_dict[node]) * self.sq_lambda_TC

    def select_node_to_fail(self):
        g = self.G.copy()
        # Remove selfloop
        g.remove_edges_from(g.selfloop_edges())
        # maximal subgraph that contains nodes of degree 2
        g_k2 = nx.k_core(g, 2)
        # Find the articulation points of the graph. Removing articulation point
        # increases the number of connected components
        excluded_nodes = [n for n in nx.articulation_points(g_k2)]
        candidate_nodes = [n for n in g_k2.nodes() if n not in excluded_nodes]
        sorted_candidates = []
        for n, c in sorted(self.bet_dict.items(), key=lambda x: -x[1]):
            if n in candidate_nodes:
                sorted_candidates.append((n, self.bet_dict[n]))
        return sorted_candidates

    def compute_loss(self, node, pop=True):
        if pop:
            L_h = self.Hi[node] * self.bet_dict[node]
            L_tc = self.TCi[node] * self.bet_dict[node]
        else:
            L_h = self.cH * self.bet_dict[node]
            L_tc = self.cTC * self.bet_dict[node]
        return L_h, L_tc

    def compute_loss_interfacce(self, node):
        nodi_inaltera = ListaNodiInalterati(self.G_ori, self.G)
        L_h = 0
        L_tc = 0
        L_hnp = 0
        L_tcnp = 0

        if node in nodi_inaltera:
            L_h = self.Hi[node] * self.bet_dict[node]
            L_tc = self.TCi[node] * self.bet_dict[node]
            L_hnp = self.cH * self.bet_dict[node]
            L_tcnp = self.cTC * self.bet_dict[node]
        else:
            num_int = self.G_ori.node[node]['n_interf']
            for x in range(1, (num_int + 1)):
                i = node + '.' + str(x)
                L_h += self.Hi[i] * self.bet_dict[i]
                L_tc += self.TCi[i] * self.bet_dict[i]
                L_hnp += self.cH * self.bet_dict_ori[node]
                L_tcnp += self.cTC * self.bet_dict_ori[node]
            L_h /= num_int
            L_tc /= num_int
            L_hnp /= num_int
            L_tcnp /= num_int

        return L_h, L_hnp, L_tc, L_tcnp
