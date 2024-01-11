from v4.graph import node

from operator import itemgetter
from itertools import groupby
import numpy as np

class Obj:
    def __init__(self, nb_o, voting_met, vote_para):
        """
        nb_o : number of object
        voting_met : the voting method we use
        vote_para : the parameters for the vote
        
        of : list of node object
        facts : list of node facts
        truth : true facts
        """
        self.of = []
        self.facts = []
        self.voting_met = voting_met()
        self.option = vote_para
        self.max_len_of = 0
        self.truth = []
        for i in range(nb_o):
            self.of.append(node.Node(idn=i+1, ind=i, typef="O"))
        # TEST CONV
        self.winners = [[] for n in range(nb_o)]
        self.change = [0 for n in range(nb_o)]
            
    def get_obj(self, indf):
        fct = self.facts[indf]
        for i in range(len(self.of)):
            o = self.of[i]
            if fct in o.prec:
                return i
        return None
        
    def update_truth(self, truth):
        if len(truth) > 0: 
            if len(truth) != len(self.facts):
                raise ValueError("Length of truth {len(truth)} and self.facts {len(self.facts)} must be the same")
            self.truth = truth
            for i in range(len(truth)):
                self.facts[i].is_true = (truth[i] == 1)
    
    def reset_obj(self, trust_f):
        for n in self.of:
            for p in n.prec:
                p.reset_node()
        self.update_trust(trust_f)
        # self.voting_met.reset_vote()
        
    def change_vote(self, vote, option):
        self.voting_met = vote(option)
        self.option = option
        self.update_voting_parameters()
    
    def get_truth(self, i):
        """
        return the true fact on each object
        i : index of object 
        """
        return self.of[i].truth()
    
    def get_best_facts_group(self):
        """
        get the best fact in list of sub lists
        """
        res = []
        for i in range(len(self.of)):
            res.append(self.get_best_fact(i))
        return res
    
    def get_best_facts(self):
        """
        get the best fact in a list
        """
        res = []
        for i in range(len(self.of)):
            res.extend(self.get_best_fact(i))
        return res
        
    def get_best_fact(self, i):
        """
        return the best fact on each object
        i : index of object 
        """
        return self.of[i].best()
    
    def get_rank_fct_on_obj(self, i, reverse=True):
        """
        return the rank of the facts on the obj in index i
        """
        trust = []
        name = []
        for n in self.of[i].prec:
            trust.append(n.trust)
            name.append(n)
        res = list(zip(name, trust))
        res.sort(reverse=reverse, key=itemgetter(1))
        
        ind = []
        for i in range(len(res)):
            if res[i][0].nb_prec == 0:
                ind.append(i)
        
        res = [res[j] for j in range(len(res)) if j not in ind]
        
        groups = groupby(res, itemgetter(1))
        return [[item[0] for item in data] for (key, data) in groups]        
    
    def get_rank_facts(self, reverse=True):
        """
        return the ranking for the facts
        """
        trust = []
        for n in self.facts:
            trust.append(n.trust)
        res = list(zip(self.facts, trust))
        res.sort(reverse=reverse, key=itemgetter(1))
        
        ind = []
        for i in range(len(res)):
            if res[i][0].nb_prec == 0:
                ind.append(i)
        
        return [res[j] for j in range(len(res)) if j not in ind]
    
    def str_rank_facts(self, reverse=True):
        rank = self.get_rank_facts(reverse)
        res = "Rank facts : \n"
        for t in rank:
            #res += t[0].str_spe() + "\n"
            res += t[0].str_spe_nos() + " - " + str(t[0].is_true) + "\n"
        return res
        
    def __str__(self):
        res = "of : \n"
        for n in self.of:
            res += f"\033[31m{n.id}\033[00m : ["
            for f in n.prec:
                res += f"{f.id},"
            if len(n.prec) > 0:
                res = res[:-1]
            res += "]\n"
        return res
    
    def str_trust_f(self):
        res = "Reliability facts :\n"
        for f in self.facts:
            #res += f"{str(f)} ; "
            res += f"{f.str_spe()} ; "
            #res += f"{f.str_spe_nos()} ; "
        res += "\n"
        return res
    
    def str_object(self):
        res = "Reliability facts :\n"
        for o in self.of:
            res += f"Object {o.id} :\n"
            for f in o.prec:
                # res += f"{f.str_spe_nos()}\n"
                # res += f"{f.str_spe_nos()} - {f.is_true}\n"
                res += f"{f.str_spe()}\n"
            res += "\n"
        return res
    
    def get_nb_true_prec(self, i):
        """
        return the number of facts with at least one claim
        """        
        n = 0
        for nd in self.of[i].prec:
            if nd.nb_prec > 0:
                n += 1
        return n
    
    def add_nodes(self, matrix, mat_fs):
        """
        add the nodes of the matrix
        matrix : [np.array([1,1,1,0,0]), np.array([0,0,0,1,1]) Adjacency matrix between facts and objects
        """
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    n = node.Node(idn=j+1, ind=j, typef="F", nb_prec=np.count_nonzero(mat_fs[j] == 1))
                    self.of[i].add_prec(n)
                    self.facts.append(n)
                    #facts with no claim
                    self.max_len_of = max(self.max_len_of, self.of[i].nb_prec)
                    #only facts with claim
                    #self.max_len_of = max(self.max_len_of, self.get_nb_true_prec(i))

    def add_nodes_long(self, matrix, mat_fs):
        """
        add the nodes of the matrix
        matrix : list of facts for each object
        """
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                n = node.Node(idn=matrix[i][j]+1, ind=matrix[i][j], typef="F", nb_prec=np.count_nonzero(mat_fs[j] == 1))
                self.of[i].add_prec(n)
                self.facts.append(n)
                self.max_len_of = max(self.max_len_of, self.of[i].nb_prec)

    def update_voting_parameters(self):
        """
        upate the parameters of the voting method
        """
        self.voting_met.max_len_of = self.max_len_of
        self.voting_met.set_para(self.option)
        self.voting_met.update_max_value()
    
    def update_trust(self, trust):
        """
        update the trust of the node with a vector of trust
        """
        for i in range(len(trust)):
            self.facts[i].trust = trust[i]

    def reset_score(self):
        """
        reset the score of the facts
        """
        for n in self.of:
            for f in n.prec:
                f.score = 0
                
    def voting(self):
        """
        rank the facts
        update the parameters of the vote
        execute the vote to get the score depending on the ranking and the voting method
        """
        self.reset_score()
        ind = 0
        for n in self.of:
            name = []
            trust = []
            rank = []
            for f in n.prec:
                name.append(f)
                trust.append(f.trust)
                ziped = list(zip(name, trust))
                ziped.sort(reverse=True, key = itemgetter(1))
                groups = groupby(ziped, itemgetter(1))
                rank = [[item[0] for item in data] for (key, data) in groups]
                
            self.voting_met.execute(rank)
            self.winners[ind].append([(n.id%2) for n in self.get_best_fact(ind)])
            if len(self.winners[ind]) > 1:
                self.change[ind] += int(not(self.winners[ind][-1] == self.winners[ind][-2]))
            ind += 1
            #print("\nDans voting de obj.py")
            #for f in n.prec:
                #print(f, "-", f.score, [f.nb_prec])
            #print()

