from v4.vote import voting_method

# from v4.vote import parameters_vote as pm

class Plurality(voting_method.Vote):
    def __init__(self, option=1):
        """
        Plurality vote
        """
        super().__init__(option=option)
        
    def update_max_value(self):
        super().update_max_value(1)
        
    def plurality_opti(self, r):
        if len(r[0]) == 1:
            res = [1]
            res.extend([0 for n in range(self.max_len_of-1)])
        else:
            res = [1 for i in range(len(r[0]))]
            res.extend([0 for n in range(self.max_len_of-len(r[0]))])
        return res

    def plurality_tie(self, r):
        res = [1]
        res.extend([0 for n in range(self.max_len_of-1)])
        return res
    
    def set_para(self, option):
        self.option = option
        if self.option == 1:
            self.sr = self.plurality_tie
        elif self.option == 2:
            self.sr = self.plurality_opti
        else:
            raise ValueError(f"{self.option} = Unknown scoring rule")

        
    # def execute(self, ranking):
    #     """
    #     Update the score of the node
        
    #     The first fact get a score if it is alone
    #     The facts rank first get a score if they're more than one
    #     The other facts (not rank first) get another score
    #     """        
    #     ### V1 Si tie on donne 1 a tout le monde
    #     # self.set_rank(ranking)
    #     # for i in range(len(self.rank)):
    #     #     if i == 0:
    #     #         if len(self.rank[i]) == 1:
    #     #             for n in self.rank[i]:
    #     #                 n.score += self.sr[0]
    #     #         else:
    #     #             for n in self.rank[i]:
    #     #                 if callable(self.sr[1]) and (self.sr[1]).__name__ == "<lambda>":
    #     #                     n.score += self.sr[1](len(self.rank[i]))
    #     #                 else:
    #     #                     n.score += self.sr[1]
    #     #     else:
    #     #         for n in self.rank[i]:
    #     #             n.score += self.sr[2]
    #     ##### V2 si tie on donne la moyenne
    #     self.set_rank(ranking)
    #     values = self.sr(ranking)
    #     # print("values : ", values)
    #     # print("ranking : ", [[e.id for e in r] for r in self.rank])            

    #     cpt = 0
    #     sum_score = 0
    #     for i in range(len(self.rank)):
    #         # print(self.rank[i])
    #         for j in range(len(self.rank[i])):
    #             if len(self.rank[i]) > 1:
    #                 # print(f"add to sum_score {sum_score} + {values[cpt]}")
    #                 sum_score += values[cpt]
    #                 if j+1 == len(self.rank[i]):
    #                     for k in range(len(self.rank[i])):
    #                         self.rank[i][k].score += sum_score/len(self.rank[i])
    #                         # print("INFO fct", self.rank[i][k].id, "score", self.rank[i][k].score, "sum_s", sum_score, "index", cpt, values, "j", j, [e.id for e in self.rank[i]])
    #                     sum_score = 0
    #             else:
    #                 self.rank[i][j].score += values[cpt]
    #                 # print("INFO fct", self.rank[i][j].id, "score", self.rank[i][j].score, "index", cpt, values, "j", j, [e.id for e in self.rank[i]])
    #             cpt += 1
    #     # print("\n")