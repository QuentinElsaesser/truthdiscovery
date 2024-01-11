from v4.generation import priors as pr
from v4.generation import metrics, latex, random_graph
from v4.generation import brutefrc_exp_para as bfexp
from v4.generation import graph_methods as gm

from v4.vote import plurality as voting

from v4.constants import constants

import os, sys

from copy import deepcopy

class ReadXP:
    def __init__(self, path, option=1):
        """
        Read file in path and run algorithm on the graphs in the file
        option : number for the scoring rule for the first graph that will be duplicate
        """
        self.f = open(path, "r")
        print(f"read {path}")
        lines = self.f.readlines()
        
        header = lines[0].strip().split(";")
        
        indtypeg = header.index("TYPEG")
        indnbo = header.index("NB_OBJ")
        indnbs = header.index("NB_SRC")
        indnbfl = header.index("NB_FL")
        indnbfu = header.index("NB_FU")
        indnbf = header.index("NBF")
        indtrust = header.index("TRUST")
        # indnorma = header.index("NORMA")
        normalization = constants.NORMA_A
        indsf = header.index("SF")
        indof = header.index("OF")
        indtruth = header.index("TRUTH")
        for i in range(len(header)):
            if header[i].startswith("INTERVAL"):
                indintv = i
                self.interval = header[indintv][len("INTERVAL:"):].strip().split("/")[:-1]
                break
            else:
                indintv = -1
        
        #type of gen + percent
        type_gen = header[-1].split("_")
        self.nvalue = type_gen[0]
        self.fixed_prc = type_gen[1]
       
        lines = lines[1:]
        self.dico = dict()
        self.exp = None
        
        # self.spe_metric = []
        
        taille = len(lines)
        
        ind = 0
        l_intv = ""
        normalization = constants.NORMA_A
        first = True
        
        for i,l in enumerate(lines):            
            print(f"creation graph {i}/{taille}")
            tmp = l.split(";")
            
            self.typeg = tmp[indtypeg]
            self.nbo = int(tmp[indnbo])
            self.nbs = int(tmp[indnbs])
            self.nbfl = int(tmp[indnbfl])
            self.nbfu = int(tmp[indnbfu])
            nbf = int(tmp[indnbf])
            
            if first:
                infograph = f"{self.nbo};{self.nbs};{self.nbfl};{self.nbfu}"
                # self.interval = tmp[indintv].strip().split("/")[:-1]
                for intv in self.interval:
                    self.dico[intv] = []
                first = False
            
            intv, _ = self.find_intv_para(trust=int(tmp[indtrust]), nbf=nbf, nbo=self.nbo, nbs=self.nbs)
            if l_intv != intv:
                ind = 0            
                l_intv = intv
            prior = [0 for s in range(self.nbs)]
            
            tmpsf = tmp[indsf].split("-")
            sf = []
            for j in range(len(tmpsf)):
                tmps = [0 for f in range(nbf)]
                elts = tmpsf[j].split(",")
                for index in elts:
                    tmps[int(index)] = 1
                sf.append(tmps)
                # sf.append(list(map(int, l.split(","))))

            tmpof = tmp[indof].split("-")
            of = []
            for j in range(len(tmpof)):
                tmpo = [0 for f in range(nbf)]
                elts = tmpof[j].split(",")
                for index in elts:
                    tmpo[int(index)] = 1
                of.append(tmpo)

            truth = []
            tmptrue = tmp[indtruth].split("-")
            curr_id = 0
            length = len(tmptrue)
            for f in range(nbf):
                if curr_id < length and int(tmptrue[curr_id]) == f:
                    truth.append(1)
                    curr_id += 1
                else:
                    truth.append(0)

            self.dico[intv].append(gm.GraphMethods(prior, nbo=self.nbo, nbfl=self.nbfl, \
                                  nbfu=self.nbfu, nbs=self.nbs, typeg=self.typeg, \
                                  min_fs=1, allg=False))

            rg = random_graph.randomGraph(voting.Plurality, option, 
                              nbo=self.nbo, nbfl=self.nbfl, nbfu=self.nbfu, nbs=self.nbs, 
                            norma=normalization, prior=prior, typeg=self.typeg, min_fs=1,
                            sf=sf, of=of, truth=truth)
            
            self.dico[intv][ind].add_rg(rg)
            ind += 1
                
        nb_exp = len(self.dico[intv])

        priors = pr.Priors(len_prior=5, nbo=10, bmin=0, bmax=100)
        print("Priors generated.")
        
        print("Start generating Latex")
        m = metrics.Metrics(None)
        ltx = latex.Latex(nb_metrics=len(m.metrics), spe=m.n_methods["Mt"], path_f=constants.PATH_RESULTS, 
                          nvalue=self.nvalue, fixed_prc=self.fixed_prc, infograph=infograph, readname=path.split("/")[-1].split("xp")[0])
        ltx.new_section(m.metrics_name)
        
        prc = priors.percent[-1]
        
        self.exp = bfexp.BruteForceExperiencesParameters(nb_exp=nb_exp, percentage=prc, 
                                          nbs=self.nbs, nbo=self.nbo, nbfl=self.nbfl, 
                                          nbfu=self.nbfu, all_priors=priors, 
                                          typeg='ncpr', min_fs=1, 
                                          stop=1000000, q=1000, aff=100, 
                                          name=ltx.name, step=1000,
                                          path_xp=constants.PATH_XP, read=True,
                                          interval=self.interval, nvalue=self.nvalue, 
                                          fixed_prc=self.fixed_prc)
        
        self.exp.interval = self.interval
        self.exp.dico = self.dico
        
        self.exp.other_methods()
        self.exp.run_graph()
        
        nbg = 0
        for prc in self.exp.interval:
            if self.nvalue == "SRC":
                self.nbs = prc
            ltx.new_subsection(prc, nb_exp, m, self.exp.fixed_prc)
            #don't delete the graph to check the graphs
            #exp.put_in_graph(prc)
            self.exp.graphes = self.exp.dico[prc]
            m = metrics.Metrics(self.exp)
            for i in range(len(m.metrics)):
                m.metrics[i]()
                ltx.body_tab(metric=m, typeg=self.typeg, nbs=self.nbs)
                # if m.n == constants.ID_METRICS["Mt"]:
                    # uniquement pour la plurality
                #     self.spe_metric.append((m.spe_metric.trust[0], m.spe_metric.proba[0], m.spe_metric.difference[0]))
            nbg += 1
            print(f"Writing interval {nbg}/{len(self.exp.interval)}")
            ltx.end_tab()
        ltx.combined()
        ltx.write()

        self.f.close()
        
        
        #name = ltx.name;base_dir = f"{constants.PATH_PNG}{name.split('/')[-1].split('.')[0]}/"
        #directorypng = self.name_directory(base_dir)
        #m = metrics.Metrics(None)
        #self.generate_plot(name=name, metric=m, directory=directorypng)
        
    def name_directory(self, directory):
        name = directory
        nbf = 0
        while os.path.exists(name):
            nbf += 1
            name = f"{directory[:-1]}-{nbf}/"
        return name
    
    # def generate_plot(self, name, metric, directory):
    #     """
    #     for each metric, read the file with the result and create the png
    #     """
    #     print("Start generating Plot")
    #     for i in range(len(metric.id_methods)):
    #         ind = metric.n_methods[metric.id_methods[i]]
    #         if i not in [constants.ID_METRICS["Ia"]]:#dont create the plot for some metrics
    #             myplot = plot.Plot(name=name, index_m=ind, metric_name=metric.metrics_name[ind], spe=metric.n_methods["Mt"], directory=directory, cut=False)
    #             myplot.plot_all()
    #         else:
    #             print("main_generate.py -> IGNORE", metric.metrics_name[ind])
    #     print("done")
        
    def find_intv_para(self, trust, nbf, nbo, nbs):
        if self.nvalue == "PRC":
            return self.find_intv_prc(trust)
        elif self.nvalue == "FCT":
            return self.find_intv_elt(int(nbf/nbo), trust)
        elif self.nvalue == "OBJ":
            return self.find_intv_elt(nbo, trust)
        elif self.nvalue == "SRC":
            return self.find_intv_elt(nbs, trust)
        elif self.nvalue == "PRP":
            return self.find_intv_prc(trust)
            # return self.fixed_prc_prp, 0
        
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
        
if __name__ == "__main__":
    n = 1
    nvalue = ""
    #nvalue = "src"
    nvalue = "fct"
    option = 1
    ####prp:
    #nvalue = "prp"; 
    n = int(sys.argv[1])
    ####
    name = f"res{n}xp0{nvalue}.csv"
    readxp = ReadXP(f"{constants.PATH_XP}{name}", option=option)
    
