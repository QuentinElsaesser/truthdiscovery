from v4.vote import plurality as voting

from v4.graph import graph

from v4.constants import constants

from v4.examples import read_file as rf

import os, sys

if __name__ == "__main__":
    
    #Default parameters
    norma = constants.NORMA_A
    para = 1
    # para = pm.plurality_tie
    name = "v4/examples/graphes/article.txt"
    voting_method = voting.Plurality
    
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == constants.NORMA_O:
            norma = constants.NORMA_O
        elif os.path.isfile(sys.argv[i]):
            name = sys.argv[i]
    
    mat_fs, mat_of, tmptruth = rf.read_file(name)
    truth = [0 for n in mat_fs]
    for i in range(len(tmptruth)):
        truth[tmptruth[i]-1] = 1
    #read file to get that
    #mat_fs_t = [np.array([0,1,0]), np.array([1,0,1]), np.array([0,0,0]), np.array([0,1,0]), np.array([1,0,1])]
    #mat_of_t = [np.array([1,1,1,0,0]), np.array([0,0,0,1,1])]
    
    G = graph.Graph(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs), truth=truth)
    
    print("Plurality + Normalization", G.normalizer.name)
    
    print(G)
    
    G.run()
    
    print("Results :\n")
    print(G.str_trust())
    
    print(G.str_rank_sources())
    print(G.obj.str_rank_facts())
    
