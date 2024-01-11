import os, sys

from v4.vote import plurality as voting
from v4.vote import borda as voting2
from v4.vote import parameters_vote as pm

from v4.graph import graph
from v4.examples import read_file as rf
from v4.constants import constants

from v4.other_methods import sums, usums, hna, truthfinder, voting_majo

def noprint_G(G):
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_A
    G.change_norma(norma)
    G.change_vote(voting_method_b, para)
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = sums.Sums(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = usums.Usums(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = hna.Hna(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = truthfinder.Truthfinder(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = voting_majo.VotingMajo(G)
    print(algo)
    algo.run_noprint()
    print("---Results--- :\n")
    print(G.str_trust())
    
def print_G(G):
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_A
    G.change_norma(norma)
    G.change_vote(voting_method_b, para)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    norma = constants.NORMA_O
    G.change_norma(norma)
    print(G.obj.voting_met, G.normalizer.name)
    G.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = sums.Sums(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = usums.Usums(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = hna.Hna(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(G.str_trust())

    algo = truthfinder.Truthfinder(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(G.str_trust())
    
    algo = voting_majo.VotingMajo(G)
    print(algo)
    algo.run()
    print("---Results--- :\n")
    print(G.str_trust())

if __name__ == "__main__":
    #Default parameters
    norma = constants.NORMA_A
    opt = 1
    
    name = "v4/examples/graphes/article.txt"
    
    voting_method_b = voting2.Borda
    
    para = 1
    voting_method = voting.Plurality
    
    for i in range(1, len(sys.argv)):
        if os.path.isfile(sys.argv[i]):
            name = sys.argv[i]
    
    mat_fs, mat_of, truth = rf.read_file(name)
            
    G = graph.Graph(mat_fs, mat_of, voting_method, para, norma, len(mat_fs[0]), len(mat_fs),truth=truth)
    
    print_G(G)
    # noprint_G(G)
    
