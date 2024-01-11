class Node:
    def __init__(self, idn, ind, typef=None,truth=False,nb_prec=0):
        """
        idn : name or id of the node
        ind : index of the node in the list of nodes
        typef : type of the node (object, fact, source)
        truth : if the node if true or false (for a fact)
        
        prec : predecessor in the graph (to link the object and the fact)
        trust : the trust of the node
        score : the score get with the vote
        """
        self.typef=typef
        self.prec = []
        self.nb_prec = nb_prec
        self.id = idn
        self.ind = ind
        self.trust = 0
        self.score = 0
        self.is_true = truth
        
    def reset_node(self):
        self.trust = 0
        self.score = 0
        if self.typef == "O":
            self.nb_prec = len(self.prec)
        
    def add_prec(self, node):
        """
        Add a predecessor for the node
        """
        self.prec.append(node)
        self.nb_prec += 1
        
    def best(self):
        """
        return the best among the predecessors
        """
        b = []
        for f in self.prec:
            if len(b) == 0:
                b.append(f)
            else:
                if f.trust > b[0].trust:
                    b = [f]
                elif f.trust == b[0].trust:
                    b.append(f)
        return b
    
    def truth(self):
        """
        return the true fact
        """
        res = []
        for f in self.prec:
            if f.is_true:
                res.append(f)
        return res
    
    def __str__(self):
        if self.typef == "O":
            return f"O{self.id}"
        return f"\033[31m{self.id}\033[00m : {round(self.trust,3)}"
    
    def str_spe(self):
        return f"\033[31m{self.id}\033[00m : {round(self.trust,3)} - \033[32m{self.score}\033[00m - [{self.nb_prec}]"
    
    def str_spe_nos(self):
        """
        Without score
        """
        return f"\033[31m{self.id}\033[00m : {round(self.trust,3)} - [{self.nb_prec}]"
    
    