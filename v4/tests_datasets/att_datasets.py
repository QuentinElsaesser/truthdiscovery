from v4.graph import graph

import numpy as np

class AttDatasets():
    def __init__(self, G, truth_obj):
        """
        truth_of : list of true fact for every object
        truth_obj : list of object with a true fact
        """
        self.G = G if isinstance(G, graph.Graph) else G.G
        
        self.truth_obj = truth_obj
        
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        
        self.recall = 0
        self.accuracy = 0
        self.precision = 0
        self.csi = 0
        
        self.diff = 0
        self.diff_src = []
        
        self.iteration = self.G.iteration
        
    # def __str__(self):
    #     res = f"Precision : {round(self.precision*100,2)} - {self.precision*100}\n"
    #     res += f"Accuracy :  {round(self.accuracy*100,2)} - {self.accuracy*100}\n"
    #     res += f"Recall : {round(self.recall*100,2)} - {self.recall*100}\n"
    #     res += f"CSI : {round(self.csi*100,2)} - {self.csi*100}\n"
    #     return res
    
    def __str__(self):
        res = f"Precision : {round(self.precision*100,2)}\n"
        res += f"Accuracy :  {round(self.accuracy*100,2)}\n"
        res += f"Recall : {round(self.recall*100,2)}\n"
        res += f"CSI : {round(self.csi*100,2)}\n"
        res += f"Iteration : {self.iteration}\n"
        return res
    
    def compute_diff(self, v, l):
        for i in range(len(v)):
            self.diff_src.append(abs(v[i] - l[i]))
        self.diff = np.mean(self.diff_src)
    
    def compute_truth(self):
        for i in self.truth_obj:
            ind = i-1
            best = self.G.obj.get_best_fact(ind)
            for f in self.G.obj.of[ind].prec:
                if f in best:
                    if f.is_true:
                        self.TP += 1
                    else:
                        self.FP += 1
                else:
                    if f.is_true:
                        self.FN += 1
                    else:
                        self.TN += 1
    
    def compute_metrics(self):
        tmp = (self.TP+self.FP)
        if tmp == 0:
            tmp = 1
        self.precision = self.TP / tmp

        tmp = self.TP + self.FN + self.FP
        if tmp == 0:
            tmp = 1
        self.csi = (self.TP / tmp)

        tmp = (self.TP+self.FP+self.TN+self.FN)
        if tmp == 0:
            tmp = 1
        self.accuracy = (self.TP+self.TN) / tmp
        
        tmp = (self.TP+self.FN)
        if tmp > 0:
            self.recall = self.TP / tmp
        
    def run_all(self):
        """
        run all the metrics
        """
        self.compute_truth()
        self.compute_metrics()
        self.iteration = self.G.iteration
    