import numpy as np
from numpy.linalg import norm

# import math

class Truthfinder:
    def __init__(self, G):
        self.init_trust = 0.9
        self.similarityConstant = 0.5 # Rho (p) in article
        self.base_sim = 0.5 
        self.dampingFactor = 0.3 # Gamma (y) in article
        
        self.G = G
        #t(w)
        self.G.reset_graph([self.init_trust for i in range(len(self.G.mat_fs[0]))])
        
        #self.confidence_score = [0 for n in self.G.trust_f]
        #R
        self.trustworthiness_score = [-np.log(1-self.G.trust_s[i]) for i in range(len(self.G.trust_s))]
        
        #Compute matrices A and B
        self.A = []
        for i in range(len(self.G.sf)):
            self.A.append([])
            for j in range(len(self.G.mat_fs)):
                if self.G.mat_fs[j][i] == 1:
                    self.A[i].append(1/(np.count_nonzero(np.array(self.G.sf[i]) == 1)))
                else:
                    self.A[i].append(0)
            
        self.B = []
        for j in range(len(self.G.mat_fs)):
            self.B.append([])
            for i in range(len(self.G.sf)):
                if self.G.mat_fs[j][i] == 1:
                    self.B[j].append(1)
                else:
                    #case where wi provide fk and o(fk) = o(fj) because imp(f,f)=0 no matter what in our case 
                    self.B[j].append(0)
        
        self.adjusted_matrix = []
        self.confidence = []
            
    def update_fact_score_matrix(self):
            self.adjusted_matrix = np.array(np.array(self.B) @ np.array(self.trustworthiness_score))
            self.confidence = np.array([(1/(1+np.exp(-self.dampingFactor * self.adjusted_matrix[i]))) for i in range(len(self.adjusted_matrix))])
            self.G.trust_f = list(self.confidence)
            self.G.obj.update_trust(self.G.trust_f)
            
    def update_src_score_matrix(self):
        self.G.trust_s = np.array(np.array(self.A) @ np.array(self.confidence))
        for s in self.G.trust_s:
            if s >= 1:
                #print("Trust become 1 for at least one source")
                #print(self.G.to_file())
                return True
        self.trustworthiness_score = np.array([-np.log(1-self.G.trust_s[i]) for i in range(len(self.G.trust_s))])
            
    def compute_similarity(self, f1, f2):
        """
        f1, f2 : facts index
        """
        return 0.0
                        
    def run(self):
        print(self.G.str_trust())
        while not self.convergence():
            self.G.iteration += 1
            self.update_fact_score_matrix()
            self.update_src_score_matrix()
            self.G.update_mem()
            print(self.G.str_trust())
        
    def run_noprint(self):
        while not self.convergence():
            self.G.iteration += 1
            self.update_fact_score_matrix()
            self.update_src_score_matrix()
            self.G.update_mem()
    
    def convergence(self):
        """
        Check the convergence of the cosine similarity
        """
        if self.G.iteration < 2:
        # if len(self.G.mem) < 2:
            return False
        if self.G.iteration > 100:
            print("Infinite Loop / Bug")
            print("Unknown error")
            print(f"Method : TruthFinder - {self.G.obj.voting_met} - {self.G.normalizer.name}")
            print(self.G)
            print(self.G.str_trust())
            print("\nGraph links :")
            print(self.G.to_file())
            return True
        old = self.G.mem[1]
        current = self.G.mem[0]
        if sum(old) == 0 or sum(current) == 0:
            print("Infinite Loop / Bug")
            print("Trust of all elements is null, no facts claimed")
            print(f"Method : TruthFinder - {self.G.obj.voting_met} - {self.G.normalizer.name}")
            print(self.G)
            print(self.G.str_trust())
            print("\nGraph links :")
            print(self.G.to_file())
            return True
        
        for s in self.G.trust_s:
            if s >= 1:
                #print("Trust become 1 for at least one source")
                #print(self.G.to_file())
                return True
        
        cos_sim = np.dot(current, old) / (norm(current)*norm(old))
        epsilon = 0.001
        if 1-cos_sim <= epsilon:
            return True
        return False
   