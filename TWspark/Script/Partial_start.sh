#!/bin/sh
#Starta solo la parte di ricerca.
python3 StreamRx.py |xterm -hold -e python3 $PWD/TWclient.py