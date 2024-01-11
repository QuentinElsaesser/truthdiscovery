# graph.py

Here we create a graph and then run the algorithm.

We have 2 vectors for the reliability of the sources and the facts (in the code trust_s and trust_f).

We have 2 adjacency matrix. One between the facts and the sources (1 if a fact is claimed by a source, O otherwise).

We have a method to create the graph and the methods to compute the reliability of the sources and the facts.

# node.py

The node will represent the facts and the objects because we use that to do the vote and assign the score to the facts depending on the scoring voting rule.

A fact can be true or false. It has a reliability (trust in the code) and a score (score given by the scoring rule).

An object have a list of predecessor.

All the nodes have a number of predecessor (the facts have an empty list of predecessor because we do not need to represent the sources as a node)

# obj.py

In this class we run the voting method and assign the score to the facts. We also create the links between the facts and the objects.