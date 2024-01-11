from v4.generation import graph_methods as gm

from v4.generation import priors as pr

from v4.generation import metrics, latex

from v4.constants import constants

import logging, os

class BruteForceExperiencesParameters:
    def __init__(self, nb_exp, percentage, all_priors, prior=None,
                 nbo=10, nbfl=3, nbfu=3, nbs=10, typeg='ncpr',
                 min_fs=1, stop=10000, q=1000, aff=1000, name="v4/results/res0.tex",
                 step=10000, path_xp="xp/", read=False, interval=[], nvalue="", fixed_prc="45-50",
                 formula=None,interp=[]):
        """
        nb_exp : number of graphes we want to generate
        percentage : percentage choose to generate graphs at the start
        all_priors : all the priors for all the percentage
        
        interval : The values we change to test
        nvalue : name of the parameter we change (PRC/FCT/OBJ/SRC)
        fixed_prc : for FCT/OBJ/SRC every graph must be in this prc
        
        We stock in an experience all the nb_exp graphs for one percentage
        """
        self.read = read
        self.name = name.replace("tex", "log")
        if not self.read:
            logging.basicConfig(filename=self.name, format='%(message)s', filemode='w', encoding='utf-8', level=logging.DEBUG)
        
        self.interval = interval
        self.nvalue = nvalue
        self.fixed_prc = fixed_prc
        self.formula = formula
        self.interp = interp
        
        self.isok = [False for i in range(len(self.interval))]
        self.nbgr = [0 for i in range(len(self.interval))]
                
        self.parameters = [stop, step, typeg, percentage, q, min_fs, nbfl, nbfu, nbs, nbo]
        
        self.display = 0
        self.max_step = 0
        
        self.step = step
        self.stop = stop
        self.q = q
        self.aff = aff
        
        self.nb_exp = nb_exp
        
        self.nbs = nbs
        self.nbo = nbo
        self.typeg = typeg
        self.nbfl = nbfl
        self.nbfu = nbfu
        self.typeg = typeg
        self.all_priors = all_priors
        self.prc = percentage
        self.min_fs = min_fs
        
        self.graphes = []
        self.spe_metric = None
        
        self.dico = dict()
        self.infos = [constants.ID_NORMA_A, constants.ID_NORMA_O]
        self.index_info = 0
        
        if not self.read:
            logging.debug(f"obj:{self.nbo} - facts:{self.nbfl}-{self.nbfu} - src:{self.nbs} - prc:{self.prc} - type:{self.typeg}")
        
        for intv in self.interval:
            self.dico[intv] = []
            
        self.write = [False for i in range(len(self.interval))]
        self.path_xp = path_xp
        if not self.read:
            self.file_xp = self.name_xp()
            self.write_head_xp()
    
    def name_xp(self):
        if self.nvalue == "PRC":
            spe = ""
        else:
            spe = self.nvalue.lower()
        nbf = 0
        name_res = self.name.split("/")[-1][:-4]
        name = f"{self.path_xp}{name_res}xp0{spe}.csv"
        while os.path.isfile(name):
            nbf += 1
            name = f"{self.path_xp}{name_res}xp{nbf}{spe}.csv"
        f = open(name, "w")
        print(f"Create file {name}")
        self.name = name
        return f
    
    def str_interval(self):
        res = ""
        for intv in self.interval:
            res += f"{intv}/"
        return res
    
    def write_head_xp(self):
        """
        typeg; nbo; nbs; nbf_low; nbf_up; interval
        """
        if not self.read:
            self.file_xp.write(f"TYPEG;NB_OBJ;NB_SRC;NB_FL;NB_FU;NBF;TRUST;SF;OF;TRUTH;INTERVAL:{self.str_interval()};{self.nvalue}_{self.fixed_prc}\n")
    
    def write_graphes(self, i, intv):
        """
        typeg; nbo; nbs; nbfl; nbfu; nbf; theo_trust; sf; of; truth; interval; type_xp
        interval and type_xp in header and empty in the whole dataset bc it is always the same
        """
        if not self.read:
            for graphes in self.dico[intv]:
                self.file_xp.write(f"{self.typeg};{self.nbo};{self.nbs};{self.nbfl};{self.nbfu};{len(graphes.rgs[self.index_info].G.mat_of[0])};{graphes.rgs[self.index_info].theoritical_trust};{graphes.rgs[self.index_info].G.list_sf()};{graphes.rgs[self.index_info].G.list_of()};{graphes.rgs[self.index_info].G.list_truth()};;\n")
    
    def ask(self):
        if self.display % self.stop == 0:
            txt = "\nContinue infinite loop ? :"
            cont = input(txt)
            logging.debug(f"{txt} {cont}")
            if cont == 'n':
                return False
            elif cont.isnumeric():
                self.stop = int(cont)
            
        if self.display % self.q == 0:
            print(f"{self.infos[self.index_info]} - {self.display} : stop={self.stop} - step={self.step} - type={self.typeg}_{self.prc} -  ask={self.q} - min_fs={self.min_fs}")
            ######
            txt = "\nType graph ? :"
            v = input(txt)
            logging.debug(f"{txt} {v}")
            if v == 'n':
                self.typeg = 'ncpr'
            elif v == 'cp':
                self.typeg = 'cpr'
            elif v == 'r':
                self.typeg = 'ncrand'
            elif v == 'rc':
                self.typeg = 'crand'
            if self.typeg == 'ncpr' or self.typeg == 'cpr':
                if self.nvalue != "PRC":
                    txt = f"Desired prc:{self.fixed_prc}\n"
                    logging.debug(txt)
                    print(txt.strip())
                txt = f"\nA priori PRC in {self.all_priors.percent}? :"
                v = input(txt)
                if v.isnumeric():
                    self.prc = int(v)
                    if self.prc not in self.all_priors.percent:
                        self.prc = self.all_priors.percent[-1]
                logging.debug(f"{txt}\n:{v}")
                if self.nvalue != "PRC":
                    txt, v = self.change()
                    logging.debug(f"{txt}\n:{v}")
            ######
            txt = "\nNumber iteration before q ? :"
            v = input(txt)
            logging.debug(f"{txt} {v}")
            if v.isnumeric():
                if int(v) == 0:
                    return self.ask()
                self.q = self.display + int(v)
                self.step = int(v)
            else:
                self.q = self.display + self.step
            ######
            txt = "\nMin_fs ? :"
            v = input(txt)
            logging.debug(f"{txt} {v}")
            if v.isnumeric():
                self.min_fs = int(v)
                if self.min_fs >= self.nbo:
                    self.min_fs = 1
            txt = f"{self.infos[self.index_info]} - {self.display} : stop={self.stop} - step={self.step} - type={self.typeg}_{self.prc} -  ask={self.q} - min_fs={self.min_fs}"
            logging.debug(f"{txt}\n")
            print(txt)
            
        return True
    
    def change(self):
        if self.nvalue == "FCT":
            txt = f"\nCurrentVal:{self.nbfl}-{self.nbfu}\nNb FCT ?"
            v = input(txt)
            if v.isnumeric():
                self.nbfl = int(v)
                self.nbfu = self.nbfl
        elif self.nvalue == "OBJ":
            txt = f"\nCurrentVal:{self.nbo}\nNb OBJ ?"
            v = input(txt)
            if v.isnumeric():
                self.nbo = int(v)
        elif self.nvalue == "SRC":
            txt = f"\nCurrentVal:{self.nbs}\nNb SRC ?"
            v = input(txt)
            if v.isnumeric():
                self.nbs = int(v)
        return txt, v
    
    def find_intv_para(self, rG):
        if self.nvalue == "PRC":
            return self.find_intv_prc(rG.theoritical_trust)
        elif self.nvalue == "FCT":
            return self.find_intv_elt(int(rG.nbf/rG.nbo), rG.theoritical_trust)
        elif self.nvalue == "OBJ":
            return self.find_intv_elt(rG.nbo, rG.theoritical_trust)
        elif self.nvalue == "SRC":
            return self.find_intv_elt(rG.nbs, rG.theoritical_trust)
        
    def find_intv_elt(self, v, relia):
        """
        find the interval depending on the nbs/nbo and the relia is in the fixed interval
        """
        iv = self.fixed_prc.split("-")
        if int(iv[0]) <= relia <= int(iv[1]):
            for i in range(len(self.interval)):
                intv = self.interval[i]
                if int(intv) == v:
                    return self.interval[i], i
        return None, None    
    
    def find_intv_prc(self, v):
        """
        find the interval depending on the a posteriori probability.theoritical trust
        """
        for i in range(len(self.interval)):
            intv = self.interval[i].split("-")
            if int(intv[0]) <= v <= int(intv[1]):
                return self.interval[i], i
        return None, None    
    
    def add_dict(self, graphe, rG):
        """
        add graphes in the dict at the good interval
        """
        
        intv, i = self.find_intv_para(rG)
        if intv != None:
            if not self.isok[i]:
                # if self.index_info == 0:
                self.dico[intv].append(graphe)   
                    
                self.dico[intv][self.nbgr[i]].add_rg(rG)
                # if self.typeg == "cpr":
                #     self.dico[intv][self.nbgr[i]].complet_graph()
                self.nbgr[i] += 1
                self.isok[i] = self.nbgr[i] >= self.nb_exp
                if not self.write[i] and self.isok[i]:
                    self.write[i] = True
                    self.write_graphes(i, intv)
    
    def run(self):
        """
        generate graphs and write in file but dont run the metrics
        """
        print(f"Generation of {self.infos[self.index_info]}")
        while True:
            for i in range(self.step):
                if not self.ask():
                    #stop during run
                    for i, intv in enumerate(self.interval):
                        if not self.write[i]:
                            self.write_graphes(i, intv)
                    # self.other_methods()
                    # self.run_graph()
                    logging.debug(f"{self.display} : Done")
                    self.file_xp.close()
                    return True
                
                prior = self.all_priors.rand_prior(self.prc)
                graphe = gm.GraphMethods(prior, nbo=self.nbo, nbfl=self.nbfl, 
                                          nbfu=self.nbfu, nbs=self.nbs, typeg=self.typeg,
                                          min_fs=self.min_fs, allg=False)
                
                rG = graphe.create_graph()
                
                self.add_dict(graphe, rG)
                
                self.print_str()
                
                if all(self.isok):
                    self.print_str(force=True)
                    # # self.index_info += 1
                    # # if self.index_info == len(self.infos) or self.typeg == "cpr":
                    # self.other_methods()
                    # self.run_graph()
                    logging.debug(f"{self.display} : Done")
                    self.file_xp.close()
                    return True

                    # self.write = [False for i in range(len(self.interval))]
                    # self.isok = [False for i in range(len(self.interval))]
                    # self.nbgr = [0 for i in range(len(self.interval))]
                    # logging.debug(f"{self.display} : Done")
                    # self.display = 0
                    # txt = f"\n---Generation of {self.infos[self.index_info]}---"
                    # logging.debug(f"{txt}")
                    # self.print_str(force=True)
                    # self.display = 0
                    # self.stop, self.step, self.typeg, self.prc, self.q, self.min_fs, self.nbfl, self.nbfu, self.nbs, self.nbo = self.parameters[0], self.parameters[1], self.parameters[2], self.parameters[3], self.parameters[4], self.parameters[5], self.parameters[6], self.parameters[7], self.parameters[8], self.parameters[9]
                    # break
    
    def other_methods(self):
        """
        used to run methods
        """
        l = len(self.interval)
        for i in range(l):
            print(f"Copy graph for all the other methods : interval {i+1}/{l}")
            for g in self.dico[self.interval[i]]:
                g.generate_other_methods()
    
    def run_graph(self):
        """
        used to run methods
        """
        l = len(self.interval)
        for i in range(l):
            print(f"Run all the graphs : interval {i+1}/{l}")
            for g in self.dico[self.interval[i]]:
                g.run_all(self.interp)
              
    def print_str(self, force=False):
        """
        display
        """
        self.display += 1
        if self.display % self.aff == 0 or force:
            #res = f"{self.display}/{self.q} - {self.index_info+1}/{len(self.infos)}\n"
            res = f"{self.display}/{self.q}\n"
            res += "Posteriori "
            keys = list(self.dico.keys())
            for i in range(len(keys)):
                res += f"\033[31m{keys[i]}\033[00m:\033[32m{self.nbgr[i]}\033[00m / "
            res += "\n"
            print(res)
        
    # def put_in_graph(self, k):
    #     """
    #     free memory + put graphs in the tab
    #     """
    #     self.graphes = self.dico[k]
    #     del self.dico[k]
    
