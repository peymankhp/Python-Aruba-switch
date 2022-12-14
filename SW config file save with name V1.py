from netmiko import Netmiko
import sys
import os
import glob
import re
import time
import os
import shutil
import subprocess
import io
import linecache
from icmplib import ping, multiping, traceroute, resolve
from icmplib import async_ping, async_multiping, async_resolve
from icmplib import ICMPv4Socket, ICMPv6Socket, AsyncSocket, ICMPRequest, ICMPReply
import re

#remove all .txt file in config folder
onfigfolder="C:\\OS\Python Auba\Config files"
for zippath in glob.iglob(os.path.join(onfigfolder, '*.txt')):
    os.remove(zippath)

orig_stdout = sys.stdout
sys.stdout = open("switchfile", "w")

# redirect stdout to file for Netmiko to use later
print ("sh run | includ hostname")
print("""
sh mac-add vlan 100
""")

#time.sleep(2)

# close the file, stop redirecting stdout
sys.stdout.close()
sys.stdout = orig_stdout
# opening the file in read mode
Hostlist = open("C:\\OS\Python Auba\SW list.txt", "r")
# reading the file
thislist = Hostlist.read()
# replacing end splitting the text
# when newline ('\n') is seen.
data_into_list = thislist.split("\n")

#Erase SW down list file for new SW down list
a = open("C:\\OS\Python Auba\SW down list.txt", "a")

a.truncate(0)

#For ping and connect to server
for hostname in data_into_list:
    #Ping host
    #hostname = "10.10.100.3"
    response = ping (hostname , count=1)

    #Connect to host with user and password
    if response.is_alive:
        switch = {
            'host': hostname,
            'username': 'admin',
            'password': '1ns2deout',
            'device_type': 'hp_procurve',
        }
        switchconnect = Netmiko(**switch)
        switchconnect.enable()

        # run Netmiko, print what happens on switch, disconnect
        output = switchconnect.send_config_from_file("switchfile")

        #open file and write configuration
        f = open("C:\\OS\Python Auba\SW.txt", "w")
        f.write(output)
        #print(output)
        switchconnect.disconnect()

        #convert content of config file tostring for regex
        s = str(output)

        #find host name of file
        start = '"'
        end = '"'
        SWFilename= (s[s.find(start) + len(start):s.rfind(end)])
        # Create textfile with extention
        SWFilename= str(SWFilename + '.txt')
        filepath = os.path.join('C:\OS\Python Auba\Config files', SWFilename)
        if not os.path.exists('C:\OS\Python Auba\Config files'):
            os.makedirs('C:\OS\Python Auba\Config files')
        f = open(filepath, "a")
        #write config to hostname file
        f.write(output)


    else:
      a = open("C:\\OS\Python Auba\SW down list.txt", "a")
      #Add down SW to list
      a.write(hostname)
      #new line
      a.write('\n')
      print (hostname, 'is down!')


