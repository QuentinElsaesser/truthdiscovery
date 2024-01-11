from v4.constants import constants

import numpy as np

class Normalize:
    def __init__(self, name):
        """
        O is the C in the article
        """
        self.name = name
        if self.name != constants.NORMA_A and self.name != constants.NORMA_O:
            raise ValueError(f"{self.name} = Unknown normalization")
        
    def run_normalize(self, G, i):
        if self.name == constants.NORMA_A:
            return self.norma_A(G, i)
        elif self.name == constants.NORMA_O:
            return self.norma_O(G, i)
        
    def norma_A(self, G, i):
        """
        i : index of the sources
        """
        return G.trust_s[i] / (len(G.mat_of) * G.obj.voting_met.max_value)

    def norma_O(self, G, i):
        """
        i : index of the sources
        """
        n = np.count_nonzero(G.sf[i] == 1)
        if n == 0:
            return 0
        return G.trust_s[i] / (n * G.obj.voting_met.max_value)
