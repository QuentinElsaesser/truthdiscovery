from v4.vote import voting_method

class Borda(voting_method.Vote):
    def __init__(self, option=1):
        super().__init__(option=option)
        
    def update_max_value(self):
        super().update_max_value(self.sr(self.max_len_of)[0])
        
    def borda_tie(self, r):
        """
        generate depending on the length of fact in the object (fact in the ranking to be more precise)
        r : ranking
        """
        if type(r) == int:
            x = r
        else:
            x = sum([len(l) for l in r])
        if x == 0:
            return []
        if x == 1:
            if self.max_len_of == 1:
                return [1]
            return [self.max_len_of-1]
        v = [i for i in range(self.max_len_of-1, self.max_len_of-x-1, -1)]
        return v
    
    def borda_opti(self, r):
        """
        generate depending on the length of fact in the object (fact in the ranking to be more precise)
        r : ranking
        """
        if type(r) == int:
            return [i for i in range(r-1, -1, -1)]
        if len(r) == 0:
            return []
        if len(r) == 1:
            if self.max_len_of == 1:
                return [1]
            if sum([len(l) for l in r]) == 1:
                return [self.max_len_of-1]
        x = self.max_len_of-1
        v = []
        for l in r:
            for i in range(len(l)):
                v.append(x)
                if len(l) == 1:
                    x -= 1
                else:
                    if i+1 == len(l):
                        x -= len(l)
        return v
    
    def set_para(self, option):
        self.option = option
        if self.option == 1:
            self.sr = self.borda_tie
        elif self.option == 2:
            self.sr = self.borda_opti
        else:
            raise ValueError(f"{self.option} = Unknown scoring rule")
        
    # def execute(self, ranking):
    #     """
    #     Retourne le tableau avec les valeurs a donner aux sources
    #     """
    #     self.set_rank(ranking)
    #     values = self.sr(ranking)
    #     #print("values : ", values)
    #     #print("ranking : ", [[e.id for e in r] for r in self.rank])            

    #     cpt = 0
    #     sum_score = 0
    #     for i in range(len(self.rank)):
    #         #print(self.rank[i])
    #         for j in range(len(self.rank[i])):
    #             if len(self.rank[i]) > 1:
    #                 #print(f"add to sum_score {sum_score} + {values[cpt]}")
    #                 sum_score += values[cpt]
    #                 if j+1 == len(self.rank[i]):
    #                     for k in range(len(self.rank[i])):
    #                         self.rank[i][k].score += sum_score/len(self.rank[i])
    #                         #print("INFO fct", self.rank[i][k].id, "score", self.rank[i][k].score, "sum_s", sum_score, "index", cpt, values, "j", j, [e.id for e in self.rank[i]])
    #                     sum_score = 0
    #             else:
    #                 self.rank[i][j].score += values[cpt]
    #                 #print("INFO fct", self.rank[i][j].id, "score", self.rank[i][j].score, "index", cpt, values, "j", j, [e.id for e in self.rank[i]])
    #             cpt += 1
    #     #print("\n")