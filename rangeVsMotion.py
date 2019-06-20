#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:46:46 2019

@author: coreyaustin
"""
#%%
from gwpy.timeseries import TimeSeriesDict
from matplotlib import pyplot as plt
import numpy as np
from os import path

class rangeData:
    
    default_start = 'June 16 2019 00:00:00 UTC'
    default_end   = 'June 18 2019 23:00:00 UTC'
    
    def __init__(self,channels,filename,start=default_start,end=default_end):
        self.channels = channels
        if path.exists('./data/{}.hdf5'.format(filename)):
            self.data = TimeSeriesDict.read('./data/{}.hdf5'.format(filename))
        else:
            self.data = TimeSeriesDict.fetch(channels,start,end)
            self.data.write('./data/{}.hdf5'.format(filename))
            
    def cullGlitches(self):
        range = self.data[self.channels[0]]
        index = np.where(range.value>120)
        for i in self.channels:
            self.data[i] = self.data[i][index]
        
        
    def averageRange(self,motion):
        for i in self.channels[1:]:
            self.data[i].avg_range = np.zeros(len(motion))
            for j in xrange(len(motion)):
                idx = np.where((self.data[i].value>motion[j]-25)&(self.data[i].value<motion[j]+25))
                self.data[i].avg_range[j] = np.mean(self.data[self.channels[0]][idx].value)
        
        
    
#%%
channels = ['L1:DMT-SNSH_EFFECTIVE_RANGE_MPC.mean',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_100M_300M.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_3_10.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_X_BLRMS_100M_300M.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_X_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_X_BLRMS_3_10.mean,m-trend',
            'L1:ISI-GND_STS_ITMY_Z_BLRMS_100M_300M.mean,m-trend',
            'L1:ISI-GND_STS_ITMY_Z_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ITMY_Z_BLRMS_3_10.mean,m-trend']

start = 'June 11 2019 00:00:00 UTC'
end   = 'June 18 2019 23:00:00 UTC'

filename = '190611_to_190618_data'

motion = np.arange(50,1000,10)

noise = rangeData(channels,filename,start=start,end=end)
noise.cullGlitches()
noise.averageRange(motion)
    
#%%
plt.rcParams.update({'text.usetex': False})
fig, axes = plt.subplots(3,3,sharex=True,sharey=True,figsize=[16*1.5,9*1.5])

for i in range(3):
    for j in range(3):
        index = (i * 3) + j + 1
        axes[i,j].scatter(motion,noise.data[channels[index]].avg_range)
        axes[i,j].set_title(channels[index][15:-13],fontsize=16)
axes[0,0].set_ylim([125,140])
for ax in axes.flat:
    ax.set(xlabel='Ground Motion (nm/s)',ylabel='Range (Mpc)')    
    ax.label_outer()


