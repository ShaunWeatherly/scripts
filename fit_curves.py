'''
// Script for extracting data from text files and fitting them to curves.
//
// Example use case:
//
// >>> from fit_curves import TDL
// >>>
// >>> fit = TDL()
// >>> fit.read(read_path="file1.log", name="Set1")
// >>> fit.read(read_path="file2.log", name="Set2")
// >>> fit.gen_plot(save_name="my_plot")
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re

class TDL:
    
    def __init__(self, filepath = None):
        
        self.Nks = []
        self.Ecorrs = []
        self.legend_entries = []
        self.filepath = filepath
    
    def generate(self, save_name=None):
        
        #This is the function to which the datapoints will be fitted to.
        def func(Nk, E, α, β):
                return (E + α*(Nk**(-1.0)) + β*(Nk**(-2.0)))
            
        plt.xlabel('N kpt')
        plt.ylabel('Ecorr (Ha)')
        
        #Sets up range of colors for lines and markers
        color = iter(plt.cm.rainbow(np.linspace(0, 1, len(self.Nks))))
        
        for row in range(len(self.Nks)):
            c = next(color)
            Nk = np.array(self.Nks[row])
            Ecorr = np.array(self.Ecorrs[row])
            filename = self.legend_entries[row]
            xspace=np.linspace(1,Nk[-1],500)
            popt, pcov = curve_fit(func, Nk, Ecorr)
            
            plt.plot(xspace, func(xspace, *popt), color=c, label='TDL Extrapolation: E=%5.3f, α=%5.4f, β=%5.5f' % tuple(popt))
            plt.scatter(Nk, Ecorr, color=c, label=filename)
            plt.legend()
            
            ###Plan to add error bar functionality
            #pcov = np.sqrt(np.diag(pcov))
            #plt.errorbar(xspace, func(xspace, *popt), fmt='none', yerr=perr)
        
        if save_name != None:
            plt.savefig(f"{save_name}.png", dpi=300, pad_inches=0.1, bbox_inches='tight')
        else: 
            plt.savefig(f"no_name.png", dpi=300, pad_inches=0.1, bbox_inches='tight')

    def read(self, readpath=None, name=None):
        
        if readpath != None:
            filepath = readpath
        elif self.filepath != None:
            filepath = self.filepath
        else:
            print("Error: Please specify a file path when calling 'read', for example: >>> read(readpath='path/to/file.txt')")
        if name != None:
            filename = name
        else:
            filename = self.filepath
        
        Nk = []
        Ecorr = []
        Nk_lines = []
        Ecorr_lines = []

        with open(filepath, 'r') as f:
            print(f"Reading from {filepath}...")
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
        
        self.Nks.append(Nk)
        self.Ecorrs.append(Ecorr)
        self.legend_entries.append(filename)
        
        print(self.Nks)
        print(self.Ecorrs)
        print(self.legend_entries)
        print("Done.")

fit = TDL()
fit.read("kh2_d_1000.log")
fit.generate()