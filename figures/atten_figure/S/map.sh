#!/bin/bash

J=x2id
R=-91/-88.5/35/37.5
PS=map.ps

gmt gmtset MAP_FRAME_TYPE plain
gmt pscoast -J$J -R$R -BWSen -Bxa0.5f0.5 -Bya0.5f0.5 -Df -W1/0 -W2/0 -A1 -N2 -P -K > $PS

gawk '{print $3,$4}' eventid.txt | gmt psxy -R -J -Sa0.2c -W0.2p,red -Gred -K -O -P >> $PS
