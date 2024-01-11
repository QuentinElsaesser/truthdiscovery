from v4.graph import graph

from v4.generation import att_metrics as am

from v4.constants import constants

import random
import numpy as np


# import matplotlib.pyplot as plt

class randomGraph:
    def __init__(self, voting_method, voting_parameters, nbs=10, nbo=10, 
                 nbfl=3, nbfu=3, 
                 prior=[0.1,0.2,0.3,0.4,0.5], norma=constants.NORMA_A, typeg='ncpu',
                 min_fs=1, sf=None, of=None, truth=None):
        """
        voting_method : voting method
        voting_paramters : parameters for the voting method
        nbs : number of sources
        nbo : number of object
        nbfl : number of fact by object (min)
        nbfu : number of fact by object (max)
        prior : proba to choose the true fact on each object for the sources
        norma : normalization for the algorithm
        typeg : type of graph we generate
        min_fs : minimum number of facts for a source
        """
        self.voting_met = voting_method
        self.voting_para = voting_parameters
        self.nbs = nbs
        self.nbo = nbo
        self.nbf = 0
        self.nbfl = nbfl
        self.nbfu = nbfu
        self.min_fs = (min_fs if min_fs <= nbo else nbo)
        self.norma = norma
        self.typeg = typeg
        if sf == None:# and of == None and truth == None:
            self.true_facts = []
            self.of = self.rand_of(nbfl, nbfu)
            self.sf = [[0 for j in range(self.nbf)] for i in range(self.nbs)]
            self.fs = [[0 for j in range(self.nbs)] for i in range(self.nbf)]
            self.prior_src = self.generate_prior(prior)
            self.generate_graph()
            self.posterioriA, self.posteriori_trustA = self.generate_posteriori(constants.NORMA_A)
            self.posterioriO, self.posteriori_trustO = self.generate_posteriori(constants.NORMA_O)
            if self.norma == constants.NORMA_A:
                self.posteriori, self.posteriori_trust = self.posterioriA, self.posteriori_trustA
            else:
                self.posteriori, self.posteriori_trust = self.posterioriO, self.posteriori_trustO
        else:
            # self.true_facts = [int(n) for n in truth.split("-")]
            self.true_facts = truth
            self.nbf = len(self.true_facts)
            self.of = of
            self.sf = sf
            self.fs = self.gen_fs()
            self.posterioriA, self.posteriori_trustA = self.generate_posteriori(constants.NORMA_A)
            self.posterioriO, self.posteriori_trustO = self.generate_posteriori(constants.NORMA_O)
            if self.norma == constants.NORMA_A:
                self.posteriori, self.posteriori_trust = self.posterioriA, self.posteriori_trustA
            else:
                self.posteriori, self.posteriori_trust = self.posterioriO, self.posteriori_trustO
            self.prior_src = self.posteriori_trust
        
        #averaged trust with the edges
        self.theoritical_trust = self.min_maj(self.posteriori_trustA)
        
        if self.typeg == 'ncrand' or self.typeg == 'crand':
            self.prior_src = self.posteriori_trust
            
        self.array_to_np()
        
        self.G = graph.Graph(self.fs, self.of, self.voting_met, self.voting_para, 
                             self.norma, len(self.fs[0]), len(self.fs),
                             truth=self.true_facts)
        
        self.metric_att = None
        
    def gen_fs(self):
        res = [[0 for n in self.sf] for i in self.sf[0]]
        for i in range(len(self.sf)):
            for j in range(len(self.sf[i])):
                if self.sf[i][j] == 1:
                    res[j][i] = 1
        return res
        
    def update_metric_att(self, interp=None):
        self.metric_att = am.AttMetrics(self, interp)
        self.metric_att.run_all()
        
    def change_norma(self, norma):
        self.norma = norma
        self.G.change_norma(self.norma)
        if self.norma == constants.NORMA_A:
            self.posteriori, self.posteriori_trust = self.posterioriA, self.posteriori_trustA
        else:
            self.posteriori, self.posteriori_trust = self.posterioriO, self.posteriori_trustO
        self.theoritical_trust = self.min_maj(self.posteriori_trustA)
        
    def change_vote(self, voting_met, voting_para):
        self.voting_met = voting_met
        self.voting_para = voting_para
        self.G.change_vote(self.voting_met, self.voting_para)
    
    def min_maj(self, proba):
        """
        percentage we have depending on the proba
        """
        link = 0
        total = 0
        for p in proba:
            link += p
            total += 1
        tmp = link/total
        return round(tmp*100)
    
    def array_to_np(self):
        for i in range(len(self.fs)):
            self.fs[i] = np.array(self.fs[i])
        for i in range(len(self.of)):
            self.of[i] = np.array(self.of[i])
        
    def rand_of(self, nbfl, nbfu):
        """
        generation of the links facts objects
        """
        res = []
        
        tmp = [random.randint(nbfl, nbfu) for i in range(self.nbo)]
        self.nbf = sum(tmp)
        of = [0 for i in range(self.nbf)]
        self.true_facts = of.copy()
        n = 0
        for v in tmp:
            ofc = of.copy()
            self.true_facts[random.randint(n,v+n-1)] = 1
            for j in range(n,v+n):
                ofc[j] = 1
            res.append(np.array(ofc))
            n += v
        return res
    
    def generate_prior(self, prior):
        """
        generation of the prior for each source
        the number of sources and the length of the prior must be a multiple
        """
        if self.nbs % len(prior) != 0:
            raise ValueError("Error, self.nbs {self.nbs} not a multiplier of len(prior) {len(prior)}")
        res = []
        n = int(self.nbs / len(prior))
        for i in range(len(prior)):
            for j in range(n):
                res.append(prior[i])
        return res
    
    def generate_posteriori(self, norma):
        res = [0 for i in range(self.nbs)]
        for i in range(len(self.fs)):
            if self.true_facts[i] == 1:
                for j in range(len(self.fs[i])):
                    res[j] += self.fs[i][j]
        if norma == constants.NORMA_A:
            for i in range(len(res)):
                res[i] /= self.nbo
        elif norma == constants.NORMA_O:
            for i in range(len(res)):
                res[i] /= np.count_nonzero(np.array(self.sf[i]) == 1)
        src_p = []
        post = []
        for i in range(len(res)):
            src_p.append((i+1, res[i]))
            post.append(res[i])
        return src_p, post
    
    def proba_rand(self, p, nbf):
        """
        return a vector with the proba randomly distributed
        """
        res = [0 for i in range(nbf)]
        for i in range(nbf):
            if i == nbf-1:
                res[i] = p
                np.random.shuffle(res)
                return res
            res[i] = round(np.random.uniform(0, p), 2)
            p -= res[i]
            if p <= 0:
                np.random.shuffle(res)
                return res
        np.random.shuffle(res)
        return res
    
    def proba_unif(self, p, nbf):
        """
        return a vector with the same proba for all the elements
        """
        proba = p/nbf
        return [proba for i in range(nbf)]
    
    def generate_proba(self, prior, ind_o, typeg='r'):
        """
        prior : prior for the source to choose the true fact
        typeg : r if random and u if uniform (to give 1-prior to the other facts)
        nbf : number of facts on this object
        """
        nbf = np.count_nonzero(self.of[ind_o] == 1)
        if nbf == 1:
            return [1.0]
        p = 1-prior
        index = np.where(self.of[ind_o] == 1)[0]
        res = [0 if self.true_facts[i] == 0 else prior for i in index]
        if typeg == 'r':
            proba_false = self.proba_rand(p, nbf-1)
        else:
            proba_false = self.proba_unif(p, nbf-1)
        n = 0
        for i in range(len(res)):
            if res[i] == 0:
                res[i] = proba_false[n]
                n += 1
        return res
        
    def generate_ncpr(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            nbo = round(np.random.uniform(self.min_fs, self.nbo))
            choice = [1 for j in range(nbo)] + [0 for j in range(self.nbo-nbo)]
            np.random.shuffle(choice)
            for j in range(self.nbo):
                if choice[j] == 1:
                    proba = self.generate_proba(self.prior_src[i], typeg='r', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
        
    def generate_ncpu(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            nbo = round(np.random.uniform(self.min_fs, self.nbo))
            choice = [1 for j in range(nbo)] + [0 for j in range(self.nbo-nbo)]
            np.random.shuffle(choice)
            for j in range(self.nbo):
                if choice[j] == 1:
                    proba = self.generate_proba(self.prior_src[i], typeg='u', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                    
    def generate_cpu(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            for j in range(self.nbo):
                proba = self.generate_proba(self.prior_src[i], typeg='u', ind_o=j)
                index = np.where(self.of[j] == 1)[0]
                f = np.random.choice(index, size=1, p=proba)[0]
                #print(f"src {i+1} choose fact {f}")
                self.fs[f][i] = 1
                self.sf[i][f] = 1
                
    def generate_cpr(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            for j in range(self.nbo):
                proba = self.generate_proba(self.prior_src[i], typeg='r', ind_o=j)
                index = np.where(self.of[j] == 1)[0]
                f = np.random.choice(index, size=1, p=proba)[0]
                #print(f"src {i+1} choose fact {f}")
                self.fs[f][i] = 1
                self.sf[i][f] = 1
                
    def generate_randc(self):
        """
        generate complete graph without prior
        """
        for i in range(self.nbs):
            for j in range(self.nbo):
                proba = self.proba_unif(1.0, np.count_nonzero(self.of[j] == 1))
                index = np.where(self.of[j] == 1)[0]
                f = np.random.choice(index, size=1, p=proba)[0]
                #print(f"src {i+1} choose fact {f}")
                self.fs[f][i] = 1
                self.sf[i][f] = 1
                
    def generate_randnc(self):
        """
        generate non complete graph without prior
        """
        for i in range(self.nbs):
            nbo = round(np.random.uniform(self.min_fs, self.nbo))
            choice = [1 for j in range(nbo)] + [0 for j in range(self.nbo-nbo)]
            np.random.shuffle(choice)
            for j in range(self.nbo):
                if choice[j] == 1:
                    proba = self.proba_unif(1.0, np.count_nonzero(self.of[j] == 1))
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                    
    def generate_cfu(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            co = int(self.prior_src[i]*self.nbo)
            nco = int(self.nbo - co)
            choice = [1 for i in range(co)] + [0 for i in range(nco)]
            np.random.shuffle(choice)
            for j in range(self.nbo):
                if choice[j] == 1:
                    proba = self.generate_proba(1.0, typeg='u', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                else:
                    proba = self.generate_proba(0.0, typeg='u', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                    
    def generate_cfr(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            co = int(self.prior_src[i]*self.nbo)
            nco = int(self.nbo - co)
            choice = [1 for i in range(co)] + [0 for i in range(nco)]
            np.random.shuffle(choice)
            for j in range(self.nbo):
                if choice[j] == 1:
                    proba = self.generate_proba(1.0, typeg='r', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                else:
                    proba = self.generate_proba(0.0, typeg='r', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                    
    def generate_ncfr(self):
        """
        Each source claim at least 1 fact
        """
        for i in range(self.nbs):
            co = int(self.prior_src[i]*self.nbo)
            nco = int(self.nbo - co)
            choice = [1 for i in range(co)] + [0 for i in range(random.randint(0, nco))]
            np.random.shuffle(choice)
            for j in range(len(choice)):
                if choice[j] == 1:
                    proba = self.generate_proba(1.0, typeg='r', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
                else:
                    proba = self.generate_proba(0.0, typeg='r', ind_o=j)
                    index = np.where(self.of[j] == 1)[0]
                    f = np.random.choice(index, size=1, p=proba)[0]
                    #print(f"src {i+1} choose fact {f}")
                    self.fs[f][i] = 1
                    self.sf[i][f] = 1
        
    # def generate_proba_test(self, prior, ind_o):
    #     """
    #     prior : prior for the source to choose the true fact
    #     typeg : r if random and u if uniform (to give 1-prior to the other facts)
    #     nbf : number of facts on this object
    #     """
    #     nbf = np.count_nonzero(self.of[ind_o] == 1)
    #     if nbf == 1:
    #         return [1.0]

    #     c = np.random.choice([1,0], size=1, p=[prior, 1-prior])[0]
    #     index = np.where(self.of[ind_o] == 1)[0]
    #     if c == 1:
    #         return [0 if self.true_facts[i] == 0 else 1 for i in index]
        
    #     proba_false = self.proba_unif(1.0, nbf-1)
    #     res = [1 if self.true_facts[i] == 0 else 0 for i in index]
    #     n = 0
    #     for i in range(len(res)):
    #         if res[i] == 1:
    #             res[i] = proba_false[n]
    #             n += 1
    #     return res
        
    # def generate_test(self):
    #     """
    #     Each source claim at least 1 fact
    #     """
    #     for i in range(self.nbs):
    #         nbo = round(np.random.uniform(self.min_fs, self.nbo))
    #         choice = [1 for j in range(nbo)] + [0 for j in range(self.nbo-nbo)]
    #         np.random.shuffle(choice)
    #         for j in range(self.nbo):
    #             if choice[j] == 1:
    #                 proba = self.generate_proba_test(self.prior_src[i], ind_o=j)
    #                 index = np.where(self.of[j] == 1)[0]
    #                 f = np.random.choice(index, size=1, p=proba)[0]
    #                 #print(f"src {i+1} choose fact {f}")
    #                 self.fs[f][i] = 1
    #                 self.sf[i][f] = 1
        
    def generate_graph(self):
        """
        generate the graph depending the typeg attirbute
        """
        if self.typeg == 'ncpr':
            self.generate_ncpr()
        elif self.typeg == 'ncpu':
            self.generate_ncpu()
        elif self.typeg == 'cpu':
            self.generate_cpu()
        elif self.typeg == 'cpr':
            self.generate_cpr()
        elif self.typeg == 'crand':
            self.generate_randc()
        elif self.typeg == 'ncrand':
            self.generate_randnc()
        elif self.typeg == 'cfu':
            self.generate_cfu()
        elif self.typeg == 'cfr':
            self.generate_cfr()
        elif self.typeg == 'ncfr':
            self.generate_ncfr()
        # elif self.typeg == 'test':
        #     self.generate_test()
        else:
            raise ValueError(f"No type specified/recognized in self.typeg {self.typeg}")
        
# if __name__ == "__main__":
#     vote = voting.Plurality
#     para = pm.plurality_opti
#     # vote = voting2.Borda
#     # para = pm.borda_opti
#     nbo = 10
#     nbfl = 2
#     nbfu = 4
#     nbs = 10
#     min_src = 10
#     norma = constants.NORMA_A
#     typeg = 'ncrand'
#     if 'rand' in typeg:
#         prior = [0]
        
#     rg = randomGraph(vote, para, nbo=nbo, nbfl=nbfl, nbfu=nbfu, nbs=nbs, 
#                    norma=norma, prior=prior, typeg=typeg, min_fs=1)
    
#     #tmp = rg.generate_proba(0.8, 2, 'u')
#     #index = np.where(rg.of[2] == 1)[0]
#     #print(rg.true_facts[index[0]:index[-1]+1])
#     #print(tmp, sum(tmp))
    
#     #print(list(map(int, rg.G.list_sf().split("-")[0].split(","))))
#     #print(rg.G.list_sf())
    
#     # Seed the random number generator
#     # np.random.seed(42)
    
#     # # Initialize random numbers: random_numbers
#     # random_numbers = np.empty(100000)
    
#     # # Generate random numbers by looping over range(100000)
#     # for i in range(100000):
#     #     random_numbers[i] = np.random.random()
#     #     print(np.random.get_state()[2], np.random.get_state()[3], np.random.get_state()[4])
    

    
#     # # priors = pr.Priors(len_prior=min_src, nbo=nbo, bmin=0, bmax=100)
#     # # prc = priors.rand_percent()
#     # # prior = priors.rand_prior(prc)
#     # prior=[0.1,0.2,0.3,0.4,0.5]
    
#     # #print(f"#{vote} {norma} - {typeg}")
    
#     # rg = randomGraph(vote, para, nbo=nbo, nbfl=nbfl, nbfu=nbfu, nbs=nbs, 
#     #                   norma=norma, prior=prior, typeg=typeg, min_fs=1)
#     # print(rg.G)
#     # print(rg.prior_src)
#     # print(rg.posteriori_trust)
#     # # G = rg.G
#     # print(G)
#     # print(G.to_file())
#     #G.run()
    
#     #print(G.str_rank_sources())
#     #print(G.obj.str_object())
    
#     #print(G.to_file())
    
#     # print("Results :\n")
#     # print(G.str_trust())
#     # print(G.str_rank_sources())
#     # print(G.obj.str_rank_facts())
    
#     #print(G.str_rank_sources())
    
#     #print(G.obj.str_object())
    
#     #print(rg.posteriori)
    
#     #print(rg.G.get_rank_sources_name(True))
    
#     #for i in range(len(G.obj.of)):
#         #print([n.id for n in G.obj.get_best_facts(i)])
    