#!/home/meichen/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('pairsfile_nm.csv',skipinitialspace=True)
data_array = np.array(data)
num_stations = 3
std_to_mean = 0.1
upper_fc = 19.9
lower_fc = 0.51

# plot magnitude difference vs. moment mag
fig,ax = plt.subplots(1,2,figsize=[12,6])
for m,phase in zip(np.arange(2),['S','P']):
    data_array_filter = data_array[data_array[:,13+m*6]>=num_stations]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]<upper_fc]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]>lower_fc]
    data_array_filter = data_array_filter[data_array_filter[:,17+m*6]/data_array_filter[:,18+m*6]<std_to_mean]
    mag=[]
    magdif=[]
    fit_magdif=[]
    egf_lat=[]
    egf_lon=[]
    for i in np.arange(len(data_array_filter[:,12])):
        magdif.append(data_array_filter[i,12])
        fit_magdif.append(data_array_filter[i,14])
        mag.append(data_array_filter[i,2])
        egf_lat.append(float(data_array_filter[i,9]))
        egf_lon.append(float(data_array_filter[i,10]))
        print(phase, data_array_filter[i,9],data_array_filter[i,10])
    fit_magdif = 2./3.*np.log10(fit_magdif)
    ax[m].scatter(magdif,fit_magdif,s=10)
    ax[m].set_xlim([0,2.5])
    ax[m].set_ylim([0,2.5])
    ax[m].set_xlabel('magdif from NEIC')
    ax[m].set_ylabel('fitting magdif')
    ax[m].set_title('phase={}, num of points={}'.format(phase,len(magdif)))

plt.suptitle('magnitude difference of fitting and NEIC')
plt.savefig('mag_difference.png')

# plot distribution of station recording number
fig,ax = plt.subplots(1,2,figsize=[12,6])
for m,phase in zip(np.arange(2),['S','P']):
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]<upper_fc]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]>lower_fc]
    data_array_filter = data_array_filter[data_array_filter[:,17+m*6]/data_array_filter[:,18+m*6]<std_to_mean]
    stnnm = data_array_filter[:,13+m*5]
    tmp = []
    for i in np.arange(len(stnnm)):
        tmp.append(stnnm[i])
    median = np.median(tmp)
    ax[m].hist(tmp,10)
    ax[m].set_xlabel('station number')
    ax[m].set_title('phase={}, num of points={}'.format(phase,len(tmp)))

plt.suptitle('Variation of station number')
plt.savefig('stnnm_hist.png')


# plot stress drop and corner frequency vs. depth
fig,ax = plt.subplots(1,2,figsize=[12,6])
for m,phase in zip(np.arange(2),['S','P']):
    data_array_filter = data_array[data_array[:,13+m*6]>=num_stations]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]<upper_fc]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]>lower_fc]
    data_array_filter = data_array_filter[data_array_filter[:,17+m*6]/data_array_filter[:,18+m*6]<std_to_mean]

    mean_pairs = {}
    std_pairs = {}
    depth = []
    depth.append(data_array_filter[0,5])

    for i in np.arange(len(data_array_filter[:,0])):
        mean_pairs.setdefault(data_array_filter[i,0],[]).append(data_array_filter[i,18+m*6])
        std_pairs.setdefault(data_array_filter[i,0],[]).append(data_array_filter[i,17+m*6])
        if i>0 and data_array_filter[i,0] != data_array_filter[i-1,0]:
            depth.append(data_array_filter[i,5])
   
    fc = np.ones(len(mean_pairs))
    fc_std = np.zeros(len(mean_pairs))
    
    for counter,key in enumerate(list(mean_pairs.keys())):
        mean = mean_pairs.get(key)
        std = std_pairs.get(key)
    
        for i in np.arange(len(mean)):
            fc[counter] = fc[counter]*mean[i]
            fc_std[counter] = fc_std[counter] + (std[i]/mean[i])**2
        fc[counter] = fc[counter]**(1/len(mean))
        fc_std[counter] = 1/len(mean)*fc[counter]*fc_std[counter]**0.5
    ax[m].errorbar(depth,fc,yerr=fc_std,linestyle='',marker='o',mfc='red',mec='blue',markersize=3)
#    ax[m].set_yscale('log')
    ax[m].set_xlabel('Depth(km)')
    ax[m].set_ylabel('Corner frequency(Hz)')
    ax[m].set_title('phase={}, num of points={}'.format(phase,len(depth)))

fig.suptitle('Corner frequency variation with depth')
fig.savefig('fc_depth.png')


## plot corner frequency vs. moment magnitude
#fig,ax = plt.subplots(1,2,figsize=[12,6])
#for m,phase in zip(np.arange(2),['S','P']):
#    data_array_filter = data_array[data_array[:,13+m*5]>2]
#    data_array_filter = data_array_filter[data_array_filter[:,17+m*5]<19.9]
#    data_array_filter = data_array_filter[data_array_filter[:,17+m*5]>0.51]
#    data_array_filter = data_array_filter[data_array_filter[:,16+m*5]/data_array_filter[:,17+m*5]<0.1]
#    fc = data_array_filter[:,17+m*5]
#    M0_gcmt = data_array_filter[:,9]
#    mag = []
#    for i in np.arange(len(fc)):
#        mag.append(2./3.*(np.log10(np.float(M0_gcmt[i]))-9.1))
#    ax2 = ax[m,j].twiny()
#    sd_low = 0.001*1000000
#    sd_up = 30*1000000
#    if phase == 'S':
#        wave_v = 5300
#        C = 1.99
#    elif phase == 'P':
#        wave_v = 9200
#        C = 1.6
#    ax[m,j].plot([10**16,10**22],[pow((2*sd_low*C**3*wave_v**3)/(7*10**16),1/3),pow((2*sd_low*C**3*wave_v**3)/(7*10**22),1/3)],linestyle='--',color='orange',label='{}Mpa'.format(sd_low*1e-6))
#    ax[m,j].plot([10**16,10**22],[pow((2*sd_up*C**3*wave_v**3)/(7*10**16),1/3),pow((2*sd_up*C**3*wave_v**3)/(7*10**22),1/3)],linestyle='--',color='red',label='{}Mpa'.format(sd_up*1e-6))
#    ax2.scatter(mag,fc,s=5,label='{}'.format(len(mag)))
#    
#    ax[m,j].set_yscale("log")
#    ax[m,j].set_xscale("log")
#    ax[m,j].legend()
#    ax[m,j].set_title('{} {} {}'.format(distance,phase,len(fc)))
#
#plt.suptitle('moment magnitude(x axis) vs.\ncorner frequency(Hz)')
#plt.savefig('fc.png')
        

