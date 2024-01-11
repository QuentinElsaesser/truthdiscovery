class Vote:
    def __init__(self, option=1):
        self.rank = []
        #scoring method
        self.sr = None
        #1 : mean if tie
        self.option = option
        #max numbre of facts for an object
        self.max_len_of = 0
        #The best score possible given with the vote
        self.max_value = 0
    
    def set_para(self, option) -> None:
        """
        add the scoring rule depending on the option
        """
        pass
        # self.option = para[0]
        # self.sr = para[1]

    def set_rank(self, ranking):
        """
        Update rank with the new ranking
        """
        self.rank = ranking
        
    def update_max_value(self, v):
        self.max_value = v
        
    # def reset_vote(self):
    #     """
    #     no need, we set the rank when the execute is called
    #     """
    #     self.rank = []

    def execute(self, ranking):
        """
        Execute the vote
        """
        self.set_rank(ranking)
        values = self.sr(ranking)
        #print("values : ", values)
        #print("ranking : ", [[e.id for e in r] for r in self.rank])            

        cpt = 0
        sum_score = 0
        for i in range(len(self.rank)):
            #print(self.rank[i])
            for j in range(len(self.rank[i])):
                if len(self.rank[i]) > 1:
                    #print(f"add to sum_score {sum_score} + {values[cpt]}")
                    sum_score += values[cpt]
                    if j+1 == len(self.rank[i]):
                        for k in range(len(self.rank[i])):
                            self.rank[i][k].score += sum_score/len(self.rank[i])
                            #print("INFO fct", self.rank[i][k].id, "score", self.rank[i][k].score, "sum_s", sum_score, "index", cpt, values, "j", j, [e.id for e in self.rank[i]])
                        sum_score = 0
                else:
                    self.rank[i][j].score += values[cpt]
                    #print("INFO fct", self.rank[i][j].id, "score", self.rank[i][j].score, "index", cpt, values, "j", j, [e.id for e in self.rank[i]])
                cpt += 1
        #print("\n")