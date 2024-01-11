from v4.vote import plurality as maj
from v4.vote import borda as bor

from v4.constants import constants

from v4.other_methods import sums, usums, hna, truthfinder, voting_majo
from v4.other_methods import averagelog, pooledinvestment, investment

from v4.generation import random_graph as rg
from v4.generation import priors as pr

from copy import deepcopy

class GraphMethods:
    """
    Generate a graph for the 8 methods
    Run all the graph
    
    #use another class for metrics and get the results on the nb_exp graph
    """
    def __init__(self, prior, nbo=10, nbfl=3, nbfu=3, nbs=10, typeg='ncpu', min_fs=1, allg=False):
        self.rgs = []
        self.prior = prior
        self.nbo = nbo
        self.nbs = nbs
        self.nbfl = nbfl
        self.nbfu = nbfu
        self.typeg = typeg
        self.min_fs = min_fs
        self.graphes = []
        
        self.names_nonorma = constants.NAMES_NONORMA
        
        self.names = constants.NAMES
            
    def create_graph(self):
        """
        create graph with default para (Plurality - normaA)
        """
        vote = maj.Plurality
        option = 1
        norma = constants.NORMA_A
            
        return rg.randomGraph(voting_method=vote, 
                                       voting_parameters=option, 
                                       nbs=self.nbs, nbo=self.nbo, 
                                       nbfl=self.nbfl, nbfu=self.nbfu, 
                                       prior=self.prior, norma=norma, 
                                       typeg=self.typeg, min_fs=self.min_fs)
    
    def all_methods(self, i):
        option_vote = self.rgs[0].G.obj.voting_met.option
        rGA = deepcopy(self.rgs[0])
        if constants.ORDER[i] == constants.NAMES[1]:
            rGA.change_norma(constants.NORMA_O)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[2]:
            rGA.change_vote(bor.Borda, option_vote)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[3]:
            rGA.change_norma(constants.NORMA_O)
            rGA.change_vote(bor.Borda, option_vote)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[4]:
            rGA.G = sums.Sums(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[5]:
            rGA.G = usums.Usums(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[6]:
            rGA.G = hna.Hna(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[7]:
            rGA.G = truthfinder.Truthfinder(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[8]:
            rGA.G = voting_majo.VotingMajo(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[9]:
            rGA.G = averagelog.AverageLog(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[10]:
            rGA.G = investment.Investment(rGA.G)
            self.rgs.append(rGA)
        elif constants.ORDER[i] == constants.NAMES[11]:
            rGA.G = pooledinvestment.PooledInvestment(rGA.G)
            self.rgs.append(rGA)
    
    def generate_other_methods(self):
        for i in range(len(constants.NAMES)):
            if constants.ORDER[i] in constants.RUN_METHODS:
                self.all_methods(i)
    
    def run_all(self, interp):
        for g in self.rgs:
            # if isinstance(g.G, graph.Graph):
            #     print(g.G.trust_s, g.G.trust_f)
            # else:
            #     print(g.G.G.trust_s, g.G.G.trust_f)
            g.G.run_noprint()
            # if isinstance(g.G, graph.Graph):
            #     print(g.G.trust_s, g.G.trust_f)
            # else:
            #     print(g.G.G.trust_s, g.G.G.trust_f)
            # print()
            g.update_metric_att(interp)
            
    def add_rg(self, G):
        """
        G : random_graph
        """
        self.rgs.append(G)
        
    def gen_one_graph(self):
        self.add_rg(self.create_graph())
        self.generate_other_methods()
        self.run_all()
    
if __name__ == "__main__":    
    nbo = 2
    nbfl = 2
    nbfu = 2
    
    nbs = 10
    len_prior=10
    
    typeg = 'ncpr'
    
    min_fs=1
    
    bmin=10
    bmax=90
    
    priors = pr.Priors(len_prior=len_prior, nbo=nbo, bmin=bmin, bmax=bmax)
    prc = priors.rand_percent()
    prior = priors.rand_prior(prc)
    print(prc, prior)
    
    graphmet = GraphMethods(prior, nbo=nbo, nbfl=nbfl, nbfu=nbfu, nbs=nbs, typeg=typeg, min_fs=min_fs, allg=False)
    