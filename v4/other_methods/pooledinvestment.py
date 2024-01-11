import numpy as np
from numpy.linalg import norm

class PooledInvestment:
    def __init__(self, G):
        # C_s = Claim affrimé par la source s
        # S_c = Source qui affirme c
        # S_d = Source qui affirme les claim du Mutual ex set M_c
        # M_c = Mutual ex set du claim c (c est dans le mut ex set !)
        # C_r = Claim affirmé par la source r
        self.init_trust = 1.0
        self.g = 1.4
        # self.gx = lambda x : x**self.g
        
        self.mem_fact = []
        
        self.G = G
        
        self.dobj = dict()
        for i in range(len(self.G.mat_fs)):
            self.dobj[i] = self.G.obj.get_obj(i)
        
        # nb fois qu'une source claim des faits
        self.srcbyfct = [0 for n in self.G.sf]
        for i in range(len(self.G.sf)):
            self.srcbyfct[i] = np.count_nonzero(self.G.sf[i] == 1)
    
        # a fact is in conflict only with the facts in the same object
        tmp_trust = []
        length = len(self.G.mat_fs)
        for i in range(length):
            # print(f"{i}l{len(self.G.mat_fs)}")
            ind = self.dobj[i]
            tmp_trust.append(1/(self.G.obj.of[ind].nb_prec))

        self.G.reset_graph([self.init_trust for i in range(len(self.G.mat_fs[0]))])
        self.G.trust_f = tmp_trust
        self.G.obj.update_trust(self.G.trust_f)
        self.mem_fact = tmp_trust
        
    def trust_sources(self):
        """
        Compute the trust for the sources
        """
        tmp_trust_s = [0 for i in self.G.trust_s]
        for i in range(len(self.G.trust_s)):
            tmpsum = 0
            for j in range(len(self.G.mat_fs)):
                if self.G.mat_fs[j][i] == 1:
                    bc = self.mem_fact[j]
                    ts = self.G.mem[0][i]
                    cs = self.srcbyfct[i]
                    tmpsum2 = 0
                    for r in range(len(self.G.sf)):
                        if self.G.sf[r][j] == 1:
                            cr = self.srcbyfct[r]
                            tmpsum2 += (self.G.mem[0][r]/cr)
                    if tmpsum2 == 0 or cs == 0:
                        tmpsum += 0
                    else:
                        tmpsum += bc * (ts/(cs * tmpsum2))
            tmp_trust_s[i] = tmpsum
        self.G.trust_s = tmp_trust_s
        
    def trust_fact(self):
        """
        Compute the trust for the facts
        """
        tmp_trust_f = [0 for i in self.G.trust_f]
        hc = []
        for i in range(len(self.G.trust_f)):
            hctmp = 0
            for j in range(len(self.G.sf)):
                if self.G.sf[j][i] == 1:
                    cs = self.srcbyfct[j]
                    hctmp += (self.G.trust_s[j] / cs)
            hc.append(hctmp)
        
        for i in range(len(self.G.trust_f)):
            ind = self.dobj[i]
            tmpsum = 0
            for n in self.G.obj.of[ind].prec:
                tmpsum += hc[n.ind]**self.g #self.gx(hc[n.ind])
            if tmpsum == 0:
                tmp_trust_f[i] = 0
            else:
                tmp_trust_f[i] = hc[i] * ((hc[i]**self.g) / tmpsum)
                #tmp_trust_f[i] = hc[i] * (self.gx(hc[i]) / tmpsum)
        self.G.trust_f = tmp_trust_f
        
    def convergence(self):
        if self.G.iteration >= 20:
            return True
        return False
        # if len(self.G.mem) < 2:
        # # if self.G.iteration < 2:
        #     return False
        # if self.G.iteration > 100:
        #     print("Infinite Loop / Bug")
        #     print("Unknown error")
        #     print(f"Method : {self.G.obj.voting_met} - {self.G.normalizer.name}")
        #     print(self.G)
        #     print(self.G.str_trust())
        #     print("\nGraph links :")
        #     print(self.G.to_file())
        #     return True
        # old = self.G.mem[1]
        # current = self.G.mem[0]
        # if sum(old) == 0 or sum(current) == 0:
        #     print("Infinite Loop / Bug")
        #     print("Trust of all elements is null, no facts claimed")
        #     print(f"Method : {self.G.obj.voting_met} - {self.G.normalizer.name}")
        #     print(self.G)
        #     print(self.G.str_trust())
        #     print("\nGraph links :")
        #     print(self.G.to_file())
        #     return True
        
        # cos_sim = np.dot(current, old) / (norm(current)*norm(old))
        # epsilon = 0.001
        # if 1-cos_sim <= epsilon:
        #     return True
        # return False
        
    def run(self):
        """
        Normalized by the max (same as Sums)
        """
        maxi = 0
        print(self.G.str_trust())
        while not self.convergence():
            self.G.iteration += 1
            
            self.mem_fact = self.G.trust_f
            
            self.trust_fact()
            maxi = max(self.G.trust_f)
            for i in range(len(self.G.trust_f)):
                if maxi == 0:
                    self.G.trust_f[i] = 0
                else:
                    self.G.trust_f[i] /= maxi
            self.G.obj.update_trust(self.G.trust_f)
            
            self.trust_sources()
            maxi = max(self.G.trust_s)
            for i in range(len(self.G.trust_s)):
                if maxi == 0:
                    self.G.trust_s[i] = 0
                else:
                    self.G.trust_s[i] /= maxi
                
            self.G.update_mem()
            print(self.G.str_trust())
            
    def run_noprint(self):
        maxi = 0
        while not self.convergence():
            self.G.iteration += 1
            
            self.mem_fact = self.G.trust_f
            
            self.trust_fact()
            maxi = max(self.G.trust_f)
            for i in range(len(self.G.trust_f)):
                self.G.trust_f[i] /= maxi
            self.G.obj.update_trust(self.G.trust_f)
            
            self.trust_sources()
            maxi = max(self.G.trust_s)
            for i in range(len(self.G.trust_s)):
                self.G.trust_s[i] /= maxi
                
            self.G.update_mem()
