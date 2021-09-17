#!/home/meichen/anaconda3/bin/python
import numpy as np
import pandas as pd
import os
import obspy
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader
import glob
import shutil
import subprocess
from scipy.optimize import curve_fit
from sys import argv
import csv

def main():
    events_list = pd.read_csv('new_madrid.csv',skipinitialspace=True)
    events = np.array(events_list)
    main_path="/home/meichen/Research/New_Madrid"
    jpath="/home/jritsema/work1/New_Madrid"
    window_length = 2
    
    lat = []
    lon = []
    radius = []
    for i in np.arange(events.shape[0]):
        lat.append(np.float(events[i,1])*(2*np.pi)/180.)
        lon.append(np.float(events[i,2])*(2*np.pi)/180.)
        radius.append(6371-np.float(events[i,3]))
    
    num=0
    pairs = {}
    d = []
    
    for i in np.arange(events.shape[0]):
        if np.float(events[i,4])>=1.5:
            for j in np.arange(events.shape[0]):
                if np.float(events[j,4])>=0:
                    if (np.float(events[i,4])-np.float(events[j,4]))>=0.5:
                        arg=np.cos(lat[i])*np.cos(lat[j])*np.cos(lon[i]-lon[j])+np.sin(lat[i])*np.sin(lat[j])
                        dist=np.sqrt(radius[i]**2+radius[j]**2-2*radius[i]*radius[j]*arg)
                        if dist<=0.5:
                            d.append(events[i,11])
                            d.append(events[j,11])
                            pairs.setdefault(events[i,11],[]).append(events[j,11])
    
    uni_d = np.unique(np.array(d))

###save text file
#    with open("uni_id.txt",'w') as f:
#        for key in uni_d:
#            index = list(events[:,11]).index(key)
#            f.write("%s,%s,%s,%s,%s,%s\n" % (events_list['id'][index], events_list['time'][index], events_list['latitude'][index], events_list['longitude'][index], events_list['depth'][index], events_list['mag'][index]))
#
##save all records
#
#
###make directory; download data; mseedfile to sacfile
#    os.chdir('{}'.format(main_path))
#    for key in events[:,11]:
#        mk_path('event_{}'.format(key))
#        index=list(events[:,11]).index(key)
#        download_data(events[index,:],"event_{}".format(key))
#        mseed2sac('event_{}'.format(key))
#
#    subprocess.call(['mv {}/event_* {}/events/'.format(main_path,main_path)],shell=True)
#    subprocess.call(['bash {}/remove.sh'.format(main_path)],shell=True)

##use dict to save masters and their egfs
#     for i in np.arange(events.shape[0]):
#         if events[i,10]>=6:
#             for j in np.arange(events.shape[0]):
#                 if events[j,10]>=5.5:
#                     if (events[i,10]-events[j,10])>=0.5:
#                         arg=np.cos(lat[i])*np.cos(lat[j])*np.cos(lon[i]-lon[j])+np.sin(lat[i])*np.sin(lat[j])
#                         dist=np.sqrt(radius[i]**2+radius[j]**2-2*radius[i]*radius[j]*arg)
#                         if dist<=50:
#                             pairs.setdefault(events[i,0],[]).append(events[j,0])
#                             num = num +1

##process data now for each egf     
    headers = ['masterID','masterTime','mastermag','masterlat','masterlon','masterdep','egfID','egfTime','egfmag','egflat','egflon','egfdep','s','s_fit_a','s_fit_b','s_fit_c','s_fc_std','s_fc_mean','p','p_fit_a','p_fit_b','p_fit_c','p_fc_std','p_fc_mean']
    with open('{}/pairsfile_nm.csv'.format(main_path),'w+') as f:
        f_csv = csv.DictWriter(f,headers)
        f_csv.writeheader()
    f.close()

    row = []                      
    for key in list(pairs.keys()):
        isExist = os.path.exists('{}/master_{}'.format(main_path,key))
        if isExist:
            shutil.rmtree('{}/master_{}'.format(main_path,key))

        mk_path('{}/master_{}'.format(main_path,key))
        index = list(events[:,11]).index(key)
        masterTime = events[index,0]                               
        mastermag = "{}".format(events[index,4])
        masterlat = events[index,1]
        masterlon = events[index,2]
        masterdep = events[index,3]
        flag = 0
        for value in list(pairs.get(key)):
            isExist = os.path.exists('{}/master_{}/egf_{}'.format(main_path,key,value))
            if isExist:
                shutil.rmtree('{}/master_{}/egf_{}'.format(main_path,key,value))
            index = list(events[:,11]).index(value)
            egfTime = events[index,0]                              
            egfmag = "{}".format(events[index,4]) 
            egflat = events[index,1]
            egflon = events[index,2]
            egfdep = events[index,3]

            each_process(main_path,key,value,'P')
            each_process(main_path,key,value,'S')
            s_fit_a,s_fit_b,s_fit_c,s_c_std,s_c_mean,s_stnnm = fit(main_path=main_path,master=key,egf=value,phase="S",window_length=window_length)
            p_fit_a,p_fit_b,p_fit_c,p_c_std,p_c_mean,p_stnnm = fit(main_path=main_path,master=key,egf=value,phase="P",window_length=window_length)

            if flag == 0:
                row = [{'masterID':key,'masterTime':masterTime,'mastermag':mastermag,'masterlat':masterlat,'masterlon':masterlon,'masterdep':masterdep,'egfID':value,'egfTime':egfTime,'egfmag':egfmag,'egflat':egflat,'egflon':egflon,'egfdep':egfdep,'s':s_stnnm,'s_fit_a':s_fit_a,'s_fit_b':s_fit_b,'s_fit_c':s_fit_c,'s_fc_std':s_c_std,'s_fc_mean':s_c_mean,'p':p_stnnm,'p_fit_a':p_fit_a,'p_fit_b':p_fit_b,'p_fit_c':p_fit_c,'p_fc_std':p_c_std,'p_fc_mean':p_c_mean}]
            else:
                row = [{'egfID':value,'egfTime':egfTime,'egfmag':egfmag,'egflat':egflat,'egflon':egflon,'egfdep':egfdep,'s':s_stnnm,'s_fit_a':s_fit_a,'s_fit_b':s_fit_b,'s_fit_c':s_fit_c,'s_fc_std':s_c_std,'s_fc_mean':s_c_mean,'p':p_stnnm,'p_fit_a':p_fit_a,'p_fit_b':p_fit_b,'p_fit_c':p_fit_c,'p_fc_std':p_c_std,'p_fc_mean':p_c_mean}]
            flag = flag + 1
            with open('{}/pairsfile_nm.csv'.format(main_path),'a') as f:
                f_csv = csv.DictWriter(f,headers)
                f_csv.writerows(row)
            f.close()

        subprocess.call(['sudo cp -r {}/master_{} {}/'.format(main_path,key,jpath)],shell=True)
        subprocess.call(['rm -r {}/master_{}'.format(main_path,key)],shell=True)

