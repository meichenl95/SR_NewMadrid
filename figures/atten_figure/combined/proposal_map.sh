#!/bin/bash

main_path=/home/meichen/Research/New_Madrid/figures/atten_figure/combined

J=x2id
R=-90.3/-89.2/35.7/37
PS=prop_map.ps

gmt gmtset MAP_FRAME_TYPE plain
gmt pscoast -J$J -R$R -BWSen -Bxa0.5f0.5 -Bya0.5f0.5 -Df -W1/0 -W2/0 -A1 -N2 -P -K > $PS

#---- Global constants-----                                      
gmtset MAP_FRAME_TYPE fancy 
gmtset MAP_FRAME_WIDTH 0.055 
gmtset MAP_DEGREE_SYMBOL degree 
gmtset MAP_TICK_LENGTH 0.1
gmtset FONT_LABEL 6p 

# input topography file 
GRD=GMRTv3_6_20190402topo.grd 
gmt grdgradient $GRD -Nt -A0 -Ggrid_grad.nc
gmt makecpt -Cglobe -A50 > Itopo.cpt 
gmt grdimage -R$R -J$J $GRD -CItopo.cpt -Igrid_grad.nc -P -O -K >> $PS 



eventid_S=`gawk '{print $2}' $main_path/eventid_S.txt`
eventid_PS=`gawk '{print $2}' $main_path/eventid_PS.txt`
eventid_P=`gawk '{print $2}' $main_path/eventid_P.txt`

#plot egfs locations

for id in $eventid_S
do
    evlo=`gawk '$2=="'"$id"'"{print $3}' $main_path/eventid_S.txt`
    evla=`gawk '$2=="'"$id"'"{print $4}' $main_path/eventid_S.txt`
    color=lightgrey
    gawk '{print ""'"$evlo"'" "'"$evla"'"\n",$1,$2}' ${id}_HNE_stn.txt | gmt psxy -R -J -Wfaint,$color,.. -K -O -P -N >> $PS
done

for id in $eventid_P
do
    evlo=`gawk '$2=="'"$id"'"{print $3}' $main_path/eventid_P.txt`
    evla=`gawk '$2=="'"$id"'"{print $4}' $main_path/eventid_P.txt`
    color=lightgrey
    gawk '{print ""'"$evlo"'" "'"$evla"'"\n",$1,$2}' ${id}_HZ_stn.txt | gmt psxy -R -J -Wfaint,$color,.. -K -O -P -N >> $PS
done

for id in $eventid_PS
do
    evlo=`gawk '$2=="'"$id"'"{print $3}' $main_path/eventid_PS.txt`
    evla=`gawk '$2=="'"$id"'"{print $4}' $main_path/eventid_PS.txt`
    color=lightgrey
    gawk '{print ""'"$evlo"'" "'"$evla"'"\n",$1,$2}' ${id}_HZ_stn.txt | gmt psxy -R -J -Wfaint,$color,.. -K -O -P -N >> $PS
    gawk '{print ""'"$evlo"'" "'"$evla"'"\n",$1,$2}' ${id}_HNE_stn.txt | gmt psxy -R -J -Wfaint,$color,.. -K -O -P -N >> $PS
done
cat *.txt | gmt psxy -R -J -St0.2c -W0.1p,gold -Ggold -O -K -P >> $PS

for id in $eventid_S
do
    evlo=`gawk '$2=="'"$id"'"{print $3}' $main_path/eventid_S.txt`
    evla=`gawk '$2=="'"$id"'"{print $4}' $main_path/eventid_S.txt`
    color=blue
    echo $evlo $evla | gmt psxy -R -J -Sc0.2c -W0.4p,$color -K -O -P >> $PS
done

for id in $eventid_P
do 
    evlo=`gawk '$2=="'"$id"'"{print $3}' $main_path/eventid_P.txt`
    evla=`gawk '$2=="'"$id"'"{print $4}' $main_path/eventid_P.txt`
    color=blue
    echo $evlo $evla | gmt psxy -R -J -Sc0.2c -W0.4p,$color -K -O -P >> $PS
done

for id in $eventid_PS
do 
    evlo=`gawk '$2=="'"$id"'"{print $3}' $main_path/eventid_PS.txt`
    evla=`gawk '$2=="'"$id"'"{print $4}' $main_path/eventid_PS.txt`
    color=blue
    echo $evlo $evla | gmt psxy -R -J -Sc0.2c -W0.4p,$color -K -O -P >> $PS
done

cat *.txt | gmt psxy -R -J -St0.2c -W0.1p,gold@100 -Ggold@100 -O -P >> $PS
gmt psconvert -Tf $PS
