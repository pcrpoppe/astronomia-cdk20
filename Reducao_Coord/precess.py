"""
    ############################
    #                          # 
    #  Redução de Coordenadas  #
    #                          #
    ############################ 

    - Alpha deve ser escrito no formato hh:mm:ss, por exemplo: 10:8:22.2
    - Delta deve ser escrito no formato gg:mm:ss, por exemplo: 11º 58´ 2´´
    - Date deve ser escrito no formato DD:MM:AA, por exemplo: 12/3/1995
"""

import sys
import numpy as np
from precess_functions.calculus import coordReduction

def main():
    alpha = np.array([10, 8, 22.2])
    delta = np.array([11, 58, 2])
    date  = np.array([12, 3, 1995])

    coordReduction(alpha, delta, date)
    
if __name__ == '__main__':
    main()
