#!/home/meichen/anaconda3/bin/python
import numpy as np
import pandas as pd

main_path  = "/home/meichen/Research/New_Madrid/figures/atten_figure/combined"

eventid = pd.read_csv('{}/eventid_S.txt'.format(main_path),skipinitialspace=True,header=None,sep=' ',names=['phase','id','lon','lat'])
eventid = eventid['id']
for sid in eventid:
    hn = np.genfromtxt('{}/{}_HN_stn.txt'.format(main_path,sid))
    he = np.genfromtxt('{}/{}_HE_stn.txt'.format(main_path,sid))
    hs = np.vstack((hn,he))
    df = pd.DataFrame(hs)
    hs = hs[df.duplicated()]
    np.savetxt('{}/{}_HNE_stn.txt'.format(main_path,sid),hs)

