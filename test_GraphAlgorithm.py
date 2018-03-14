import unittest
import networkx as nx
from networkx.algorithms import community

class FigureOutAlgorithm(unittest.TestCase):
    tight = {'weight':100.0}
    medium = {'weight':50.0}
    weak = {'weight':1.0}

    barbell_set = [
        ('a', 'b', tight),
        ('b', 'c', tight),
        ('c', 'a', tight),

        ('d', 'e', tight),
        ('e', 'f', medium),
        ('g', 'f', tight),
        ('g', 'e', medium),

        # Weak bridge
        ('c', 'g', weak),

    ]

    def test_try_connected_components_on_barbell_graph(self):
        g = nx.Graph()
        g.add_edges_from(x for x in self.barbell_set if x[2]['weight']> 51)
        subgraphs = nx.connected_components(g)
        print("Connected Components:", sorted(subgraphs))


    def test_givran_newman_on_barbell_graph(self):
        g = nx.Graph()
        g.add_edges_from(self.barbell_set)
        algorithm = community.girvan_newman(g)
        [left,right] = next(algorithm)
        first,second = ('a' in left) and (left,right) or (right,left)
        self.assertSetEqual({'a','b','c'}, first)
        self.assertSetEqual({'d','e','f','g'}, second)
        # Note: this gives a similar result, using path closeness instead of weight.
        # This is curious, perhaps meaningful.

    sub_community_graph = [
        ('inner1', 'inner2', tight),
        ('inner2', 'inner3', tight),
        ('inner1', 'inner3', tight),
        ('inner1', 'outer1', medium),
        ('inner1', 'outer2', medium),
        ('inner3', 'outer2', medium),
        ('outer1', 'outer3', tight),
        ('outer2', 'outer3', tight),
        ('outer4', 'outer1', tight),
        ('outer1', 'bridge', weak),
        ('bridge', 'separate1', medium),
        ('separate1', 'separate2', medium),
        ('separate2', 'separate3', medium),
        ('separate3', 'separate1', tight)
    ]
    def test_with_inner_groups(self):
        g = nx.Graph()
        g.add_edges_from(self.sub_community_graph)
        poop = community.girvan_newman(g)
        print("inner groups GN:", next(poop))

    def test_inner_groups_with_subcomponent(self):
        g = nx.Graph()
        g.add_edges_from(x for x in self.sub_community_graph if x[2]['weight'] > 51)
        print("inner groups CC", list(nx.connected_components(g)))
