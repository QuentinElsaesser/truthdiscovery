import os

from v4.constants import constants

class Latex:
    def __init__(self, nb_metrics, spe, path_f="../results/", nvalue="PRC", fixed_prc="", infograph="", readname=""):
        """
        in ../results : save the results in latex
        
        each metric will be a section
        each percent will be a subsection
        each nbs will be a line in a tab
        """
        self.lxt = ""
        self.nb_metrics = nb_metrics
        self.section = ["" for i in range(nb_metrics)]
        
        self.spe = spe
        
        self.nvalue = nvalue
        self.fixed_prc = ""
        # if fixed_prc == "":
            # self.fixed_prc = ""
        # else:    
        #     self.fixed_prc = f"_{fixed_prc}\%"
        
        self.infograph = infograph.split(";")
        if self.nvalue == "SRC":
            self.infograph = self.infograph[:1]+self.infograph[2:]
        elif self.nvalue == "FCT":
            self.infograph = self.infograph[:2]
        elif self.nvalue == "OBJ":
            self.infograph = self.infograph[1:]
        self.infograph = ";".join(self.infograph)
        
        nbf = 0
        if readname == "":
            name = f"{path_f}res0.tex"
            while os.path.isfile(name):
                nbf += 1
                name = f"{path_f}res{nbf}.tex"
            f = open(name, "w")
            print(f"Create file {name}")
            f.close()
        else:
            name = f"{path_f}{readname}.tex"
            while os.path.isfile(name):
                nbf += 1
                name = f"{path_f}{readname}_{nbf}.tex"
            f = open(name, "w")
            print(f"Create file {name} from {path_f}{readname}")
            f.close()
        self.name = name
        
        self.start_file()
        
    def texte(self, prc, fixed_prc, first):
        if self.nvalue == "PRC" or self.nvalue == "PRP":
            return f"{prc}\%"
        else:
            if self.nvalue == "FCT":
                txt = "fct"
            elif self.nvalue == "SRC":
                txt = "src"
            elif self.nvalue == "OBJ":
                txt = "obj"
            return f"{prc}{txt}" if first else f"{prc}{txt} with {fixed_prc}\%"
        
    def write(self):
        """
        creation of the file and write the results
        """
        f = open(self.name, "w")
        print(f"Write results in {self.name}")
        f.write(self.lxt)
        f.close()
        self.ltx = ""
        print("done")

    def combined(self):
        """
        merge all the section in one
        end file
        """
        for i in range(len(self.section)):
            self.lxt += self.section[i]
            self.section[i] = ""
        self.end_file()
        
    def start_file(self):
        """
        head of document
        """
        tmp = ""
        for o in constants.ORDER:
            if o in constants.RUN_METHODS:
                tmp += f"{o};"
        self.lxt = "\\documentclass{article}\n"
        self.lxt += "\\usepackage[utf8]{inputenc}\n"
        self.lxt += "\\usepackage{graphicx}\n"
        self.lxt += "\\usepackage{booktabs}\n"
        self.lxt += "\\newcommand{\\graph}[2]{$G_{#1}^{#2}$}\n"
        self.lxt += "\\newcommand{\\typegeneration}[0]{" + self.nvalue + self.fixed_prc + "}\n"
        self.lxt += "\\newcommand{\\infograph}[0]{" + self.infograph + "}\n"
        self.lxt += "\\author{quentin elsaesser}\n\n"
        self.lxt += "\\title{" + tmp[:-1] + "}\n\n"
        self.lxt += "\\begin{document}\n\n\\newpage\n\n"
        
    def end_file(self):
        """
        end of document
        """
        self.lxt += "\\end{document}\n"
            
    def new_section(self, metrics_name):
        """
        new section
        """
        for i in range(self.nb_metrics):
            self.section[i] += "\\newpage\n\\section{Metric : "+metrics_name[i]+"}\n\n\\newpage\n"
    
    def new_subsection(self, prc, nb_exp, metric, fixed_prc):
        """
        new subsection
        header for tabular 
        """
        for i in range(self.nb_metrics):
            if i == self.spe:
                self.section[i] += "\\newpage\n"
            
            # self.section[i] += "\n\\subsection{"+f"{prc}\%"+"}\n\n"
            self.section[i] += "\n\\subsection{"+f"{self.texte(prc, fixed_prc, True)}"+"}\n\n"

            
            if i != self.spe:
                # self.section[i] += f"{prc}\% with {nb_exp} experiences for metric {metric.metrics_name[i]}.\n"
                self.section[i] += f"{self.texte(prc, fixed_prc, True)} with {nb_exp} experiences for metric {metric.metrics_name[i]}.\n"
                self.section[i] += "\n"
                self.section[i] += "\\noindent\\begin{tabular}{|l|" + "c|"*constants.NB_METHODS + "}\n"
                self.section[i] += "\\hline\n"
                for n in constants.ORDER:
                    self.section[i] += f"& {n}"
                self.section[i] += "\\\\\n"
                # self.section[i] += f"& Plurality {self.normaA} & Plurality {self.normaO} & Borda {self.normaA} & Borda {self.normaO} & TF & H\&A & Sums & U-Sums & Voting\\\\\n"
                self.section[i] += "\\hline\n"
        
    def body_tab(self, metric, typeg, nbs):
        """
        body of tabular
        """
        if metric.n == self.spe:
            self.section[metric.n] += metric.spe_metric.generate_latex_body()
        else:
            resstr = self.find_best(metric)
            # self.section[metric.n] += "\graph{"+typeg+"}{"+str(nbs)+"} &"+resstr[0]+"&"+resstr[1]+"&"+resstr[2]+"&"+resstr[3]+"&"+resstr[7]+"&"+resstr[6]+"&"+resstr[4]+"&"+resstr[5]+"&"+resstr[8]+"\\\\\n"
            self.section[metric.n] += "\graph{"+typeg+"}{"+str(nbs)+"} "
            for i in range(constants.NB_METHODS):
                self.section[metric.n] += f"&{resstr[i]}"
            self.section[metric.n] += "\\\\\n"
            self.section[metric.n] += "\\hline\n"
        
    def end_tab(self):
        """
        end of tabular
        """
        for i in range(self.nb_metrics):
            if i != self.spe:
                self.section[i] += "\\end{tabular}\n\\newpage\n"
    
    def new_sources_tab(self):
        """
        new number of sources in tabular
        """
        for i in range(self.nb_metrics):
            if i == self.spe:
                self.section[i] += "\\newpage\n"
            else:
                self.section[i] += "\\hline\n"
        
    def find_best(self, metric):
        """
        return the list with the best result depending on the metric.mini value
        """
        maxi = metric.res[0]
        ind = [0]
        length = range(1,constants.NB_METHODS) if metric.n in list(constants.ID_METRICS_TD.values()) else constants.ID_METHODS_SOURCES[1:]
        for i in length:
            if (not metric.mini and metric.res[i] > maxi) or (metric.mini and metric.res[i] < maxi):
                maxi = metric.res[i]
                ind = [i]
            elif metric.res[i] == maxi:
                ind.append(i)
        if not metric.mini and maxi == 0:
            ind = []
        
        resstr = []
        for i in range(len(metric.res)):
            if i in ind:
                resstr.append("\\textbf{"+str(round(metric.res[i],3))+"}")
            else:
                resstr.append(str(round(metric.res[i],3)))
        return resstr
    