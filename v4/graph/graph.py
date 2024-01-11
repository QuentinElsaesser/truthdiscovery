import numpy as np
# from numpy.linalg import norm

from operator import itemgetter
from itertools import groupby

from v4.vote import normalize as nm

from v4.graph import obj

from scipy.spatial import distance

from copy import deepcopy

class Graph:
    def __init__(self, mat_fs, mat_of, voting_met, vote_para, name_norma, nb_s, nb_f, init_trust=1,truth=[],normalizer=None,trust_s=None,trust_f=None,long=False,gobj=None,sf=None):
        """
        mat_fs : Adjacency matrix where mat_fs[0] (type np.array) is the vector of sources that claimed fact index 0 
        (ex = [np.array([0,1,0]), np.array([1,0,0]), np.array([1,0,0]), np.array([0,1,0]), np.array([1,1,1])])
        mat_of : Adjacency matrix where mat_of[0] (type np.array) is the vector of facts linked to object index 0 
        (ex = [np.array([1,1,1,0,0]), np.array([0,0,0,1,1])])
        voting_met : voting method chosen
        vote_para : parameters linked to the voting method chosen
        nb_s : number of sources
        nb_f : number of facts
        init_trust : initial trust
        truth : the true facts
        normalizer : if a normalizer if already used
        trust_s : vector of trust for the sources (vector a priori if not None)
        trust_f : vector of trust for the facts (vector a priori if not None)
        long : if it is a huge flle (big dataset like flight)
        
        
        _____
        np.count_nonzero(sublist == 1)
        """
        self.long = long
        self.iteration = 0
        self.max_it = 30
        self.voting_met = voting_met
        self.vote_para = vote_para
        self.mat_fs = mat_fs
        self.mat_of = mat_of
        self.init_trust = init_trust
        self.trust_s = [self.init_trust for i in range(nb_s)] if trust_s == None else trust_s
        self.trust_f = [0 for i in range(nb_f)] if trust_f == None else trust_f
        self.mem = [self.trust_s.copy()]
        
        if gobj == None:
            self.obj = obj.Obj(len(mat_of), self.voting_met, self.vote_para)
            if self.long:
                self.obj.add_nodes_long(mat_of, mat_fs)
            else:
                self.obj.add_nodes(mat_of, mat_fs)
            self.obj.update_voting_parameters()
            self.obj.update_truth(truth)
        else:
            self.obj = gobj
            
        if sf == None:
            self.sf = []
            self.gen_sf()
        else:
            self.sf = sf
            
        if normalizer != None:
            self.normalizer = normalizer(name_norma)
        else:
            self.normalizer = nm.Normalize(name_norma)
        # TEST
        self.same_trust = 0
        #self.majority_it = [[0 for i in range(o.nb_prec)] for o in self.obj.of]
        # self.config_src = [[] for i in range(len(self.sf))]
        self.config_obj = []
        # self.hamming = [[] for i in range(len(self.sf))]
        
        # for s in range(len(self.sf)):
        #     self.gen_config_sources(s)
        
    def to_file(self):
        """
        write a file with the current graph
        """
        res = "#nbsrc nbobj nbfct\n"
        res += f"{len(self.mat_fs[0])} {len(self.mat_of)} {len(self.mat_of[0])}\n"
        res += f"#truth : {'-'.join([str(self.obj.get_truth(i)[0].id) for i in range(len(self.obj.of))])}\n"
        res += "#links between sources and facts\n"
        res += "#source 1\n"
        for i in range(len(self.sf)):
            for j in range(len(self.sf[i])):
                if self.sf[i][j] == 1:
                    res += f"{j+1},"
            if res[-1] == ',':
                res = res[:-1]
            res += "\n"
        res += "-\n"
        res += "#links between objects and facts\n"
        res += "#object 1\n"
        for i in range(len(self.mat_of)):
            for j in range(len(self.mat_of[i])):
                if self.mat_of[i][j] == 1:
                    res += f"{j+1},"
            if res[-1] == ',':
                res = res[:-1]
            res += "\n"            
        return res
    
    def list_sf(self):
        res = ""
        for i in range(len(self.sf)):
            for j in range(len(self.sf[i])):
                if self.sf[i][j] == 1:
                    res += f"{j},"
            res = res[:-1]
            res += "-"
        # for s in self.sf:
        #     for e in s:
        #         res += f"{int(e)},"
        #     res = res[:-1]
        #     res += "-"
        return res[:-1]
        
    def list_of(self):
        res = ""
        for i in range(len(self.mat_of)):
            for j in range(len(self.mat_of[i])):
                if self.mat_of[i][j] == 1:
                    res += f"{j},"
            res = res[:-1]
            res += "-"
        # for o in self.mat_of:
        #     for e in o:
        #         res += f"{int(e)},"
        #     res = res[:-1]
        #     res += "-"
        return res[:-1]
    
    def list_truth(self):
        res = ""
        for i in range(len(self.obj.facts)):
            if self.obj.facts[i].is_true:
                res += f"{i}-"
        # for n in self.obj.facts:
        #     res += f"{1 if n.is_true else 0}-"
        return res[:-1]
    
    def add_new_fact(self, fct, obj, src):
        """
        add a new fact in a existing graph
        /!\ it is essential to use graph.regen_graph() after 
        having added all the facts to rebuild the graph correctly
        
        fct : id (not index) of the new fact
        obj : id (not index) of object linked to the new fact
        src : id (not index) of sources that claim fct
        """
        newf = []
        for i in range(len(self.trust_s)):
            if i+1 in src:
                newf.append(1)
            else:
                newf.append(0)
        self.mat_fs.insert(fct-1, np.array(newf))
        
        if len(self.mat_of) < obj:
            self.mat_of.append(np.array([0 for i in range(len(self.mat_of[0]))]))
            
        for i in range(len(self.mat_of)):
            if i+1 == obj:
                self.mat_of[i] = np.insert(self.mat_of[i], fct-1, [1])
            else:
                self.mat_of[i] = np.insert(self.mat_of[i], fct-1, [0])
        
    
    def regen_graph(self, init_trust=[]):
        """
        does not regenerate :
            - the normalizer
            - the truth value
        """
        if len(init_trust) == 0:
            self.trust_s = [self.init_trust for i in range(len(self.mat_fs[0]))]
        else:
            self.trust_s = [init_trust[i] for i in range(len(self.mat_fs[0]))]
        self.mem = [self.trust_s.copy()]
        self.trust_f = [0 for i in range(len(self.mat_fs))]
        self.iteration = 0
        self.obj = obj.Obj(len(self.mat_of), self.voting_met, self.vote_para)
        if self.long:
            self.obj.add_nodes_long(self.mat_of, self.mat_fs)
        else:
            self.obj.add_nodes(self.mat_of, self.mat_fs)
        self.obj.update_voting_parameters()
        self.sf = []
        self.gen_sf()
        
    def reset_graph(self, init_trust=[]):
        """
        reset the reliabilty/memory/iteration/confidence 
        of the elements of the graph
        """
        if len(init_trust) == 0:
            self.trust_s = [self.init_trust for i in range(len(self.mat_fs[0]))]
        else:
            self.trust_s = deepcopy(init_trust)
 #[init_trust[i] for i in range(len(self.mat_fs[0]))]
        self.mem = [self.trust_s.copy()]
        self.trust_f = [0 for i in range(len(self.mat_fs))]
        self.iteration = 0
        self.obj.reset_obj(self.trust_f)
    
    def change_norma(self, norma_name):
        self.reset_graph()
        self.normalizer.name = norma_name
    
    def change_vote(self, voting_method, option):
        self.reset_graph()
        self.voting_met = voting_method
        self.vote_para = option
        self.obj.change_vote(self.voting_met, self.vote_para)
        
    def best_sources(self):
        """
        return the index of the best sources
        """
        best = [0]
        for i in range(1, len(self.trust_s)):
            if self.trust_s[i] > self.trust_s[best[0]]:
                best = [i]
            elif self.trust_s[i] == self.trust_s[best[0]]:
                best.append(i)
        return best
    
    def nb_best_facts(self, s):
        """
        number of best facts for a source
        s : index of the source
        """
        n = 0
        best = [n.ind for n in self.obj.get_best_facts()]
        for j in range(len(self.sf[s])):
            if self.sf[s][j] == 1 and j in best:
                n += 1
        return n
        
    def get_rank_sources_name(self, reverse=True):
        """
        return the ranking of the sources (only the name)
        If 2 sources have the same trust, both of them are in one list
        """
        name = []
        for i in range(len(self.trust_s)):
            name.append(i+1)
        res = list(zip(name, self.trust_s))
        res.sort(reverse=reverse, key=itemgetter(1))
        groups = groupby(res, itemgetter(1))
        rank = [[item[0] for item in data] for (key, data) in groups]
        return rank
        
    def get_rank_sources(self, reverse=True):
        """
        return the ranking of the sources
        """
        name = []
        for i in range(len(self.trust_s)):
            name.append(i+1)
        res = list(zip(name, self.trust_s))
        res.sort(reverse=reverse, key=itemgetter(1))
        return res
    
    def str_rank_sources(self, reverse=True):
        rank = self.get_rank_sources(reverse)
        res = "Rank sources : \n"
        for t in rank:
            #res += f"\033[31m{t[0]}\033[00m : {round(t[1],3)}\n"
            res += f"\033[31m{t[0]}\033[00m : {round(t[1],3)} - [{np.count_nonzero(self.sf[t[0]-1] == 1)}]\n"
        return res
        
    def __str__(self):
        res = self.str_sf()
        res += "\n"
        res += str(self.obj)
        #res += "\n"
        #res += self.str_trust_s()
        #res += "\n"
        #res += self.obj.str_trust_f()
        return res
    
    def print_iteration(self):
        if self.iteration == 0:
            return "Initialization\n"
        return f"### {self.iteration}\n"    
    
    def str_sources(self):
        res = ""
        for i in range(len(self.trust_s)):
            res += f"Source {i+1} : {self.trust_s[i]}\n"
        return res + "\n"
    
    def str_trust(self):
        """
        """
        res = self.print_iteration()
        res += self.str_trust_s() + "\n"
        res += self.obj.str_trust_f() + "\n"
        
        #ITERATION TRUST
        # res += f"It{self.iteration} & "
        # res += " & ".join([str(round(self.trust_s[i],3)) for i in range(len(self.trust_s))])
        # res += " \\\\\n"
        # res += f"It{self.iteration} & "
        # res += " & ".join([str(round(self.trust_f[i],3)) for i in range(len(self.trust_f))])
        # res += " \\\\\n"
        # DETAIL BY OBJ
        #if self.iteration > 0:
            #res += self.str_sources()
            #res += self.obj.str_object() + "\n"
        #CONFIG
        self.print_config()
            
        res += "\n-------\n"
        return res
    
    def print_config(self):
        if self.iteration >= 1:
            self.gen_winning_config()
            #for s in range(len(self.sf)):
                #print(f"c_{s+1} : ", self.config_src[s][-1])

            print(f"co{self.iteration} : ", self.config_obj[-1])
            # print(f"It{self.iteration} & {' & '.join([str(n) for n in self.config_obj[-1]])} \\\\\n")
            #for s in range(len(self.sf)):
                #print(f"c_{s} : ", self.config_src[s], self.hamming[s][-1])
        
    def gen_sf(self):
        self.sf = [np.array([]) for i in range(len(self.mat_fs[0]))]
        for i in range(len(self.mat_fs)):
            for j in range(len(self.mat_fs[i])):
                self.sf[j] = np.append(self.sf[j], self.mat_fs[i][j])
        
    def str_sf(self):
        res = "sf : \n"
        for i in range(len(self.sf)):
            res += f"\033[31m{i+1}\033[00m : ["
            for j in range(len(self.sf[i])):
                if self.sf[i][j] > 0:
                    res += f"{j+1},"
            if np.count_nonzero(self.sf[i] == 1) > 0:
                res = res[:-1]
            res += "]\n"
        return res
    
    def str_trust_s(self):
        res = "Reliability sources :\n"
        for i in range(len(self.trust_s)):
            #res += f"\033[31m{i+1}\033[00m : {round(self.trust_s[i],3)} ; "
            res += f"\033[31m{i+1}\033[00m : {round(self.trust_s[i],3)} - [{np.count_nonzero(self.sf[i] == 1)}] ; "
        res += "\n"
        return res
        
    def trust_fact(self):
        """
        Compute the trust for the facts
        """
        tmp_trust_f = [0 for i in self.trust_f]
        for i in range(len(self.trust_f)):
            tmp_trust_f[i] = sum(self.mat_fs[i]*self.trust_s)
        self.trust_f = tmp_trust_f
        
    def trust_sources(self):
        """
        Compute the trust for the sources
        """
        tmp_trust_s = [0 for s in self.trust_s]
        for i in range(len(self.mat_fs)):
            for j in range(len(self.mat_fs[i])):
                tmp_trust_s[j] += (self.mat_fs[i][j] * self.obj.facts[i].score)
        self.trust_s = tmp_trust_s
    
    def majority(self, extend=False):
        """
        return a list with the nodes(facts) that have 
        the majority (most number of claims) on each object
        """
        maj = []
        n = 0
        m = []
        for o in self.obj.of:
            for f in o.prec:
                if n < f.nb_prec:
                    m = [f]
                    n = f.nb_prec
                elif n == f.nb_prec:
                    m.append(f)
            if extend:
                maj.extend(m)
            else:
                maj.append(m)
            m = []
            n = 0
        return maj
    
    def check_true_majority_obj(self):
        """
        Test if all the winner have a clear majority (with the reliability)
        Return True or False, List with the number of facts with the majority on the object (ind 0 = object 1 in the graph)
        """
        res = []
        for i in range(len(self.obj.of)):
            src = [0 for s in range(len(self.trust_s))]
            fct = []
            o = self.obj.of[i]
            for f in o.prec:
                fct.append(f.trust)
                src = src + self.mat_fs[f.ind]
            nb = sum([self.trust_s[i] for i in range(len(src)) if src[i] > 0])
            majo_score = nb/2
            n = 0
            for f in fct:
                if f > majo_score:
                    n += 1
            res.append(n)
        return all(res), res
    
    def check_true_majority_fct(self):
        """
        Test if all the winner have a clear majority (with the reliability)
        Return True or False, List with the number of facts with the majority on the object (ind 0 = object 1 in the graph)
        """
        res = []
        for i in range(len(self.obj.of)):
            src = [0 for s in range(len(self.trust_s))]
            fct = []
            o = self.obj.of[i]
            for f in o.prec:
                fct.append(f.trust)
                src = src + self.mat_fs[f.ind]
            nb = sum([self.trust_s[i] for i in range(len(src)) if src[i] > 0])
            majo_score = nb/2
            n = []
            for f in fct:
                if f > majo_score:
                    n.append(1)
                else:
                    n.append(0)
            res.append(n)
        return res

    
    def gen_config_sources(self, s):
        """
        """
        for i in range(len(self.mat_fs)):
            if self.mat_fs[i][s] == 1:
                # self.config_src[s].append(i+1)
                if i % 2 == 0:
                    self.config_src[s].append(0)
                else:
                    self.config_src[s].append(1)
                
    def gen_winning_config(self):
        #hamming pour une config (graphe complet)
        self.config_obj.append([])
        for i in range(len(self.obj.of)):
            bo = self.obj.get_best_fact(i)
            if len(bo)>1:
                self.config_obj[-1].append("?")
            else:
                # self.config_obj.append(bo[0].id)
                if bo[0].ind % 2 == 0: 
                    self.config_obj[-1].append(0)
                else:
                    self.config_obj[-1].append(1)

        # for s in range(len(self.sf)):
        #     tmp1 = []
        #     tmp2 = []
        #     for i in range(len(self.config_obj[-1])):
        #         if self.config_obj[-1][i] != "?":
        #             tmp1.append(self.config_obj[-1][i])
        #             tmp2.append(self.config_src[s][i])
        #     self.hamming[s].append(round(distance.hamming(tmp1, tmp2), 2))
        
        #hamming pour toutes les config des iterations precedentes
        #self.config_obj.append([])
        #for i in range(len(self.obj.of)):
            #bo = self.obj.get_best_fact(i)
            #if len(bo)>1:
                #self.config_obj[-1].append("?")
            #else:
                ## self.config_obj.append(bo[0].id)
                #if bo[0].ind % 2 == 0: 
                    #self.config_obj[-1].append(0)
                #else:
                    #self.config_obj[-1].append(1)
        #self.config_obj = []
        
        #for s in range(len(self.sf)):
            #self.hamming[s].append([])
            #for i in range(len(self.config_obj)):
                #tmp1 = []
                #tmp2 = []
                #for j in range(len(self.config_obj[i])):
                    #if self.config_obj[i][j] != "?":
                        #tmp1.append(self.config_obj[i][j])
                        #tmp2.append(self.config_src[s][j])
                #self.hamming[s][-1].append(round(distance.hamming(tmp1, tmp2), 2))
                
    def normalize_trust(self):
        for i in range(len(self.trust_s)):
            self.trust_s[i] = self.normalizer.run_normalize(self, i)
        if len(set(self.trust_s)) == 1:
            self.same_trust += 1
    
    def convergence(self):
        """
        Check the convergence of the cosine similarity
        """
        #if self.iteration < 2:
        if len(self.mem) < 2:
            return False
        if self.iteration > self.max_it:
            print("Infinite Loop / Bug")
            print("Unknown error")
            print(f"Method : {self.obj.voting_met} - {self.normalizer.name}")
            print(self)
            print(self.str_trust())
            print("\nGraph links :")
            print(self.to_file())
            return True
        old = self.mem[1]
        current = self.mem[0]
        if sum(old) == 0 or sum(current) == 0:
            print("Infinite Loop / Bug")
            print("Trust of all elements is null, no facts claimed")
            print(f"Method : {self.voting_met} - {self.normalizer.name}")
            print(self)
            print(self.str_trust())
            print("\nGraph links :")
            print(self.to_file())
            return True
        
        #cos_sim = np.dot(current, old) / (norm(current)*norm(old))
        eucli = distance.euclidean(current, old)
        epsilon = 0.001
        #if 1-cos_sim <= epsilon:
        if eucli <= epsilon:
            return True
        return False
    
    def update_mem(self):
        """
        update the memory
        """
        self.mem = [self.trust_s.copy(), self.mem[0].copy()]
        # TEST MAJORITY
        #l = self.check_true_majority_fct()
        #for i in range(len(l)):
            #for j in range(len(l[i])):
                #self.majority_it[i][j] += l[i][j]
    
    def run(self):
        """
        Run the algorithm
        update the trust of fact
        execute the vote
        update the trust of the sources
        """
        print(self.str_trust())
        while not self.convergence():
            self.iteration += 1
            self.trust_fact()
            self.obj.update_trust(self.trust_f)
            self.obj.voting()
            print(self.str_trust())
            self.trust_sources()
            self.normalize_trust()
            self.update_mem()
        self.convergence()
        
    def run_noprint(self):
        """
        Run the algorithm
        update the trust of fact
        execute the vote
        update the trust of the sources
        """
        while not self.convergence():
            self.iteration += 1
            self.trust_fact()
            self.obj.update_trust(self.trust_f)
            self.obj.voting()
            
            #self.gen_winning_config()
            
            self.trust_sources()
            self.normalize_trust()
            self.update_mem()
    
