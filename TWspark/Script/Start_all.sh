#!/bin/sh
#Starta tutti
echo -e "\n Starting clean_dataset.py \n ------------------\n\n"
python3 clean_dataset.py
echo -e "\n Starting MLtest.py \n ------------------\n\n"
python3 MLtest.py
echo -e "\n Starting  StreamRx and TWclient \n ------------------\n\n"

python3 StreamRx.py |xterm -hold -e python3 $PWD/TWclient.py

#terminator -x python3 StreamRx.py |terminator --new-tab -x python3 TWclient.py


# dashboard.py   __pycache__  Start.sh  StreamRx.py  TWclient.py