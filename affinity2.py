import subprocess
import networkx
from collections import Counter
from itertools import combinations

from gitlogparser import GitLogParser


def build_graph(collection):
    """
    This routine is passed a collection of groups of filenames, indicating that the files in each group/list were
    committed together (as returned by gitlogparser). From that, it creates a network of edges where each edge
    has a 'weight' which is a count of the number of times the two nodes were committed together.
    """
    g = networkx.Graph()
    for commit in collection:
        for (left,right) in combinations(commit,2):
            if not g.has_edge(left,right):
                g.add_edge(left, right, weight=1)
            else:
                g.get_edge_data(left,right)['weight'] += 1
    return g


def trim_graph(graph, lower_limit):
    """
    This routine will delete all nodes where the 'weight' (number of times nodes were committed together)
    falls below a given threshold.

    The graph is modified in-place.
    """
    below_grade = [ e[:2] for e in graph.edges(data='weight') if e[2] is None or e[2] < lower_limit]
    graph.remove_edges_from(below_grade)


def main(source):
    p = GitLogParser()
    g = build_graph(p.feed(source))
    average_strength = sum(weight for (_,_,weight) in g.edges(data='weight'))/g.number_of_edges();
    lower_limit = average_strength  # Wild approximation
    trim_graph(g, lower_limit or 1)
    components = networkx.connected_components(g)
    for (seq, subgroup) in enumerate( sorted(components, key=lambda x: len(x), reverse=True) ):
        if len(subgroup) < 5:
            break
        print("Sequence: %d" % seq)
        for item in sorted(subgroup):
            print(" "*4, item)
    return components

if __name__ == '__main__':
    g = main(open("gitlog.ascii", "r"))
