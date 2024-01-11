from v4.graph import graph

from copy import deepcopy

from operator import itemgetter
from itertools import groupby

import numpy as np

class AttMetrics:
    def __init__(self, rg, interp):
        """
        rg = random graph
        interp = interpretations
        """
        self.rg = rg
        
        self.G = rg.G if isinstance(rg.G, graph.Graph) else rg.G.G
        
        self.nbs = len(self.G.trust_s)
        
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        
        self.recall = 0
        self.accuracy = 0
        self.precision = 0
        self.csi = 0
        
        self.swap = 0
        self.swap_max = 0
        self.swap1 = False
        self.swap2 = False
        
        self.euclidean_d = 0
        self.euclidean_d_max = 0
        
        self.difference = 0
        self.diffbysrc = [0 for s in range(self.nbs)]
        
        self.interp = interp
        self.consistent_f = 0

        self.iteration = self.G.iteration
        
        self.posteriori = deepcopy(self.rg.posteriori)
        
        self.posteriori.sort(reverse=True, key=itemgetter(1))
        groups = groupby(self.posteriori, itemgetter(1))
        self.posteriori = [[item[0] for item in data] for (key, data) in groups]
        
        #order with the trust
        self.ordre = self.G.get_rank_sources_name(True)
        # fact that won the vote
        self.best_f = []
        
    def gen_cpl_in(self, e, lst):
        """
        couple where e in lst
        """
        res = []
        for elt in lst:
            if e != elt:
                res.append((e,elt))
        return res

    def gen_cpl_out(self, e, lst):
        """
        couple where e not in lst
        """
        res = []
        for l in lst:
            for elt in l:
                res.append((e,elt))
        return res
        
    def gen_couple(self, lst):
        """
        generate every couple
        """
        res = []
        for i in range(len(lst)):
            l = lst[i]
            for e in l:
                res.extend(self.gen_cpl_in(e, l))
                res.extend(self.gen_cpl_out(e, lst[i+1:]))            
        return res

    def nb_swap2(self, lt, lp):
        """
        compute number of swaps when order is not strict
        [1,2] > [4,3] & 1 > 2 > 3 > 4 => 2
        [1,2] > [4,3] & 4 > 1 > 2 > 3 => 6
        """
        self.swap2 = True
        cpllt = self.gen_couple(lt)
        cpllp = self.gen_couple(lp)
        diff = set(cpllt).symmetric_difference(set(cpllp))
        return len(diff)
            
    def min_swap(self, lst, n):
        arrPos = [[0 for x in range(2)] for y in range(n)]
        for i in range(n):
            arrPos[i][0] = lst[i]
            arrPos[i][1] = i
        arrPos.sort()
    
        visited = [False] * (n)
        res = 0
        for i in range(n):
            if (visited[i] or arrPos[i][1] == i):
                continue
            cycle_size = 0
            j = i
            while (not visited[j]):	
                visited[j] = 1
                j = arrPos[j][1]
                cycle_size += 1
            res += (cycle_size - 1)
        return res
    
    def nb_swap1(self, lt, lp):
        """
        nb swap with strict order
        lt, lp same length
        """
        self.swap1 = True
        mp = {}
        for i in range(len(lt)):
            mp[lp[i]] = i
        #stock in lp the index where the element should be
        for i in range(len(lt)):
            lp[i] = mp[lt[i]]
        return self.min_swap(lp, len(lt))
    
    def nb_swap(self, lt, lp):
        """
        call the function
        """
        if len(lt) != self.nbs or len(lp) != self.nbs:
            return self.nb_swap2(lt, lp)
        return self.nb_swap1(list(np.array(lt).flatten()), list(np.array(lp).flatten()))
        
    def compute_swaps(self):
        """
        compute the nb swap between the trust (ordre) ranking and the a posteriori ranking
        
        if strict order -> swap
        else smt close to kendall rank
        """
        lt = deepcopy(self.ordre)
        lp = deepcopy(self.posteriori)
        
        self.swap = self.nb_swap(lt, lp)
        # self.swap_max = ((self.nbs-1) * self.nbs) / 2
        self.swap_max = ((self.nbs-1) * self.nbs)
        
    def compute_truth(self):
        for i in range(len(self.G.obj.of)):
            best = self.G.obj.get_best_fact(i)
            for f in self.G.obj.of[i].prec:
                if f in best:
                    if f.is_true:
                        self.TP += 1
                    else:
                        self.FP += 1
                else:
                    if f.is_true:
                        self.FN += 1
                    else:
                        self.TN += 1
    
    def compute_metrics(self):
        tmp = (self.TP+self.FP)
        self.precision = self.TP / tmp

        tmp = self.TP + self.FN + self.FP
        self.csi = (self.TP / tmp)

        tmp = (self.TP+self.FP+self.TN+self.FN)
        self.accuracy = (self.TP+self.TN) / tmp
        
        tmp = (self.TP+self.FN)
        if tmp > 0:
            self.recall = self.TP / tmp
            
    def consistent(self):
        if self.interp != None:
            self.best_f = [n.ind for n in self.G.obj.get_best_facts()]
            self.consistent_f = int(self.best_f in self.interp)
            
    def compute_euclidean_distance(self):
        post = np.array(self.rg.posteriori_trust)
        trust = np.array(self.G.trust_s)
        self.euclidean_d = round(np.sqrt(np.sum(np.square(post-trust))),3)
        m = []
        for t in trust:
            if t < 0.5:
                m.append(1-t)
            else:
                m.append(t)
        m = np.array(m)
        zeros = np.zeros(self.rg.nbs)
        self.euclidean_d_max = round(np.sqrt(np.sum(np.square(zeros-m))),3)
        
    def compute_difference(self):
        for i in range(self.rg.nbs):    
            self.difference += abs(self.G.trust_s[i] - self.rg.posteriori_trust[i])
            self.diffbysrc[i] = abs(self.G.trust_s[i] - self.rg.posteriori_trust[i])
        self.difference /= self.rg.nbs
        
    def run_all(self):
        """
        run all the metrics
        """
        self.compute_swaps()
        self.compute_euclidean_distance()
        self.compute_difference()
        self.compute_truth()
        self.compute_metrics()
        # self.consistent()
    