def func(x,a,b,c):
    return np.log10(a) + np.log10(1 + x**2 / b**2) - np.log10(1 + x**2 / c**2)

def fit(**kwargs):
    main_path = kwargs.get('main_path')
    master = kwargs.get('master')
    egf = kwargs.get('egf')
    phase = kwargs.get('phase')                              
    window_length = kwargs.get('window_length')              
    filename = glob.glob('{}/master_{}/egf_{}/{}/all*.stn*.Np.sr'.format(main_path,master,egf,phase))
    stn_num = filename[0].split('/')[-1].split(".")[-3]
    if int(stn_num) != 0:                                    
        # read in data and cut needed                        
        data = np.genfromtxt(filename[0])
        data = data[data[:,0]>=float(1./float(window_length))]
        data = data[data[:,0]<=20.]
        xdata = data[:,0]                                    
        ydata = data[:,1]                                    
        ydata = np.log10(ydata)                              
                                                             
        # find best fit model                                
        popt, pcov = curve_fit(func, xdata, ydata, bounds=([0.1,0.5,0.5],[1000,100.,20.]),method='trf',loss='huber',f_scale=0.1)
                                                             
        ## uncertainty analysis by bootstrapping            
        # calculate residuals                                
        res = func(xdata,*popt)-ydata
        popt_list = []                                       
        # length of xdata                                    
        l = len(xdata)                                       
        # bootstrap                                          
        for i in np.arange(1000):                            
            random_index = np.random.randint(0,l,size=l)     
            new_ydata = ydata + [res[j] for j in random_index]
            try:
                new_popt, new_pcov = curve_fit(func, xdata,new_ydata, bounds=([0.1,0.5,0.5],[1000,100.,20.]),method='trf',loss='huber',f_scale=0.1)
                popt_list.append(new_popt)
            except RuntimeError:
                print("Error - curve_fit failed")
        std = np.std(np.array(popt_list)[:,2],ddof=1)
        mean = np.mean(np.array(popt_list)[:,2])
                                                             
        return popt[0],popt[1],popt[2],std,mean,stn_num
    else:                                                    
        return 0,0,0,0,0,0



def all_85(main_path,key,value,phase):
    mk_path('{}/master_{}/egf_{}/{}/gcarc_85'.format(main_path,key,value,phase))
    os.chdir('{}/master_{}/egf_{}/{}/gcarc_85'.format(main_path,key,value,phase))
    window_begin=-0.2
    window_length=2
    window_multi=5
    subprocess.call(['cp {}/master_{}/egf_{}/{}/gcarc_30/*.Np*.master {}/master_{}/egf_{}/{}/gcarc_85/'.format(main_path,key,value,phase,main_path,key,value,phase)],shell=True)
    subprocess.call(['cp {}/master_{}/egf_{}/{}/gcarc_30_85/*.Np*.master {}/master_{}/egf_{}/{}/gcarc_85/'.format(main_path,key,value,phase,main_path,key,value,phase)],shell=True)
    subprocess.call(['cp {}/master_{}/egf_{}/{}/gcarc_30/*.Np*.egf {}/master_{}/egf_{}/{}/gcarc_85/'.format(main_path,key,value,phase,main_path,key,value,phase)],shell=True)
    subprocess.call(['cp {}/master_{}/egf_{}/{}/gcarc_30_85/*.Np*.egf {}/master_{}/egf_{}/{}/gcarc_85/'.format(main_path,key,value,phase,main_path,key,value,phase)],shell=True)
    subprocess.call(['bash','/home/meichen/bin/sr_calc.sh','{}'.format(window_begin),'{}'.format(window_length),'{}'.format(window_multi),'{}'.format(phase),'85'])
    

