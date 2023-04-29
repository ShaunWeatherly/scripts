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
    
    ###Quick scatter plot
    def quickplot(self, save_name=None):
        
        #Specify color pallet for lines and markers
        color = iter(plt.cm.rainbow(np.linspace(0, 1, len(self.Nks))))
        
        for row in range(len(self.Nks)):
            c = next(color)
            Nk = np.array(self.Nks[row])
            Ecorr = np.array(self.Ecorrs[row])
            filename = self.legend_entries[row]

            plt.scatter(Nk, Ecorr, color=c, label=filename)
            plt.legend()

        if save_name != None:
            plt.savefig(f"{save_name}.png", dpi=300, pad_inches=0.1, bbox_inches='tight')
        else: 
            plt.savefig(f"no_name.png", dpi=300, pad_inches=0.1, bbox_inches='tight')
            
    def generate(self, save_name=None):
        
        # This is the function to which the datapoints will be fitted to.
        def func(Nk, E, α, β):
                return (E + α*(Nk**(-1.0)) + β*(Nk**(-2.0)))
        
        plt.xlabel('N kpt')
        plt.ylabel('Ecorr (Ha)')
        
        # Specify color pallet for lines and markers
        color = iter(plt.cm.rainbow(np.linspace(0, 1, len(self.Nks))))
        
        for row in range(len(self.Nks)):
            c = next(color)
            Nk = np.array(self.Nks[row])
            Ecorr = np.array(self.Ecorrs[row])
            filename = self.legend_entries[row]
            xspace=np.linspace(1,Nk[-1],500)
            popt, pcov = curve_fit(func, Nk, Ecorr)
            
            plt.plot(xspace, func(xspace, *popt), color=c) #label='Extrap.: E=%5.3f, α=%5.4f, β=%5.5f' % tuple(popt))
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
            filename = filepath
        
        Nk = []
        Ecorr = []
        Nk_lines = []
        Ecorr_lines = []

        with open(filepath, 'r') as f:
            print(f"Reading from {filepath}...")
            text = f.readlines()
            for i in range(0,len(text),1):
                if re.search("Time elapsed = ", text[i]):
                    print(f"Found at line: {i}")
                    Ecorr_lines.append(int(i))
                
                elif re.search("Sweep =", text[i]):
                    Nk_lines.append(int(i))

            if len(Ecorr_lines) == 0:
                print(f"'CONVERGED' could not be found in file {filepath}")
            else:
                for i in Ecorr_lines:
                    temp=[]
                    word_list = text[i].split()
                    for word in word_list:
                        if re.search("[0-9]", word):
                            temp.append(word)
                            print(temp)
                    Ecorr.append(float(temp[1]))
                for i in Nk_lines:
                    temp=[]
                    word_list = text[i].split()
                    for word in word_list:
                        if re.search("[0-9]", word):
                            temp.append(word)
                    Nk.append(float(temp[0]))
            print(Nk)
            print(Ecorr)
        self.Nks.append(Nk)
        self.Ecorrs.append(Ecorr)
        self.legend_entries.append(filename)
        
        print("Done.")
        