# plot corner frequency of S vs. P
fig,ax = plt.subplots(1,1,figsize=[6,6])
data_array_filter_s = data_array[data_array[:,13]>=num_stations]
data_array_filter_p = data_array[data_array[:,19]>=num_stations]
data_array_filter_s = data_array_filter_s[data_array_filter_s[:,18]<upper_fc]
data_array_filter_s = data_array_filter_s[data_array_filter_s[:,18]>lower_fc]
data_array_filter_p = data_array_filter_p[data_array_filter_p[:,24]<upper_fc]
data_array_filter_p = data_array_filter_p[data_array_filter_p[:,24]>lower_fc]
data_array_filter_s = data_array_filter_s[data_array_filter_s[:,17]/data_array_filter_s[:,18]<std_to_mean]
data_array_filter_p = data_array_filter_p[data_array_filter_p[:,23]/data_array_filter_p[:,24]<std_to_mean]

s_mean_pairs = {}
s_std_pairs = {}
p_mean_pairs = {}
p_std_pairs = {}

for i in np.arange(len(data_array_filter_p[:,0])):
    if data_array_filter_p[i,0] in list(data_array_filter_s[:,0]):
        p_mean_pairs.setdefault(data_array_filter_p[i,0],[]).append(data_array_filter_p[i,24])
        p_std_pairs.setdefault(data_array_filter_p[i,0],[]).append(data_array_filter_p[i,23])
        

for i in np.arange(len(data_array_filter_s[:,0])):
    if data_array_filter_s[i,0] in list(data_array_filter_p[:,0]):
        s_mean_pairs.setdefault(data_array_filter_s[i,0],[]).append(data_array_filter_s[i,18])
        s_std_pairs.setdefault(data_array_filter_s[i,0],[]).append(data_array_filter_s[i,17])

s_fc = np.ones(len(s_mean_pairs))
s_fc_std = np.zeros(len(s_mean_pairs))
p_fc = np.ones(len(p_mean_pairs))
p_fc_std = np.zeros(len(p_mean_pairs))

for counter,key in enumerate(list(s_mean_pairs.keys())):
    #print(key)
    s_mean = s_mean_pairs.get(key)
    s_std = s_std_pairs.get(key)
    p_mean = p_mean_pairs.get(key)
    p_std = p_std_pairs.get(key)
    for i in np.arange(len(s_mean)):
        s_fc[counter] = s_fc[counter]*s_mean[i]
        s_fc_std[counter] = s_fc_std[counter] + (s_std[i]/s_mean[i])**2
    for i in np.arange(len(p_mean)):
        p_fc[counter] = p_fc[counter]*p_mean[i]
        p_fc_std[counter] = p_fc_std[counter] + (p_std[i]/p_mean[i])**2
    s_fc[counter] = s_fc[counter]**(1/len(s_mean))
    s_fc_std[counter] = 1/len(s_mean)*s_fc[counter]*s_fc_std[counter]**0.5
    p_fc[counter] = p_fc[counter]**(1/len(p_mean))
    p_fc_std[counter] = 1/len(p_mean)*p_fc[counter]*p_fc_std[counter]**0.5

ax.errorbar(s_fc,p_fc,yerr=p_fc_std,xerr=s_fc_std,linestyle='',marker='o',mfc='red',mec='blue',markersize=3)
ax.plot([0,20],[0,20],color='orange')
ax.set_xlim([0,20])
ax.set_ylim([0,20])
ax.set_xlabel('fcs(Hz)')
ax.set_ylabel('fcp(Hz)')
ax.set_title('corner frequency of S and P, num={}'.format(len(s_fc)))
plt.savefig('fcs_fcp.png')


# plot std_to_mean vs. moment magnitude
fig,ax = plt.subplots(1,2,figsize=[12,6])
for m,phase in zip(np.arange(2),['S','P']):
    data_array_filter = data_array[data_array[:,13+m*6]>=num_stations]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]<upper_fc]
    data_array_filter = data_array_filter[data_array_filter[:,18+m*6]>lower_fc]
    std_to_mean_temp = data_array_filter[:,17+m*6]/data_array_filter[:,18+m*6]
    mastermag = data_array_filter[:,2]
    ax[m].scatter(mastermag,std_to_mean_temp,s=10)
    ax[m].set_xlabel('magnitude')
    ax[m].set_ylabel('std to mean')
    ax[m].set_title('phase={},num={}'.format(phase,len(mastermag)))

fig.suptitle('std-to-mean variance with magnitude')
fig.savefig('std_to_mean.png')

