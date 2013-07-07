#!/bin/sh

hcitool dev
hcitool scan
echo Code Pin 6666
bluez-simple-agent hci0 00:18:A1:12:16:C5
python ./batcar_v1.py
