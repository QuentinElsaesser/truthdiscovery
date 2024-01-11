from v4.constants import constants

import numpy as np

class SpeMetrics:
    def __init__(self, experience):
        """
        Special metric for the sources
        Generate the latex tabular
        """
        self.exp = experience
        self.exp.spe_metric = self
        
        self.nb_methods = constants.NB_METHODS
        
        self.nbs = self.exp.nbs
        # self.maxs = self.exp.nbs if self.exp.nbs <= 15 else 15
        self.maxs = self.exp.nbs
        
        self.trust = [[0 for i in range(self.nbs)] for j in range(self.nb_methods)]
        self.proba = [[0 for i in range(self.nbs)] for j in range(self.nb_methods)]
        
        #start 1 bc it's the max for a source
        self.mintrust = [[1 for i in range(self.nbs)] for j in range(self.nb_methods)]
        self.minproba = [[1 for i in range(self.nbs)] for j in range(self.nb_methods)]
        
        self.maxtrust = [[0 for i in range(self.nbs)] for j in range(self.nb_methods)]
        self.maxproba = [[0 for i in range(self.nbs)] for j in range(self.nb_methods)]
        
        self.sources = []
        
        self.difference = [0 for j in range(self.nb_methods)]
        
        self.compute_result()
        
    def compute_result(self):
        """
        Compute the average reliability computed by the algorithm
        and the a posteriori probability for every sources
        """
        #Sum the trust and proba of the 1000 graphs
        for g in self.exp.graphes:
            for i in range(self.nb_methods):
                if i in constants.ID_METHODS_SOURCES:
                    tmp = 0
                    for j in range(self.nbs):
                        
                        trust = g.rgs[i].metric_att.G.trust_s[j]
                        posteriori = g.rgs[i].metric_att.rg.posteriori_trust[j]
                        
                        self.trust[i][j] += trust
                        self.proba[i][j] += posteriori
                        
                        # G = g.rgs[i].G if isinstance(g.rgs[i].G, graph.Graph) else g.rgs[i].G.G
                        
                        # self.trust[i][j] += G.trust_s[j]
                        # self.proba[i][j] += g.rgs[i].posteriori_trust[j]
                        
                        # self.difference[i] += g.rgs[i].metric_att.difference
                        
                        tmp += abs(trust - posteriori)
                        
                        if trust < self.mintrust[i][j]:
                            self.mintrust[i][j] = trust
                        if trust > self.maxtrust[i][j]:
                            self.maxtrust[i][j] = trust
                            
                        if posteriori < self.minproba[i][j]:
                            self.minproba[i][j] = posteriori
                        if posteriori > self.maxproba[i][j]:
                            self.maxproba[i][j] = posteriori                
                    self.difference[i] += (tmp / self.nbs)
            
        #Compute average of trust and proba
        for i in range(self.nb_methods):
            for j in range(self.nbs):
                self.trust[i][j] /= self.exp.nb_exp
                self.proba[i][j] /= self.exp.nb_exp
                
        for i in range(self.nb_methods):
            self.difference[i] /= self.exp.nb_exp
    
    def generate_latex_body(self):
        """
        stock header in head
        stock each line with the data in tmpn
        """
        tmp = ""
        c = False
        #complete
        # tex = [f"s{i+1} &" for i in range(self.nbs)]
        #non complete
        head = ["" for n in range(self.nb_methods)]
        tmpn = [[f"s{i+1} &" for i in range(self.nbs)] for n in range(self.nb_methods)]
        for i in range(self.nb_methods):
            #graph complet
            if self.exp.typeg.startswith('c'):
                c = True
                met = self.exp.graphes[0].names_nonorma[i]
            else:
                met = constants.ORDER[i]
                
            self.sources = self.indice_sources(i)
            # print(f"{met}-{self.nbs}-{self.exp.typeg} Methode{i} : {self.trust[i]}")
            # print(f"{met}-{self.nbs}-{self.exp.typeg} Methode{i} : {self.proba[i]}\n")
            head[i] += f"\\noindent Results for {met} with {self.nbs} sources graph {self.exp.typeg}.\n\n"
            head[i] += "\\noindent\\begin{tabular}{|l|c|c|c|c|c|c|}\n"
            head[i] += f"\\hline\n$s$& Probability min & {met} min & Probability & {met} - $\\ts{{s}}$ & Probability max & {met} max\\\\\n\\hline\n"
            for j in self.sources:
                tmpn[i][j] += f"{round(self.minproba[i][j],2)} & {round(self.mintrust[i][j],3)} & {round(self.proba[i][j],2)} & {round(self.trust[i][j],3)} & {round(self.maxproba[i][j],2)} & {round(self.maxtrust[i][j],3)}\\\\\n"

        for j in range(len(head)):
            if j in constants.ID_METHODS_SOURCES:
                if c:
                    if j != 2 and j != 3:
                        tmp += head[j]
                        for i in range(len(tmpn[j])):
                            tmp += f"{tmpn[j][i]}\\hline\n"
                        tmp += "\\end{tabular}\\\\\n\n"
                else:
                    tmp += head[j]
                    for i in range(len(tmpn[j])):
                        tmp += f"{tmpn[j][i]}\\hline\n"
                    tmp += "\\end{tabular}\\\\\n\n"
        # print(tmp)
        return tmp
    
    def indice_sources(self, i):
        if len(self.sources) > 0:
            return self.sources
        tmp = [i for i in range(len(self.trust[i]))]
        if len(self.trust[i]) == self.maxs:
            return tmp
        else:
            return sorted(list(np.random.choice(tmp, size=self.maxs, replace=False, p=None)))
    
    
    
    