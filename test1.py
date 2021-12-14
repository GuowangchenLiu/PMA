# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 23:20:37 2021

@author: king
"""
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing


matplotlib.rcParams['font.family']='STSong'# Italic' # 'STSong'
matplotlib.rcParams['font.size']=22


def ndsort(values1,values2):
    vlen = len(values1)
    S = [[] for i in range(0, vlen)]
    nn = [[] for i in range(0, vlen)]
    front = [[]]
    n = np.zeros(vlen)
    rank = np.zeros(vlen)
    for p in range(vlen):
        for q in range(vlen):
            if (values1[q] > values1[p] and values2[q] > values2[p]) or (  # p支配q
                    values1[q] >= values1[p] and values2[q] > values2[p]) or (
                    values1[q] > values1[p] and values2[q] >= values2[p]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[p] > values1[q] and values2[p] > values2[q]) or (  # q支配p
                    values1[p] >= values1[q] and values2[p] > values2[q]) or (
                    values1[p] > values1[q] and values2[p] >= values2[q]):
                n[p] += 1
                nn[p].append(q)
        if n[p] == 0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    # --------------
    i = 0
    while front[i] != []:
        Q = []
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if n[q] == 0:
                    rank[q] = i + 1
                    if q not in Q:
                        Q.append(q)
        i += 1
        front.append(Q)
    del front[len(front) - 1]
    return rank

def normalization(data):
    x = data-np.mean(data)
    y = x/np.max(np.abs(x))
    return y

def data():
    global data
    file = filedialog.askopenfilenames(initialdir=os.path.dirname(__file__))
    df = pd.read_excel(str(file)[2:-3])
    data = np.array(df)

    
def calculate():
    rankSources = ndsort(data[:,1],data[:,2])  # rank from 0
    rankPractices = ndsort(data[:,3],data[:,4])  # rank from 
    nSources = normalization(rankSources)
    nPractices = normalization(rankPractices)
    score = np.zeros((len(nSources),3))
    score[:,0] = nSources
    score[:,1] = nPractices

    for i in range(len(nSources)):
        if score[i,0] >= 0 and score[i,1] >= 0:
            score[i,2] = 1
        elif score[i,0] > 0 and score[i,1] < 0:
            score[i,2] = 2
        elif score[i,0] <= 0 and score[i,1] < 0:
            score[i,2] = 3
        elif score[i,0] < 0 and score[i,1] >= 0:
            score[i,2] = 4
    # plot
    plt.figure(figsize=(9, 7))
    plt.scatter(score[score[:,2]==1,1], score[score[:,2]==1,0],c = 'r',s = 50)
    plt.scatter(score[score[:,2]==2,1], score[score[:,2]==2,0],c = 'gold',s = 50)
    plt.scatter(score[score[:,2]==3,1], score[score[:,2]==3,0],c = 'darkblue',s = 50)
    plt.scatter(score[score[:,2]==4,1], score[score[:,2]==4,0],c = 'g',s = 50)
    plt.plot([-1.1,1.1], [0,0],color='gray',linewidth=2,linestyle='--')
    plt.plot([0,0], [-1.1,1.1],color='gray',linewidth=2,linestyle='--')
    plt.xlabel('Practices Score')
    plt.ylabel('Sources Score')
    # plt.xscale('log')
    # plt.yscale('log')
    plt.axis([-1.1,1.1,-1.1,1.1])
    markData = np.hstack((data[:,0:1],score))
    
    for x in markData:
        # print(i)
        if x[3] == 1:
            if x[0] == 32:
                plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]+0.01, x[1]+0.02), fontsize=22, fontweight="bold")
            else:
                plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]+0.01, x[1]+0.05), fontsize=22, fontweight="bold")
        elif x[3] == 2:
            plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]-0.1, x[1]+0.05), fontsize=22, fontweight="bold")    
            
        elif x[3] == 3:
            if x[0] == 30:
                plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]+0.01, x[1]+0.02), fontsize=22, fontweight="bold")        
            else:
                plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]-0.11, x[1]-0.05), fontsize=22, fontweight="bold")    
    
        elif x[3] == 4:
            if x[0] == 29:
                plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]+0.01, x[1]+0.02), fontsize=22, fontweight="bold")        
            else:
                plt.annotate(int(x[0]), xy = (x[2], x[1]),xytext = (x[2]-0.05, x[1]-0.12), fontsize=22, fontweight="bold")    
               
    plt.grid(False)
    plt.show()

def clear():
    pass

def main():
    global root, f, f_plot, canvs
    root = Tk()
    root.geometry("900x800")
    root.title("WQM-MD calculator v.1.0")
    f = Figure(figsize=(9, 7), dpi=100)
    f_plot = f.add_subplot(111)
    canvs = FigureCanvasTkAgg(f, root)
    canvs.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=10, sticky="nesw")
    # label
    Label(root, text="the number of dimensions:").grid(row=4,column=1)
    # combo
    combo = Combobox(root)
    combo['values'] = (4,5,6,7,8,"Text")
    combo.current(0)
    combo.grid(row=4,column=2)
    Button(root, text="add data",command=data).grid(row=4, column=6)
    Button(root, text='calculate', command=calculate).grid(row=4, column=7)
    Button(root, text='clear', command=clear).grid(row=4, column=8)
    root.mainloop()
if __name__ == '__main__':
    main()