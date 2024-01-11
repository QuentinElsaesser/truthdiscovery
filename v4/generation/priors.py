import itertools, random, os

from v4.constants import constants

class Priors:
    def __init__(self, len_prior, nbo=10, bmin=0, bmax=100, limit=[]):
        """
        len_prior : minimum number of sources
        bornemin - bornemax : the min/max percentage we generate
        """
        self.directory = constants.PRIOR_PATH
        self.nbo = nbo
        self.bornemin = bmin
        self.bornemax = bmax
        self.limit = limit
        self.len_prior = len_prior
        self.name = f"{self.directory}prior{self.nbo}-{self.len_prior}.csv"
        self.priors = dict()
        self.percent = []
        
        read = self.read()
        
        if not read:
            priors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            for p in list(itertools.combinations_with_replacement(priors, len_prior)):
                self.add_dict(p)
            self.percent = sorted(list(self.priors.keys()))
            
    def rand_percent(self):
        return self.percent[random.randint(0, len(self.percent)-1)]
    
    def rand_prior(self, prc):
        return self.priors[prc][random.randint(0, len(self.priors[prc])-1)]
        
    def min_maj(self, prior):
        """
        percentage we have depending on the prior and the number of object
        """
        link = 0
        total = 0
        for p in prior:
            link += p
            total += 1
        tmp = link/total
        return round(tmp*100)
    
    def cond(self, tmp):
        return len(self.limit) == 0 or tmp in self.limit
    
    def add_dict(self, e):
        """
        add in dict
        e : prior
        """
        srtd = sorted(e)
        tmp = self.min_maj(e)
        if self.cond(tmp) and self.bornemin <= tmp <= self.bornemax:
            if tmp in self.priors:
                if srtd not in self.priors[tmp]:
                    self.priors[tmp].append(srtd)
            else:
                self.priors[tmp] = [srtd]
                
    def create_file(self):
        if os.path.isfile(self.name):
            return True
        f = open(self.name, "w")
        print(f"Create file {self.name}")
        f.close()
        return True
    
    def prior_to_str(self, p):
        s = ""
        for n in p:
            s += f"{n};"
        return s[:-1]
    
    def str_to_prior(self, s):
        p = [float(n) for n in s.split(";")]
        return p[1:]
    
    def write(self, rewrite=False):
        if not rewrite and os.path.isfile(self.name):
            return True
        if not os.path.isfile(self.name):
            self.create_file()
        f = open(self.name, "w")
        for prc in self.percent:
            for p in self.priors[prc]:
                s = f"{prc};{self.prior_to_str(p)}\n"
                f.write(s)
        f.close()
        return True
        
    def read(self):
        if os.path.isfile(self.name):
            f = open(self.name, "r")
            lines = f.readlines()
            for l in lines:
                prior = self.str_to_prior(l)
                self.add_dict(prior)
            f.close()
            self.percent = sorted(list(self.priors.keys()))
            return True
        return False
        
                
# if __name__ == "__main__":
    
#     #l=[]
#     #limits = Priors(len_prior=5, nbo=10)
#     #l = limits.percent
#     l=[]
    
#     len_prior = 20
#     nbo=10
#     priors = Priors(len_prior=len_prior, nbo=nbo, limit=l)
#     priors.write(rewrite=True)
    
#     # v = [0.1, 0.1, 0.5, 0.6, 0.9]
#     # v = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2]
#     # tmp = 0
#     # nbo = 5
#     # tt = 0
    
#     # for i in range(len(v)):
#     #     tmp += v[i]
#     #     tt += nbo
#     # ttt = tt/10
    
#     # print(tmp, tt, ttt, (tmp/ttt))
#     # print(tmp/len(v) * 100)
#     # print(limits.min_maj(v))
    
#     # t = [0.2, 0.35, 0.35, 0.35, 0.75, 0.55, 0.6499999999999999, 0.6499999999999999, 0.6499999999999999, 0.7]
#     # p = [0.2, 0.2, 0.3, 0.3, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7]
    
#     # tmp = 0
#     # for i in range(len(t)):
#     #     tmp += abs(p[i] - t[i])
        
#     # print(tmp/len(t))
        
#     # priors2 = Priors(len_prior=20, nbo=10, limit=priors.percent)
#     # print(priors2.percent)
    
#     # a = 5
#     # b = 5
#     # tmp = [i for i in range(a)]
#     # if a == b:
#     #     print(tmp)
#     # else:
#     #     print(sorted(list(np.random.choice(tmp, size=b, replace=False, p=None))))
    
    