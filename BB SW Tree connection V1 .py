from netmiko import Netmiko
import sys
import os
import glob
import re
import time
import os
import subprocess
import shutil
import subprocess
import iptools
import io
import linecache
from icmplib import ping, multiping, traceroute, resolve
from icmplib import async_ping, async_multiping, async_resolve
from icmplib import ICMPv4Socket, ICMPv6Socket, AsyncSocket, ICMPRequest, ICMPReply
import re

##########################################################################################
#Remove file SW down list.txt in C:\GitHub\Find IP and connect\SW config
def Remove_files (FilePath,folderPath):
    if os.path.exists(FilePath):
        os.remove(FilePath)
    configfolder = folderPath
    for dir in os.listdir(configfolder):
        shutil.rmtree(os.path.join(configfolder, dir))

FilePath_Downlist= "C:\GitHub\Find IP and connect\SW config\SW down list.txt"
folderPath_Config="C:\GitHub\Find IP and connect\SW config"

Remove_files(FilePath_Downlist,folderPath_Config)

##########################################################################################
#Ask IP and check it is valid or not
def is_valid_IPAddress(ip,IPTextFile):
    c_ip = iptools.ipv4.validate_ip(ip)
    if c_ip is True:
        IPVAlidation = open(IPTextFile, "a")
        IPVAlidation.truncate(0)
        IPVAlidation.write(ip)
    else :
        print("Invalid")

sys.stdout.write("Enter IP address: ")
sys.stdout.flush()
ipreq = sys.stdin.readline()
IPTextFilePing= "C:\GitHub\Find IP and connect\IPTextFilePing.txt"
is_valid_IPAddress(ipreq,IPTextFilePing)

##########################################################################################
#Find IP add in IPList text file and copy to IPLISTpath
def IPLIST(IPList,IPLISTpath):
    for line in IPList:
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
        if ip:
            # Add each ip to ip text file
            for i in ip:
                a = open(IPLISTpath, "a")
                # Write IP as string
                a.write(str(i))
                #print(i)
                a.write('\n')

##########################################################################################
#Connect to switch and send configuration and save comand in file then find ip and save on IP.txt
def SW_Cofig_File (SWDownlist,SWCONFIG,IPLISTpath,SWCONFIGpath,IPTextFile,Command1,Command2):
    #hostname = str(ipreq)
    #Erase content of SW Down list
    a = open(SWDownlist, "a")
    a.truncate(0)
    IPTextFile
    Hostlist = open(IPTextFile, "r")
    thislist = Hostlist.read()
    data_into_list = thislist.split("\n")
    #hostname = "10.64.164.150"

    try:
        for hostname in data_into_list:
            response = ping(hostname, count=2)
            if response.is_alive:
                print("Device is alive")
                # Connect to host with user and password
                orig_stdout = sys.stdout
                sys.stdout = open("switchfile", "w")
                print(Command1)
                print(Command2)
                # close the file, stop redirecting stdout
                sys.stdout.close()
                sys.stdout = orig_stdout
                # run Netmiko, print what happens on switch, disconnect
                switch = {
                    'host': hostname,
                    'username': 'admin',
                    'password': 'Sud0kU1903sD19',
                    'device_type': 'hp_procurve',
                }
                switchconnect = Netmiko(**switch)
                switchconnect.enable()
                output = switchconnect.send_config_from_file("switchfile")

                # open file and write configuration
                f = open(SWCONFIG, "a")
                f.truncate(0)
                f = open(SWCONFIG, "w")
                f.write(output)
                # print(output)
                switchconnect.disconnect()
                # convert content of config file tostring for regex
                s = str(output)
                # Open lldp neigh file
                lldp_nei_detai = open(SWCONFIG, "r")
                # Read lldp neigh file
                fstring = lldp_nei_detai.readlines()
                # Erase IP.txt content
                IPlisttxt = open(IPLISTpath, "a")
                IPlisttxt.truncate(0)
                # Call IPLIST function for find ip format and save on IP.txt
                IPLIST(fstring, IPLISTpath)
                # Erase SW config file
                if not os.path.exists(SWCONFIGpath):
                    os.remove(SWCONFIGpath)
                f = open(SWCONFIG, "a")
                # write config to hostname file
                f.write(output)
            else:
                print("Host is down")
    except SyntaxError:
        print('Fix your syntax')
    except TypeError:
        print('Oh no! A TypeError has occured')
    except ValueError:
        print('A ValueError occured!')
    except ZeroDivisionError:
        print('Did by zero?')
    else:
        print('No exception')
    finally:
        print('Ok then')

