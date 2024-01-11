import os, sys

from v4.vote import plurality as voting

from v4.graph import graph
from v4.examples import read_file as rf
from v4.constants import constants

from v4.other_methods import sums, usums, hna, truthfinder, voting_majo

if __name__ == "__main__":
    #Default parameters
    norma = constants.NORMA_A
    para = 1
    name = "v4/examples/graphes/these_singleton.txt"
    voting_method = voting.Plurality
    
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == constants.NORMA_O:
            norma = constants.NORMA_O
        elif os.path.isfile(sys.argv[i]):
            name = sys.argv[i]
    
    mat_fs, mat_of = rf.read_file(name)
    #read file to get that
    #mat_fs_t = [np.array([0,1,0]), np.array([1,0,1]), np.array([0,0,0]), np.array([0,1,0]), np.array([1,0,1])]
    #mat_of_t = [np.array([1,1,1,0,0]), np.array([0,0,0,1,1])]
            
    G = graph.Graph(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs))
    
    n_algo = "hna"
    
    if n_algo == "sums":
        algo = sums.Sums(G)
    elif n_algo == "usums":
        algo = usums.Usums(G)
    elif n_algo == "hna":
        algo = hna.Hna(G)
    elif n_algo == "tf":
        algo = truthfinder.Truthfinder(G)
    elif n_algo == "voting":
        algo = voting_majo.VotingMajo(G)
    
    print(G)
    
    algo.run()
    
    print("Results :\n")
    print(G.str_trust())
    
    print(G.str_rank_sources())
    print(G.obj.str_rank_facts())
    
    
