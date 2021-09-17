#!/bin/bash

main_path=/home/meichen/Research/New_Madrid/events

# for filename in $(ls -d */);
# do
#     cd $main_path/$filename/
#     if [[ -d stations ]]
#     then
#         rm -r stations
#     fi
#     cd $main_path/$filename/waveforms/
#     rm *.mseed
#     rm *.dataless
#     cd $main_path/
# done

for event in $(gawk '{print $1}' uni_id.txt)
do
    echo $event
    eventid=` echo $event | gawk -F, '{print $1}'`
    evla=` echo $event | gawk -F, '{print $3}'`
    evlo=` echo $event | gawk -F, '{print $4}'`
    evdp=` echo $event | gawk -F, '{print $5}'`
    cd $main_path/event_$eventid/waveforms/
sac<<EOF
r *.SAC
ch evla $evla
ch evlo $evlo
ch evdp $evdp
wh
q
EOF

bash mark_sac.sh

    if [[ -d HE ]]
    then
        rm -r HE HN HZ
    fi
    mkdir HE HN HZ
    echo "cp *.?HE.*.SAC HE/" | sh  
    echo "cp *.?HN.*.SAC HN/" | sh
    echo "cp *.?HZ.*.SAC HZ/" | sh
done 
