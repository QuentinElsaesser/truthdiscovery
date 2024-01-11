from v4.constants import constants

from v4.graph import graph
from v4.graph import derive
from v4.graph import prio

from v4.vote import plurality as maj
from v4.vote import borda as bor

from v4.other_methods import sums, usums, hna, truthfinder, voting_majo, averagelog, pooledinvestment, investment

from v4.examples import read_file as rf

from v4.tests_datasets import att_datasets as ad

from copy import deepcopy

import numpy as np

import sys

class MethodsDatasets:
    def __init__(self, name_dataset, truth_obj, truth_f, long):
        """
        truth_obj : the index of all the true object
        truth_f : list the id of the true facts
        """
        print(f"Dataset : {name_dataset}")
        self.rgs = []
        self.metrics = []
        
        if long:
            mat_fs, mat_of = rf.read_file_long(name_dataset)
        else:
            mat_fs, mat_of, _ = rf.read_file(name_dataset)
        
        #compute truth fct with truth_of
        truth_fct=[0 for i in range(len(mat_fs))]
        for i in range(len(truth_f)):
            truth_fct[truth_f[i]-1] = 1

        print("Building graph")

        G = graph.Graph(mat_fs, mat_of, maj.Plurality, 1, constants.NORMA_A, len(mat_fs[0]), len(mat_fs), truth=truth_fct, long=long)
        tmpG = deepcopy(G)
    
        print("Graph done. Creation of methods :")
    
        self.rgs.append(deepcopy(G))
        self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        print("PLA done")
        
        # tmp = deepcopy(G)
        # tmp.change_norma(constants.NORMA_O)
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("PLO done")
        
        # G.change_vote(bor.Borda, 1)
        # self.rgs.append(deepcopy(G))
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("BoA done")
        
        # tmp = deepcopy(G)
        # tmp.change_norma(constants.NORMA_O)
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("BoO done")
        
        # tmp = derive.Derive(G=deepcopy(tmpG), voting_met=maj.Plurality, vote_para=1, name_norma=constants.NORMA_A)
        # tmp.max_it = 100000
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("DrvA done")
        
        ##tmp = derive.Derive(G=deepcopy(G), voting_met=maj.Plurality, vote_para=1, name_norma=constants.NORMA_O)
        #tmp = deepcopy(self.rgs[-1])
        #tmp.max_it = 1000
        #tmp.change_norma(constants.NORMA_O)
        #self.rgs.append(tmp)
        #self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        #print("DrvO done")
        
        #tmp = prio.Prio(G=deepcopy(tmpG), voting_met=maj.Plurality, vote_para=1, name_norma=constants.NORMA_A)
        #self.rgs.append(tmp)
        #self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        #print("PioA done")
        
        ##tmp = prio.Prio(G=deepcopy(G), voting_met=maj.Plurality, vote_para=1, name_norma=constants.NORMA_O)
        #tmp = deepcopy(self.rgs[-1])
        #tmp.change_norma(constants.NORMA_O)
        #self.rgs.append(tmp)
        #self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        #print("PioO done")
        
        # tmp = hna.Hna(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("H&A done")
        
        # tmp = sums.Sums(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("Sums done")
        
        # tmp = usums.Usums(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("USums done")
        
        # tmp = truthfinder.Truthfinder(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("TF done")
        
        # tmp = averagelog.AverageLog(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("AverageLog done")
        
        # tmp = investment.Investment(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("Investment done")
        
        # tmp = pooledinvestment.PooledInvestment(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("PooledInvestment done")
        
        # tmp = voting_majo.VotingMajo(deepcopy(G))
        # self.rgs.append(tmp)
        # self.metrics.append(ad.AttDatasets(G=self.rgs[-1], truth_obj=truth_obj))
        # print("Voting done")
        
        print(f"Creation of the {len(self.rgs)} methods done")
        
        for i in range(len(self.rgs)):
            self.rgs[i].run_noprint()
            self.metrics[i].run_all()
            if isinstance(self.rgs[i], graph.Graph):
                print(self.rgs[i].obj.voting_met, self.rgs[i].normalizer.name)
                # print(self.rgs[i].obj.str_trust_f())
            else:
                print(self.rgs[i])
                # print(self.rgs[i].G.obj.str_trust_f())
            print(self.metrics[i])
            
        print("Run done\n")
        
    def comp_src_surUN(self, ind, l):
        if len(l) == 0:
            return False
        
        G = self.rgs[ind]
        src = [l[i][1]/20 for i in range(len(l))]
        #print("PB ARRONDI ?", src)
        self.metrics[ind].compute_diff(G.trust_s, src)
        
        print(f"Trust Moyenne : {np.mean(G.trust_s)} et Note moyenne : {np.mean(src)}")
        print("\nDiff globale (/1): ", self.metrics[ind].diff)
        
        print("trust - note = difference (/1)")
        for i in range(len(G.trust_s)):
            tmp1 = round(G.trust_s[i], 2)
            tmp2 = round(src[i],2)
            print(f"src{i} {tmp1} - {tmp2} = {round(self.metrics[ind].diff_src[i],2)}")
        
    def comp_src(self, ind, l):
        if len(l) == 0:
            return False
 
        self.metrics[ind].diff_src = []
        G = self.rgs[ind]
        src = [l[i][1] for i in range(len(l))]
        #print("PB ARRONDI ?", src)
        trust_20 = [n*20 for n in G.trust_s]
        self.metrics[ind].compute_diff(trust_20, src)
        
        print(f"Trust Moyenne : {np.mean(trust_20)} et Note moyenne : {np.mean(src)}")
        print("\nDiff globale (/20): ", self.metrics[ind].diff)
        
        print("trust - note = difference (/20)")
        for i in range(len(G.trust_s)):
            tmp1 = round(G.trust_s[i]*20, 2)
            tmp2 = round(src[i],2)
            print(f"src{i} {tmp1} - {tmp2} = {round(self.metrics[ind].diff_src[i],2)}")
        
