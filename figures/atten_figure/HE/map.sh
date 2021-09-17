#!/bin/bash

J=x2id
R=-90.2/-89.2/35.8/37
PS=map.ps

gmt gmtset MAP_FRAME_TYPE plain
gmt pscoast -J$J -R$R -BWSen -Bxa0.5f0.5 -Bya0.5f0.5 -Df -W1/0 -W2/0 -A1 -N2 -P -K > $PS

# nm60195431
# nm60096472
# nm60096427
# nm60080557
gawk '{print "'-89.672' '36.5448'\n",$1,$2}' nm_60211757_HE_stn.txt | gmt psxy -R -J -Wfaint,lightred,..- -K -O -N -P >> $PS
gawk '{print "'-89.6037' '36.5358'\n",$1,$2}' nm_60096472_HE_stn.txt | gmt psxy -R -J -Wfaint,lightred,..- -K -O -N -P >> $PS
gawk '{print "'-89.6055' '36.536'\n",$1,$2}' nm_60096427_HE_stn.txt | gmt psxy -R -J -Wfaint,lightred,..- -K -O -N -P >> $PS
gawk '{print "'-89.61' '36.57'\n",$1,$2}' nm_60080557_HE_stn.txt | gmt psxy -R -J -Wfaint,lightred,..- -K -O -N -P >> $PS
gmt psxy -R -J -Sa0.2c -W0.2p,red -Gred -K -O -P >> $PS<<EOF
-89.672 36.5448
-89.6037 36.5358
-89.6055 36.536
-89.61 36.57
EOF

# nm60245416
# nm60240596
# nm60123007
gawk '{print "'-89.5367' '36.445'\n",$1,$2}' nm_60245416_HE_stn.txt | gmt psxy -R -J -Wfaint,lightblue,..- -K -O -N -P >> $PS
gawk '{print "'-89.55' '36.45'\n",$1,$2}' nm_60240596_HE_stn.txt | gmt psxy -R -J -Wfaint,lightblue,..- -K -O -N -P >> $PS
gawk '{print "'-89.56' '36.47'\n",$1,$2}' nm_60211757_HE_stn.txt | gmt psxy -R -J -Wfaint,lightblue,..- -K -O -N -P >> $PS
gmt psxy -R -J -Sa0.2c -W0.2p,blue -Gblue -K -O -P >> $PS<<EOF
-89.5367 36.445
-89.55 36.45
-89.56 36.47
EOF

# nm60216632
# nm60241501
# nm60213567
# nm60211757
# nm60146331
# nm60099616
gawk '{print "'-89.4482' '36.269'\n",$1,$2}' nm_60216632_HE_stn.txt | gmt psxy -R -J -Wfaint,lightgreen,..- -K -O -N -P >> $PS
gawk '{print "'-89.4475' '36.2688'\n",$1,$2}' nm_60241501_HE_stn.txt | gmt psxy -R -J -Wfaint,lightgreen,..- -K -O -N -P >> $PS
gawk '{print "'-89.4485' '36.2692'\n",$1,$2}' nm_60213567_HE_stn.txt | gmt psxy -R -J -Wfaint,lightgreen,..- -K -O -N -P >> $PS
gawk '{print "'-89.445' '36.2722'\n",$1,$2}' nm_60211757_HE_stn.txt | gmt psxy -R -J -Wfaint,lightgreen,..- -K -O -N -P >> $PS
gawk '{print "'-89.4688' '36.2868'\n",$1,$2}' nm_60146331_HE_stn.txt | gmt psxy -R -J -Wfaint,lightgreen,..- -K -O -N -P >> $PS
gawk '{print "'-89.4132' '36.218'\n",$1,$2}' nm_60099616_HE_stn.txt | gmt psxy -R -J -Wfaint,lightgreen,..- -K -O -N -P >> $PS
gmt psxy -R -J -Sa0.2c -W0.2p,darkgreen -Gdarkgreen -K -O -P >> $PS<<EOF
-89.4482 36.269
-89.4475 36.2688
-89.4485 36.2692
-89.445 36.2722
-89.4688 36.2868
-89.4132 36.218
EOF
cat *.txt | gmt psxy -R -J -St0.1c -W0.1p,gold -Ggold -K -O -P >> $PS
gmt psxy -R -J -Sa0.2c -W0.2p,red -Gred -K -O -P >> $PS<<EOF
-89.672 36.5448
-89.6037 36.5358
-89.6055 36.536
-89.61 36.57
EOF
gmt psxy -R -J -Sa0.2c -W0.2p,blue -Gblue -K -O -P >> $PS<<EOF
-89.5367 36.445
-89.55 36.45
-89.56 36.47
EOF
gmt psxy -R -J -Sa0.2c -W0.2p,darkgreen -Gdarkgreen -K -O -P >> $PS<<EOF
-89.4482 36.269
-89.4475 36.2688
-89.4485 36.2692
-89.445 36.2722
-89.4688 36.2868
-89.4132 36.218
EOF
