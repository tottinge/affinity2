import subprocess
import re
import networkx
import itertools
import collections

file_regex = re.compile("\d+\s+\d+\s*([\w/.]+)$")

counter = collections.Counter()

# Do GIT LOG
with subprocess.Popen(['git','log','--numstat'], stdout=subprocess.PIPE, universal_newlines=true) as command:
    files_in_commit = []

    # Collect file names in the current commit
    for line in command.communicate():
        m = re.match(line)
        if m:
            filename = m.group(1)
            files_in_commit.append(filename)
        else:
            # End of commit, so increment node count for each file pair
            if files_in_commit:
                for pair in itertools.combinations(sorted(files_in_commit),2):
                    counter[pair] +=1
            files_in_commit=[]

# Okay, we have nodes and weights in the files_in_commits, so convert to a graph
g = networkx.Graph()
# g.add_edges_from(  ... something cool here .... )
# ... and then do something cool
            

