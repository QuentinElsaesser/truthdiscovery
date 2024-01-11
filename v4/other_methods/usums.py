import numpy as np 

class Usums:
    def __init__(self, G):
        self.init_trust = 1.0
        
        self.G = G
        self.G.reset_graph([self.init_trust for i in range(len(self.G.mat_fs[0]))])
        
        tmp_trust = []
        length = len(self.G.mat_fs)
        for i in range(length):
            tmp_trust.append(np.count_nonzero(self.G.mat_fs[i]) == 1)
        
        self.G.trust_f = tmp_trust
        self.G.obj.update_trust(self.G.trust_f)
        
    def trust_sources(self):
        """
        Compute the trust for the sources
        """
        tmp_trust_s = [0 for i in self.G.trust_s]
        for i in range(len(self.G.trust_s)):
            tmp_trust_s[i] = sum(self.G.sf[i]*self.G.trust_f)
        self.G.trust_s = tmp_trust_s

    def trust_fact(self):
        """
        Compute the trust for the facts
        """
        tmp_trust_f = [0 for i in self.G.trust_f]
        for i in range(len(self.G.trust_f)):
            tmp_trust_f[i] = sum(self.G.mat_fs[i]*self.G.trust_s)
        self.G.trust_f = tmp_trust_f
        
    def convergence(self):
        # if len(self.G.mem) < 2:
        if self.G.iteration < 2:
            return False
        if self.G.iteration > 1000:
            print("Boucle infinie - USums")
            return True
        rank_current = sorted(zip(self.G.mem[0], np.arange(1,len(self.G.mem[0])+1)), reverse=True)
        rank_old = sorted(zip(self.G.mem[1], np.arange(1,len(self.G.mem[1])+1)), reverse=True)
        
        for i in range(len(rank_current)):
            if rank_current[i][1] != rank_old[i][1]:
                return False
        return True

    def run(self):
        print(self.G.str_trust())
        while not self.convergence():
            self.G.iteration += 1
            
            self.trust_fact()
            self.G.obj.update_trust(self.G.trust_f)
            
            self.trust_sources()
                
            self.G.update_mem()
            print(self.G.str_trust())
            
            
    def run_noprint(self):
        while not self.convergence():
            self.G.iteration += 1
            
            self.trust_fact()
            self.G.obj.update_trust(self.G.trust_f)
            
            self.trust_sources()
                
            self.G.update_mem()

            
