import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re

def TDL_fit(Nk, Ecorr):
    
    def func(Nk, E, α, β):
        return (E + α*(Nk**(-1.0)) + β*(Nk**(-2.0)))
    
    xspace=np.linspace(1,Nk[-1],500)
    plt.plot(Nk, Ecorr, 'co', label='Datapoints')
    popt, pcov = curve_fit(func, Nk, Ecorr)
    plt.plot(xspace, func(xspace, *popt), 'k--', label='TDL Extrapolation: E=%5.3f, α=%5.4f, β=%5.5f' % tuple(popt))
    
    plt.xlabel('N kpt')
    plt.ylabel('Ecorr (Ha)')
    plt.legend()
    plt.show()

def read(filepath):
    print(f"Reading from {filepath}...")
    Nk = []
    Ecorr = []
    Nk_lines = []
    Ecorr_lines = []
    
    with open(filepath, 'r') as f:
        text = f.readlines()
        for line in text:
            if line.find("BE took") != -1:
                Ecorr_lines.append(int(text.index(line) - 6))
            if line.find("N kpts") != -1:
                Nk_lines.append(int(text.index(line)))
        
        if len(Ecorr_lines) == 0:
            print(f"'CONVERGED' could not be found in file {filepath}")
        else:
            for i in Ecorr_lines:
                word_list = text[i].split()
                for word in word_list:
                    if re.search("[0-9]", word):
                        Ecorr.append(float(word))
            for i in Nk_lines:
                word_list = text[i].split()
                for word in word_list:
                    if re.search("[0-9]", word):
                        Nk.append(float(word))
    
    print("Done.")
    return np.array(Nk), np.array(Ecorr)

