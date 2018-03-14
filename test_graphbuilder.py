import unittest
from affinity2 import build_graph, trim_graph


def weight_for(graph, left, right):
    return graph.has_edge(left,right) and graph.get_edge_data(left, right)['weight']  or 0

class TestingGraphBuilder(unittest.TestCase):

    def test_initial_weight_of_one(self):
        g = build_graph([["first", "second"]])
        self.assertEqual(1, weight_for(g, 'first', 'second'))

    def test_initial_weight_across_edges(self):
        g = build_graph([('a', 'b', 'c')])
        self.assertEqual(1, weight_for(g, 'a', 'b'))
        self.assertEqual(1, weight_for(g, 'b', 'c'))

    def test_incrementing_when_edge_repeats(self):
        g = build_graph([('a', 'b'), ('a', 'b')])
        self.assertEqual(2, weight_for(g, 'a', 'b'))

    def test_nonrepeat_does_not_increment(self):
        g = build_graph([
            ('a', 'b', 'c'),
            ('c', 'd', 'e'),
            ('a', 'b', 'd'),
        ])
        self.assertEqual(1, weight_for(g, 'a', 'c'))
        self.assertEqual(1, weight_for(g, 'a', 'd'))
        self.assertEqual(1, weight_for(g, 'b', 'c'))
        self.assertEqual(2, weight_for(g, 'a', 'b'))
        self.assertEqual(1, weight_for(g, 'b', 'd'))
        self.assertEqual(1, weight_for(g, 'c', 'd'))
        self.assertEqual(1, weight_for(g, 'd', 'e'))


class GraphTrimmerTest(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph([
            ('a','b','c','d','e'),
            ('a','b','d','e'),
            ('a','b','e'),
            ('a','c','d','e','f'),
            ('b','c','e'),
            ('f','g','h','i'),
            ('g','h','i'),
            ('f','g','h','i')
        ])

    zero_edges = [
        ('e','i'), ('e','h'), ('e','g'), ('d','i'), ('d','h'), ('d','g'),
        ('c','i'), ('c','h'), ('c','g'), ('b','h'), ('b','g'), ('b','f'),
        ('b','f'), ('a','i'), ('a','h'), ('a','g'),
    ]

    one_edges = [
        ('e','f'), ('d','f'), ('c','f'), ('a','f'),
    ]

    two_edges = [
        ('f','i'), ('f','h'), ('f','g'), ('c','d'), ('b','d'), ('b','c'),
        ('a','c'),
    ]

    three_edges = [ 
        ('h','i'), ('g','i'), ('g','h'), ('d','e'), ('c','e'), ('a','d'),
        ('a','b'),
    ]

    four_edges = [ ('b','e'), ('a','e'), ]
    
    def test_success_in_construction(self):
        def ok(expected, node_pair):
            (left,right) = node_pair
            self.assertEqual(expected, weight_for(self.graph, left, right),
                             "expected %d for edge(%s,%s)" % (expected, left, right))
            
        for edge in self.zero_edges:
            ok(0, edge)
        for edge in self.one_edges:
            ok(1, edge)
        for edge in self.two_edges:
            ok(2, edge)
        for edge in self.three_edges:
            ok(3, edge)
        for edge in self.four_edges:
            ok(4, edge)

    def all_present(self,  edges):
        return all( (self.graph.has_edge(left,right) == True) for (left,right) in edges)

    def all_removed(self, edges):
        return all( (self.graph.has_edge(left,right) == False) for (left,right) in edges)

    def test_zeroEdges_wereNeverFormed(self):
        self.assertTrue(self.all_removed(self.zero_edges))

    def test_trimOnes(self):
        trim_graph(self.graph, 2)
        self.assertTrue(self.all_removed(self.one_edges))
        self.assertTrue(self.all_present(self.two_edges + self.three_edges + self.four_edges))

    def test_trimTwoAndLower(self):
        trim_graph(self.graph, 3)
        self.assertTrue(self.all_removed(self.two_edges + self.one_edges))
        self.assertTrue(self.all_present(self.three_edges + self.four_edges))

