import subprocess
import networkx
from collections import Counter
from itertools import combinations


from gitlogparser import GitLogParser


# Do GIT LOG
edge_collector = Counter()
parser = GitLogParser()
with subprocess.Popen(['git','log','--numstat'], stdout=subprocess.PIPE, universal_newlines=True) as command:
    for commit in parser.feed(command.stdout):
        for edge in combinations(commit, 2):
            edge_collector[edge]+=1

g = networkx.Graph()
for edge,weight in edge_collector.items():
    g.add_edge(edge, weight)



# Okay, we have nodes and weights in the files_in_commits, so convert to a graph
# g.add_edges_from(  ... something cool here .... )
# ... and then do something cool
            

