# -*- coding: utf-8 -*-
"""
@author:A.Ç.SEÇKİN
seckin.ac@gmail.com
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
path = "fabricCombinations"
files = os.listdir(path)
files=sorted(files)
files_xls = [f for f in files if f[-4:] == '.csv']

dataframes = []
types=[]
for i, filename in enumerate(files_xls):
    print(filename)
    df = pd.read_csv(path+"/"+filename,delimiter=";") # additional arguments up to your need
    r,c=df.shape
    df['fabric'] = filename[0:-4]
    
    offset=df.iloc[0,0:-1].values
    fo=find_peaks(offset, distance=100,height=np.mean(offset)*3/2)
    
    fd_list=[]
    fd_max=[]
    pa_list=[]
    sd_list=[]
    sd_max=[]
    dpow=[]
    touch=[]
    for i in range(0,r):
        cs=df.iloc[i,0:-1].values
        fc=find_peaks(cs, distance=50,height=np.mean(cs)*3/2)
        fd=np.abs(fc[0]-fo[0])
        pa=np.sum(fd>1)
        so=offset[fc[0]]
        sc=cs[fc[0]]
        sd=sc-so
        fd_list.append(fd)
        fd_max.append(np.max(fd))
        pa_list.append(pa)
        sd_list.append(sd)
        sd_max.append(np.max(sd))
        dpow.append(np.mean(np.abs(cs-offset)))
        if ((dpow[-1]>21) & (fd_max[-1]>3) & (pa>3) & (sd_max[-1]>60)):
            touch.append(1)
        else:
            touch.append(0)
            
    df['dpow'] = dpow
    df['fd_max'] = fd_max
    df['sd_max'] = sd_max
    df['pa'] = pa_list
    df['touch'] = touch
    
    fd_list=np.array(fd_list)
    
    for cn in range(16):
        df['fd_'+str(cn)] = fd_list[:,cn]
        df['fd_'+str(cn)]=df['fd_'+str(cn)].astype(float)
    sd_list=np.array(sd_list)
    for cn in range(16):
        df['sd_'+str(cn)] = sd_list[:,cn]
        df['sd_'+str(cn)]=df['sd_'+str(cn)].astype(float)
    dataframes.append(df)
    types.append(filename[0:-4])

alldata = pd.concat(dataframes)
alldata.to_csv("alldata.csv", sep=';', encoding='utf-8',float_format='%.3f',decimal=",")


xticks_lbl=alldata['fabric'].values
touch_lbl=alldata['touch'].values>0

plt.close('all')

fig=plt.figure()
fig.suptitle('Fabric Voltage Change', fontsize=16)
dpow=alldata['dpow'].values
dpow_peaks, _ = find_peaks(dpow, height=20.8)
plt.plot(dpow)
plt.plot(dpow_peaks, dpow[dpow_peaks], "x")
plt.plot(touch_lbl*dpow, "o", alpha=0.7)
plt.ylim(18,30)
plt.xticks( np.arange(0,len(dpow),10), xticks_lbl[np.arange(0,len(dpow),10)],rotation = 90)
plt.grid()


fig=plt.figure()
fig.suptitle('Fabric Frequency Change', fontsize=16)
fd_max=alldata['fd_max'].values
fd_max_peaks, _ = find_peaks(fd_max, height=4)
plt.plot(fd_max)
plt.plot(fd_max_peaks, fd_max[fd_max_peaks], "x")
plt.plot(touch_lbl*fd_max, "o", alpha=0.7)
plt.xticks( np.arange(0,len(dpow),10), xticks_lbl[np.arange(0,len(dpow),10)],rotation = 90)
plt.grid()


fig=plt.figure()
fig.suptitle('Fabric max Frequency-Voltage Change', fontsize=16)
sd_max=alldata['sd_max'].values
sd_max_peaks, _ = find_peaks(sd_max, height=80)
plt.plot(sd_max)
plt.plot(sd_max_peaks, sd_max[sd_max_peaks], "x")
plt.plot(touch_lbl*sd_max, "o", alpha=0.7)
plt.xticks( np.arange(0,len(dpow),10), xticks_lbl[np.arange(0,len(dpow),10)],rotation = 90)
plt.grid()


fig=plt.figure()
fig.suptitle('Fabric max pa Change', fontsize=16)
pa=alldata['pa'].values
pa_peaks, _ = find_peaks(pa, height=6)
plt.plot(pa)
plt.plot(pa_peaks, pa[pa_peaks], "x")
plt.plot(touch_lbl*pa, "o", alpha=0.7)
plt.xticks( np.arange(0,len(dpow),10), xticks_lbl[np.arange(0,len(dpow),10)],rotation = 90)
plt.grid()


m_std_pp=[]
m_std_idx=[]
m_pp=[]
m_idx=[]


for ty in types:
    plt.close('all')
    fig, axs = plt.subplots(2,8, figsize=(20, 6))
    plt.tight_layout()
    fig2, axs2 = plt.subplots(2, figsize=(8, 6))
    plt.tight_layout()
    fig.suptitle(ty)
    fig2.suptitle(ty)
    
    a=alldata.loc[alldata['source'] == ty]
    fir=a.iloc[0,:-1].to_numpy()
    rem=a.iloc[1:,:-1].to_numpy()
    diff=np.zeros((len(rem),3200))
    for i in range(len(rem)):
        diff[i]=rem[i]-fir
    
    i=0
    maxmindis=[]
    ppvals=[]
    for r in range(2):
        for c in range(8):
            for k in range(len(rem)):
                axs[r,c].plot(rem[k,i*200:(i*200)+200],"g")
                darray=diff[k,i*200:(i*200)+200]
                axs[r,c].plot(darray,"b")
                maxi=np.argmax(darray)
                mini=np.argmin(darray)
                maxv=darray[maxi]
                minv=darray[mini]
                idis=maxi-mini
                pp=maxv-minv
                ppvals.append(pp)
                maxmindis.append(idis)
                print(i,k,idis,pp)
            axs[r,c].plot(fir[i*200:(i*200)+200],"r")
            axs[r,c].set_title('Ch'+str(i))
            axs[r,c].grid()
            i=i+1
    
    axs2[0].plot(maxmindis,"r")
    axs2[0].set_title('Argmax-Argmin')
    axs2[0].grid()
    axs2[1].plot(ppvals,"r")
    axs2[1].set_title('Peak to Peak')
    axs2[1].grid()

    
    
    m_std_pp.append(np.std(ppvals))
    m_std_idx.append(np.std(maxmindis))
    m_pp.append(np.max(ppvals))
    m_idx.append(np.max(maxmindis))
    
        
    fig.savefig("CH_"+str(ty)+".svg") 
    fig2.savefig("DI_"+str(ty)+".svg") 

fig3, axs3 = plt.subplots(2, figsize=(10, 10))
axs3[0].plot(types,m_std_pp,label='std peak to peak value')
axs3[0].plot(types,m_std_idx,label='std index index distances')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.grid()
plt.legend()

axs4 = axs3[0].twinx() 
axs4.plot(types,np.array(m_std_pp)*np.array(m_std_idx),label='std multiplication',c="r")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.grid()
plt.legend()

axs3[1].plot(types,m_pp,label='max peak to peak value')
axs3[1].plot(types,m_idx,label='max index distance')
plt.xticks(rotation = 90)
plt.tight_layout()
plt.grid()
plt.legend()

axs5 = axs3[1].twinx() 
axs5.plot(types,np.array(m_pp)*np.array(m_idx),label='std multiplication',c="r")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.grid()
plt.legend()


plt.xticks(rotation = 90)
plt.tight_layout()
plt.grid()
plt.legend()