if __name__ == "__main__":
    # dataset = "book"
    dataset = "flight"
    # dataset = "qcm"
    # dataset = "qcm_10"
    # dataset = "qcm_noneg"
    
    s = []
    
    if dataset == "book":
        name = "dataset/book/books_format.txt"
        f = open("dataset/book/books_format_tf.txt", "r")
        long=False
    elif dataset == "flight":
        name = "dataset/flight/flight_format.txt"
        f = open("dataset/flight/flight_format_tf.txt", "r")
        long=True
    elif "qcm" in dataset:
        # typeq = "qcm"
        # typeq = "qcm_but"
        typeq = sys.argv[1]
        
        # n = ""
        # n = "_noneg"
        # n = "_10"
        # n = "_1013"
        # n = "_9"
        if len(sys.argv) >= 3:
            n = sys.argv[2]
        else:
            n = ""
        
        name = f"dataset/{typeq}/qcm{n}.txt"
        print(f"location dataset : {name}")
        f = open(f"dataset/{typeq}/qcm_tf{n}.txt", "r")
        fsrc = open(f"dataset/{typeq}/qcm_src{n}.txt", "r")
        
        long=False
        s = fsrc.read()
        s = s.split("/")
        s = [n.split("-") for n in s]
        s = [(n[0], float(n[1])) for n in s]
        fsrc.close()
    

    tmp = f.read()
    tmp = tmp.split("/")
    tmp = [n.split(",") for n in tmp]
    #stock the id of facts and objects
    true_of = [(int(n[0]), int(n[1])) for n in tmp]
    tf = [n[1] for n in true_of]
    truth_obj = [n[0] for n in true_of]
    
    f.close()
    
    g = MethodsDatasets(name_dataset=name, truth_obj=truth_obj, truth_f=tf, long=long)
    
    # g.comp_src_surUN(0, s)
    g.comp_src(0, s)
    
    print(g.rgs[0].str_trust())
    
    print("Nombre de questions : ", len(g.rgs[0].mat_of))
    
    
    
