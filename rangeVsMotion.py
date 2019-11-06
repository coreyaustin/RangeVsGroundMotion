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

plt.rcParams.update({'text.usetex': False})
#%%

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
        index = np.where(range.value>100)
        for i in self.channels:
            self.data[i] = self.data[i][index]
        
        
    def averageRange(self,motion):
        for i in self.channels[1:]:
            self.data[i].avg_range = np.zeros(len(motion))
            for j in xrange(len(motion)):
                idx = np.where((self.data[i].value>motion[j]-25)&(self.data[i].value<motion[j]+25))
                self.data[i].avg_range[j] = np.mean(self.data[self.channels[0]][idx].value)
                
    def normRange(self):
        for i in self.channels:
            self.data[i].mean = np.mean(self.data[i].value)
            self.data[i].norm = self.data[i]/self.data[i].mean
        
        
    
#%%
channels = ['L1:DMT-SNSH_EFFECTIVE_RANGE_MPC.mean',
            'L1:OAF-RANGE_RLP_3_OUT16.mean,m-trend',
            'L1:OAF-RANGE_RLP_2_OUT16.mean,m-trend',
            'L1:OAF-RANGE_RLP_1_OUT16.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Y_BLRMS_3_10.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Z_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMY_Z_BLRMS_3_10.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_X_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_X_BLRMS_3_10.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_Z_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ETMX_Z_BLRMS_3_10.mean,m-trend',
            'L1:ISI-GND_STS_ITMY_Z_BLRMS_1_3.mean,m-trend',
            'L1:ISI-GND_STS_ITMY_Z_BLRMS_3_10.mean,m-trend']

motion = np.arange(50,1000,10)
#%%
# O3A data
start = 'June 11 2019 00:00:00 UTC'
end   = 'June 18 2019 23:00:00 UTC'

filename = '190611_to_190618_data'

before = rangeData(channels,filename,start=start,end=end)
before.cullGlitches()
before.averageRange(motion)
before.normRange()
#%%
# O3B data
start = 'November 1 2019 18:00:00 UTC'
end   = 'November 5 2019 23:59:00 UTC'

filename = '191101_to_191105_data'

after = rangeData(channels,filename,start=start,end=end)
after.cullGlitches()
after.averageRange(motion)
after.normRange()
#%%
from sklearn.linear_model import LinearRegression

y_before = {}
y_after = {}
for i in xrange(len(channels)-4):
    model_before = LinearRegression()
    model_before.fit(np.array(before.data[channels[i+4]].value).reshape(-1,1),np.array(before.data[channels[0]].value).reshape(-1,1))
    
    x_before = motion
    y_before[channels[i+4]] = model_before.predict(x_before[:,np.newaxis])
    
    model_after = LinearRegression()
    model_after.fit(np.array(after.data[channels[i+4]].value).reshape(-1,1),np.array(after.data[channels[0]].value).reshape(-1,1))
    
    x_after = motion
    y_after[channels[i+4]] = model_after.predict(x_after[:,np.newaxis])

#%%
plt.style.use('seaborn')
for i in xrange(len(channels)-4):
    plt.figure(figsize=(16, 9))
    ax = plt.axes()
#    ax.set_prop_cycle('color',plt.cm.Set1(np.linspace(0,1,9)))
    
    ax.scatter(before.data[channels[i+4]],before.data[channels[0]],s=1,label='O3a')
    ax.plot(x_before, y_before[channels[i+4]])
    
    ax.scatter(after.data[channels[i+4]],after.data[channels[0]],s=1,label='O3b')
    ax.plot(x_after, y_after[channels[i+4]])
    
    ax.set_xlim(30,1000)
    ax.set_ylim(95,145)
    ax.set_title('{}'.format(channels[i+4][15:-13]))
    ax.set_xlabel('Ground Velocity (nm/s)')
    ax.set_ylabel('Range (MpC)')
    ax.legend(fontsize='x-large',loc='upper right',scatterpoints=100)
    
#    ax.axis('tight')
    
    
    plt.show()

#%%
#for i in channels[1:]:
#    fig,ax = plt.subplots(1,figsize=[16*1.5,9*1.5])
#    ax.scatter(before.data[i].times.value,before.data[i].norm,label=i[15:-13])
#    ax.scatter(before.data[channels[0]].times.value,before.data[channels[0]].norm,label='Range')
#    ax.legend()
#    ax.set_xscale('auto-gps')
#    ax.set_yscale('log')
##%%
#fig, axes = plt.subplots(3,2,sharex=True,sharey=True,figsize=[16*1.5,9*1.5])
#
#for i in range(3):
#    for j in range(2):
#        index = (i * 3) + j + 2
#        axes[i,j].scatter(motion,before.data[channels[index]].avg_range)
#        axes[i,j].set_title(channels[index][15:-13],fontsize=16)
#axes[0,0].set_ylim([125,140])
#for ax in axes.flat:
#    ax.set(xlabel='Ground Motion (nm/s)',ylabel='Range (Mpc)')    
#    ax.label_outer()
#    