def value(nvalue):
    if nvalue == "PRC":
        interval = ['10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-85']
        #interval = ['40-44', '45-49']
    elif nvalue == "FCT":
        interval = ["2","3","4","5","6","7","8","9","10","15","20","25","30"]
    elif nvalue == "SRC":
        interval = ["10","20","30","50","100"]
    elif nvalue == "OBJ":
        interval = ["5","10","15","20","25","30","50","100"]
    return interval
    
if __name__ == "__main__":
    
    nvalue = "FCT"
    interval = value(nvalue)
    fixed_prc = fixed_prc = "25-29"
    
    sources = 20
    min_src = 10
    
    nbo = 10
    nbfl = 4
    nbfu = nbfl
    min_fs = 1
    
    infograph = f"{nbo};{sources};{nbfl};{nbfu}"
    
    typesg = 'ncpr'
    # typesg = 'cpr'
    
    #Number of methods (cf length of self.rg in graph_methods.py)
    nb_methods = constants.NB_METHODS
    
    name = "v4/results/"
    path_xp = "v4/generation/xp/"
    
    bl = 0
    bu = 100
    
    #number of graphes by interval
    nb_exp = 1000
    step = 4000
    stop = 1000000
    q = step
    aff = 1000
    
    priors = pr.Priors(len_prior=min_src, nbo=nbo, bmin=bl, bmax=bu)
    print("Priors generated.")
    
    print("Start generating Latex")
    m = metrics.Metrics(None)
    ltx = latex.Latex(nb_metrics=len(m.metrics), spe=m.n_methods["Mt"], path_f=name, 
                      nvalue=nvalue, fixed_prc=fixed_prc, infograph=infograph)
    ltx.new_section(m.metrics_name)
    
    prc = priors.percent[-1]
    
    exp = BruteForceExperiencesParameters(nb_exp=nb_exp, percentage=prc, 
                                     nbs=sources, nbo=nbo, nbfl=nbfl, 
                                     nbfu=nbfu, all_priors=priors, 
                                     typeg=typesg, min_fs=min_fs, 
                                     stop=stop, q=q, aff=aff, name=ltx.name, step=step,
                                     path_xp=path_xp,
                                     interval=interval, nvalue=nvalue, fixed_prc=fixed_prc)
    
    print(fixed_prc, "->", interval)
    
    exp.run()
