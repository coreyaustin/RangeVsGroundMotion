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

channels = ['L1:DMT-SNSH_EFFECTIVE_RANGE_MPC.mean',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_100M_300M.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_3_10.mean,m-trend']

start = 'June 16 2019 00:00:00 UTC'
end   = 'June 18 2019 23:00:00 UTC'

data = TimeSeriesDict.fetch(channels,start,end)
data.wri
range = data[channels[0]]

#%%
idx = np.where(range.value>120)
range  = range[idx]
useism = data[channels[1]][idx]
anthro = data[channels[2]][idx]
#%%
motion = np.arange(50,510,10)
avg_range = np.zeros(len(motion))
for i in xrange(len(motion)):
    index = np.where((anthro.value>motion[i]-25)&(anthro.value<motion[i]+25))
    avg_range[i] = np.mean(range[index].value)
    
#motion = np.arange(50,510,10)
#avg_range = np.zeros(len(motion))
#for i in xrange(len(motion)):
#    index = np.where((useism.value>motion[i]-25)&(useism.value<motion[i]+25))
#    avg_range[i] = np.mean(range[index].value)

for i in channels[1:]:
    
#%%
plt.scatter(motion,avg_range)
    


