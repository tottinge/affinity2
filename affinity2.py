import subprocess
import networkx
from collections import Counter
from itertools import combinations


from gitlogparser import GitLogParser



def collect_edge_weights(feed):
    edge_collector = Counter()
    parser = GitLogParser()
    for commit in parser.feed(feed):
        for edge in combinations(commit, 2):
            edge_collector[edge]+=1
    return edge_collector

def build_graph(collection):
    g = networkx.Graph()
    for edge,weight in collection.items():
        g.add_edge(edge, weight)
    return g

# Edge collection and parser feeding need to be separate functions.

def main():
    logSource = subprocess.Popen(['git', 'log', '--numstat'], stdout=subprocess.PIPE, universal_newlines=True)
    n = collect_edge_weights(logSource.stdout)
    g = build_graph(n)

# Next we need to do some kind of interesting analysis

