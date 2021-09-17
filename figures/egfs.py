#!/home/meichen/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def main():
    data = pd.read_csv('pairsfile_nm.csv',skipinitialspace=True)
    data_array = np.array(data)
    jpath = '/home/jritsema/work1/New_Madrid'
    num_stations = 3
    std_to_mean = 0.1
    upper_fc = 19.9
    lower_fc = 0.51
    
    for m,phase in zip(np.arange(2),['S','P']):
        data_array_filter = data_array[data_array[:,13+m*6]>num_stations]
        data_array_filter = data_array_filter[data_array_filter[:,18+m*6]<upper_fc]
        data_array_filter = data_array_filter[data_array_filter[:,18+m*6]>lower_fc]
        data_array_filter = data_array_filter[data_array_filter[:,17+m*6]/data_array_filter[:,18+m*6]<std_to_mean]
        pairs = {}
        for i in np.arange(len(data_array_filter[:,0])):
            pairs.setdefault(data_array_filter[i,0],[]).append(data_array_filter[i,6])
        for key in list(pairs.keys()):
            os.chdir('{}/master_{}'.format(jpath,key))
            num = 0
            fig = plt.figure(figsize=[5,8])
            ax1 = fig.add_subplot(111)
            for value in list(pairs.get(key)):
                stn_num = glob.glob('egf_{}/{}/all*'.format(value,phase))[0].split('.')[-3]
                if int(stn_num) > 0 :
                    d = np.genfromtxt('{}'.format(glob.glob('egf_{}/{}/all*'.format(value,phase))[0]))
                    d = d[d[:,0]<upper_fc]
                    print(num)
                    indices = [l for l,x in enumerate(data_array_filter[:,0]) if x == key]
                    index = list(data_array_filter[l,6] for l in indices).index(value)
                    fc = data_array_filter[indices[0]+index,18+m*6]
                    a = float(data_array_filter[indices[0]+index,14+m*6])
                    b = float(data_array_filter[indices[0]+index,15+m*6])
                    if fc < b :
                        ax1.loglog(d[:,0],d[:,1],'C{}'.format(num),label='{} stn:{}'.format(value,stn_num))
                        ax1.loglog(d[:,0],func(d[:,0],a,b,fc),linestyle='--',color='grey')
                        ax1.scatter(fc,func(fc,a,b,fc),marker='v',color='C{}'.format(num),s=60)
                num = num + 1
                num = num % 9
            ax1.legend()
            ax1.set_xlabel('Frequency(Hz)')
            ax1.set_ylabel('Amplitude')
            ax1.set_title('master_{}_{}'.format(key,phase))
            plt.savefig('/home/meichen/Research/New_Madrid/figures/master_{}_{}.png'.format(key,phase))
            plt.close()


def func(x,a,b,c):
    return a * (1 + x**2 / b**2)/(1 + x**2 / c**2)

main()