IPTextFilePing= "C:\GitHub\Find IP and connect\IPTextFilePing.txt"
SWCONFIGpathFirst="C:\GitHub\Find IP and connect\SW config"
IPLISTpathFirst = "C:\GitHub\Find IP and connect\IP.txt"
SWCONFIGFirst = "C:\GitHub\Find IP and connect\SW temp config.txt"
SWDownlistFirt = "C:\GitHub\Find IP and connect\SW down list.txt"
Commandshrun = "sh run | includ hostname"
CommandLLDP = "sh lldp nei detai"
SW_Cofig_File (SWDownlistFirt,SWCONFIGFirst,IPLISTpathFirst,SWCONFIGpathFirst,IPTextFilePing,Commandshrun,CommandLLDP)
#def SW_Cofig_File (SWDownlist,SWCONFIG,IPLISTpath,SWCONFIGpath,IPTextFile,Command1,Command2):
##########################################################################################
#Connect to each IP and save config file in host folder
def SW_Config_Folder (SWDownlist,SWCONFIG,SWCONFIGpath,IPLISTpath,Command1,Command2,Command3,Command4,Command5,Command6,Command7):
    # remove all folder and file in SW folder
    if os.path.exists(SWDownlist):
        os.remove(SWDownlist)
    configfolder = SWCONFIGpath
    for dir in os.listdir(configfolder):
        shutil.rmtree(os.path.join(configfolder, dir))

    # time.sleep(2)
    # opening the file in read mode
    Hostlist = open(IPLISTpath, "r")
    # reading the file
    thislist = Hostlist.read()
    # replacing end splitting the text
    # when newline ('\n') is seen.
    data_into_list = thislist.split("\n")

    # Erase SW down list file for new SW down list
    a = open(SWDownlist, "a")

    a.truncate(0)

    # For ping and connect to server
    try:
        for hostname in data_into_list:
            response = ping(hostname, count=2)
            print(hostname)
            # Connect to host with user and password
            Pass_list = ['Sud0kU1903sD19', 'e1Dw@6+fcS*5G3Th1A', '1907sdkTuna1.']
            if response.is_alive:
                command = [Command1, Command2, Command3, Command4, Command5, Command6 , Command7]
                for item in command:
                    print(item)
                    orig_stdout = sys.stdout
                    sys.stdout = open("switchfile", "w")
                    # redirect stdout to file for Netmiko to use later
                    print("sh run | includ hostname")
                    print(item)
                    # close the file, stop redirecting stdout
                    sys.stdout.close()
                    sys.stdout = orig_stdout
                    # run Netmiko, print what happens on switch, disconnect
                    for PASSWORD in Pass_list:
                        switch = {
                            'host': hostname,
                            'username': 'admin',
                            'password': PASSWORD,
                            'device_type': 'hp_procurve',
                        }
                        try:
                            switchconnect = Netmiko(**switch)
                            switchconnect.enable()
                            output = switchconnect.send_config_from_file("switchfile")
                            # open file and write configuration
                            f = open(SWCONFIG, "a")
                            f.truncate(0)
                            f = open(SWCONFIG, "w")
                            f.write(output)
                            print(output)
                            switchconnect.disconnect()

                            # convert content of config file tostring for regex
                            s = str(output)

                            # find host name of file
                            start = '"'
                            end = '"'
                            SWFilename1 = (s[s.find(start) + len(start):s.rfind(end)])
                            print(SWFilename1)
                            # Create textfile with extention
                            SWFilename = str(SWFilename1 + ' ' + str(item) + '.txt')
                            print(SWFilename)
                            # creat folder with hostname of SW
                            newpath = os.path.join(SWCONFIGpath, SWFilename1)
                            if not os.path.exists(newpath):
                                os.makedirs(newpath)
                            # creat string of path
                            newpath = str(newpath)
                            # creat text file in path of hostname
                            filepath = os.path.join(newpath, SWFilename)
                            if not os.path.exists(SWCONFIGpath):
                                os.makedirs(SWCONFIGpath)
                            f = open(filepath, "a")
                            # write config to hostname file
                            f.write(output)

                        except Exception as e:
                            print(e)

            else:
                a = open(SWDownlist, "a")
                # Add down SW to list
                a.write(hostname)
                # new line
                a.write('\n')
                print(hostname, 'is down!')

    # except SyntaxError:
    #     print('Fix your syntax')
    # except TypeError:
    #     print('Oh no! A TypeError has occured')
    # except ValueError:
    #     print('A ValueError occured!')
    # except ZeroDivisionError:
    #     print('Did by zero?')
    # else:
    #     print('No exception')
    finally:
        print('Ok then 2nd')


SWCONFIGpathFirst="C:\GitHub\Find IP and connect\SW config"
IPLISTpathFirst = "C:\GitHub\Find IP and connect\IP.txt"
SWCONFIGFirst = "C:\GitHub\Find IP and connect\SW temp config2.txt"
SWDownlistFirt = "C:\GitHub\Find IP and connect\SW down list.txt"
Command_shrun = "sh run | includ hostname"
Command_LLDP = "sh lldp nei detai"
Command_VLAN = "sh vlan"
Command_CDPNei = "sh cdp nei"
Command_run = "sh lldp info rem"
Command_system = "sh system"
Command_MACadd = "sh mac-add"
SW_Config_Folder (SWDownlistFirt,SWCONFIGFirst,SWCONFIGpathFirst,IPLISTpathFirst,Command_shrun,Command_LLDP,Command_VLAN,Command_CDPNei,Command_run,Command_system,Command_MACadd)

##########################################################################################