def each_process(main_path,key,value,phase):
    mk_path('{}/master_{}/egf_{}/{}'.format(main_path,key,value,phase))
    os.chdir('{}/master_{}/egf_{}/{}'.format(main_path,key,value,phase))
    window_begin=-0.2
    window_length=2
    window_multi=5
    if phase == 'P':
        subprocess.call(['bash','/home/meichen/bin/stn_sel.sh','{}/events/event_{}/waveforms/HZ/filtered'.format(main_path,key),'{}/events/event_{}/waveforms/HZ/filtered'.format(main_path,value),'{}/master_{}/egf_{}/P'.format(main_path,key,value)])
        subprocess.call(['python','/home/meichen/bin/seismoscript.py',"*.master","t1",'{}'.format(window_begin),'{}'.format(window_length),'{}'.format(window_multi),'master'])
        subprocess.call(['python','/home/meichen/bin/seismoscript.py',"*.egf","t1",'{}'.format(window_begin),'{}'.format(window_length),'{}'.format(window_multi),'egf'])
    elif phase == 'S':
        subprocess.call(['bash','/home/meichen/bin/stn_sel.sh','{}/events/event_{}/waveforms/HN/filtered'.format(main_path,key),'{}/events/event_{}/waveforms/HN/filtered'.format(main_path,value),'{}/master_{}/egf_{}/S'.format(main_path,key,value)])
        subprocess.call(['bash','/home/meichen/bin/stn_sel.sh','{}/events/event_{}/waveforms/HE/filtered'.format(main_path,key),'{}/events/event_{}/waveforms/HE/filtered'.format(main_path,value),'{}/master_{}/egf_{}/S'.format(main_path,key,value)])
        subprocess.call(['bash','/home/meichen/bin/add_BHNE.sh','{}/master_{}/egf_{}/S'.format(main_path,key,value)])
        subprocess.call(['python','/home/meichen/bin/seismoscript.py',"*.master","t2",'{}'.format(window_begin),'{}'.format(window_length),'{}'.format(window_multi),'master'])
        subprocess.call(['python','/home/meichen/bin/seismoscript.py',"*.egf","t2",'{}'.format(window_begin),'{}'.format(window_length),'{}'.format(window_multi),'egf'])
    subprocess.call(['bash','/home/meichen/bin/sr_calc_nm.sh','{}'.format(str(window_begin).replace('.','0')),'{}'.format(str(window_length).replace('.','0')),'{}'.format(window_multi),'{}'.format(phase)])
        
    os.chdir('{}/events'.format(main_path))
    

def mk_path(path):
    import os
    isExist=os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def download_data(event_info,save_path):
    import obspy
    from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader, RectangularDomain

    lat=event_info[1]
    lon=event_info[2]
    origin_time=obspy.UTCDateTime(event_info[0])

#    domain=RectangularDomain(minlatitude=35,maxlatitude=37,minlongitude=-91,maxlongitude=-88.5)
    domain=CircularDomain(latitude=lat,longitude=lon,minradius=0.0,maxradius=0.5)
    restrictions=Restrictions(starttime=origin_time - 30,endtime=origin_time + 90,network="NM",reject_channels_with_gaps=False,minimum_length=0.95,minimum_interstation_distance_in_m=10,channel_priorities=["[BEH]H[ZNE]"],location_priorities=["","00","10"])

    mdl=MassDownloader(providers=["IRIS"])
    mdl.download(domain,restrictions,mseed_storage="{}/waveforms".format(save_path),stationxml_storage="{}/stations".format(save_path))

def mseed2sac(path):
    import subprocess
    for stnxml in glob.glob('{}/stations/*'.format(path)):
        stationname=stnxml.split('/')[-1]
        nw=stationname.split('.')[0]
        stn=stationname.split('.')[1]
        subprocess.call(['java','-jar','/home/meichen/bin/stationxml-seed-converter-2.0.0.jar','--input','{}/stations/{}.{}.xml'.format(path,nw,stn),'--output','{}/waveforms/{}.{}.dataless'.format(path,nw,stn)])
        for filename in glob.glob('{}/waveforms/{}.{}.*.mseed'.format(path,nw,stn)):
            mseedfile=filename.split('/')[-1]
            print('rdseed','-df','{}/waveforms/{}'.format(path,mseedfile),'-z','1','-g','{}/waveforms/{}.{}.dataless'.format(path,nw,stn),'-q','{}/waveforms/'.format(path))
            subprocess.call(['rdseed','-df','{}/waveforms/{}'.format(path,mseedfile),'-z','1','-g','{}/waveforms/{}.{}.dataless'.format(path,nw,stn),'-q','{}/waveforms/'.format(path)])

main()
