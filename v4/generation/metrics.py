from v4.constants import constants

from v4.generation import spe_metrics as spm

class Metrics:
    def __init__(self, experience):
        """
        res : res for the metric in use
        exp : experience with all the graphs
        """
        self.nb_methods = constants.NB_METHODS
        self.res = []
        self.exp = experience
        if experience != None:
            #Change the number of sources (mandatory IF nvalue = SRC)
            self.exp.nbs = self.exp.graphes[0].nbs
        #id for the metrics in dict
        self.n_methods = constants.ID_METRICS
        #id in list for the metrics
        self.id_methods = list(self.n_methods.keys())
        
        self.n = -1
        self.mini = True
        
        self.spe_metric = None
        
        self.id_methods_sources = constants.ID_METHODS_SOURCES
        
        self.metrics = [self.swaps, self.swaps_norma, 
                        self.euclidean_distance, self.euclidean_distance_norma,
                        self.difference, self.metric_trust, self.ranking_order,
                        self.precision, self.accuracy, self.recall,
                        self.csi, self.iteration_avg, self.iteration_max]
        
        #must be the same name in the file latex (used is latex.py)
        self.metrics_name = constants.METRICS_NAMES
        
    def __str__(self):
        if self.n == -1:
            return "No results"
        res = f"Results for {self.metrics[self.n].__name__} with {self.exp.graphes[0].rgs[0].nbs} sources, prior {self.exp.graphes[0].prior} and graph {self.exp.graphes[0].rgs[0].typeg}:\n"
        for i in range(len(constants.ORDER)):
            res += f"{constants.ORDER[i]} : {self.res[i]}\n"
        res += "\n"
        return res
    
    def consistency(self):
        self.mini = False
        self.n = self.n_methods["Ct"]
        self.res = [0 for i in range(self.nb_methods)]
        if self.exp.formula != None:
            for g in self.exp.graphes:
                for i in range(len(g.rgs)):
                    self.res[i] += g.rgs[i].metric_att.consistent_f
            self.res = [(r/self.exp.nb_exp) for r in self.res]
    
    def ranking_order(self):
        """
        # Number of graph with the exact ranking i.e. nb_swap == 0
        """
        self.mini = False
        self.n = self.n_methods["RO"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in self.id_methods_sources:
                self.res[i] += int(g.rgs[i].metric_att.swap == 0)
        self.res = [(r/self.exp.nb_exp) for r in self.res]
    
    def swaps(self):
        """
        Return the average number of swaps
        """
        self.mini = True
        self.n = self.n_methods["S"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in self.id_methods_sources:
                self.res[i] += g.rgs[i].metric_att.swap
        self.res = [r/self.exp.nb_exp for r in self.res]
        #print(self.res)
        
    def swaps_norma(self):
        """
        Return the normalize average number of swaps
        """
        self.mini = True
        self.n = self.n_methods["SN"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in self.id_methods_sources:
                # maxi = ((g.rgs[i].nbs-1) * g.rgs[i].nbs) / 2
                self.res[i] += (g.rgs[i].metric_att.swap/g.rgs[i].metric_att.swap_max)
        self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
            
    def euclidean_distance(self):
        """
        Return the average euclidean distance
        """
        self.mini = True
        self.n = self.n_methods["E"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in self.id_methods_sources:
                self.res[i] += g.rgs[i].metric_att.euclidean_d
        self.res = [(r/self.exp.nb_exp) for r in self.res]
        
    def euclidean_distance_norma(self):
        """
        Return the normalize average euclidean distance
        """
        self.mini = True
        self.n = self.n_methods["EN"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in self.id_methods_sources:
                self.res[i] += (g.rgs[i].metric_att.euclidean_d/g.rgs[i].metric_att.euclidean_d_max)        
        self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def difference(self):
        """
        Return the average difference between the a posteriori and trust
        """
        self.mini = True
        self.n = self.n_methods["D"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in self.id_methods_sources:
                self.res[i] += g.rgs[i].metric_att.difference
        self.res = [(r/self.exp.nb_exp) for r in self.res]
                
    def precision(self):
        """
        Return the average precision
        """
        self.mini = False
        self.n = self.n_methods["P"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in range(len(g.rgs)):
                self.res[i] += g.rgs[i].metric_att.precision
        self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def accuracy(self):
        """
        Return the average accuracy
        """
        self.mini = False
        self.n = self.n_methods["A"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in range(len(g.rgs)):
                self.res[i] += g.rgs[i].metric_att.accuracy
        self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def recall(self):
        """
        Return the average recall
        """
        self.mini = False
        self.n = self.n_methods["R"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in range(len(g.rgs)):
                self.res[i] += g.rgs[i].metric_att.recall
        self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def csi(self):
        """
        Return the average csi
        """
        self.mini = False
        self.n = self.n_methods["CSI"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in range(len(g.rgs)):
                self.res[i] += g.rgs[i].metric_att.csi
        self.res = [(r/self.exp.nb_exp)*100 for r in self.res]
        
    def iteration_avg(self):
        """
        Return the average number of iterations
        """
        self.mini = True
        self.n = self.n_methods["Ia"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in range(len(g.rgs)):
                self.res[i] += g.rgs[i].metric_att.iteration
        self.res = [(r/self.exp.nb_exp) for r in self.res]
        #print(self.res)
        
    def iteration_max(self):
        """
        Return the maximum number of iterations
        """
        self.mini = True
        self.n = self.n_methods["Im"]
        self.res = [0 for i in range(self.nb_methods)]
        for g in self.exp.graphes:
            for i in range(len(g.rgs)):
                self.res[i] = max(self.res[i], g.rgs[i].metric_att.iteration)
        #print(self.res)
        
    def metric_trust(self):
        """
        """
        self.mini = True
        self.n = self.n_methods["Mt"]
        if self.spe_metric == None:
            self.spe_metric = spm.SpeMetrics(experience=self.exp)
        
        