#! /usr/bin/python3
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import os
import subprocess
import signal
from datetime import datetime, timedelta
import lib.ServiceManagment
import time
import sys
import psutil
import json
import lib.TunnelWizard
from configuration import Configuration_Menu
from lib.TunnelCore import FnAutoRestartTunnel,CreateCommamd,Saveit,CheckStatusTunnel,SERVICE_LIST,Generate_SERVICE_LIST
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

current_directory = os.path.dirname(os.path.realpath(__file__))
JsonListFile = os.path.join(current_directory,'conf/config.json')
JsonConfig = lib.BaseFunction.LoadJsonFile(JsonListFile)
LOG_PATH = os.path.join(JsonConfig.get('log_path','/var/log'),'ssh-log')
SSHKEYFile = lib.BaseFunction.GetValue(JsonConfig,"SSHKEY",verbus=False,ReturnValueForNone='')
SSHKEYDir = os.path.join(current_directory,'key')    
SSHKEY = os.path.join(current_directory,'key',SSHKEYFile)
TunnelJsonFilePath = os.path.join(current_directory,'conf/tunnel.json')
TUNNEL_LIST = lib.BaseFunction.LoadJsonFile(JsonFile=TunnelJsonFilePath,Verbus=False,ReternValueForFileNotFound={})
#SERVICE_LIST = JsonConfig.get('services',{})
if os.path.exists(SSHKEY) is False:
    lib.BaseFunction.clearScreen()
    print('\n\n')
    lib.Logo.sshTunnel()
    lib.AsciArt.BorderIt(Text=f'canot find the SSH key File ({SSHKEY})',BorderColor=_fr,TextColor=_fw)
    lib.BaseFunction.FnExit()

if os.path.exists(LOG_PATH) is False:
    os.makedirs(LOG_PATH, exist_ok=True)



######################################################
######################################################

def RefreshTunnelList():
    global TUNNEL_LIST
    TUNNEL_LIST = lib.BaseFunction.LoadJsonFile(JsonFile=TunnelJsonFilePath,Verbus=False,ReternValueForFileNotFound={})    
    return TUNNEL_LIST

def MainMenu(Msg = ''):
    TableView = False
    while True:        
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        #RunWithRoot()
        if len(TUNNEL_LIST) > 0:
            printTunnelList(HorizontalMode=TableView)
        else:
            print('\n')
            lib.AsciArt.BorderIt(Text='No Tunnel Found',BorderColor=_fc,TextColor=_fr)
        if Msg != '':
            print("")
            print("")
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fy,TextColor=_fEx_r)
            Msg = ''
        print(f'\n\n{_fw}( {_fc}c {_fw}) Create tu{_reset}')        
        commandList = ['','c','q']
        if len(TUNNEL_LIST) > 0:
            commandList = ['q','s','d','r','','c','0','#','x']
            print(f'{_fw}( {_fb}s {_fw}) Start all Tunnel{_reset}')        
            print(f'{_fw}( {_fb}d {_fw}) Drop all Tunnel{_reset}')
            print(f'{_fw}( {_fb}r {_fw}) Restart all Tunnel{_reset}')            
            print(f'{_fw}( {_fb}x {_fw}) Configuration {_reset}')
            print(f'{_fw}( {_fy}* {_fw}) Enter tunnel {_fy}code{_fw} for Tunnel Detail{_reset}')
                        
        print(f'\n{_D}# for change View{_reset}')        
        print(f'{_D}q for quit{_reset}')        
        UserInput = input(f'{_B}{_fw}Enter Command >  {_reset}')        
        if UserInput.strip().lower() in commandList:
            if UserInput.strip().lower() == 'q':
                lib.BaseFunction.FnExit()
            elif UserInput.strip().lower() == 's':
                StartAllTunnel()
            elif UserInput.strip().lower() == 'd':
                DropAllSShTunnel()
            elif UserInput.strip().lower() == 'r':                
                DropAllSShTunnel()
                StartAllTunnel()
            elif UserInput.strip().lower() == 'x':
                Configuration_Menu()
            elif UserInput.strip() == 'c':
                TunnelMode = CreateTunnelModeMenu()
                NewTunnel = CreateTunnle(TunnelMode)
                if NewTunnel == {}:
                    Msg = "Create Tunnel Canceled"
                    continue
                else:
                    if SaveNewTunnel(NewTunnel) is False:
                        Msg = "Error on Save Tunnel"
                        continue
            elif UserInput.strip() == '':                
                continue
            elif UserInput.strip().lower() == '#':
                if TableView:
                    TableView = False
                else:
                    TableView = True
                continue
        else:
            if len(TUNNEL_LIST) > 0: 
                for _ in TUNNEL_LIST:                
                    _tunnle = TUNNEL_LIST[_]    
                    findCode = False
                    Msg = ''
                    if _tunnle["Code"].lower() == UserInput.lower().strip():
                        ViewTunnleStatus(_tunnle)
                        findCode = True
                if findCode == False:                
                    if Msg == '':
                        Msg = f"No server found ( {UserInput} )"

def PrintTunnelDetailsOnCreateTunnel(TunnelDict):
    if TunnelDict['Type'] == 'local':
        LocalOrRemoteServerlable = "Local Server"
    elif TunnelDict['Type'] == 'remote':
        LocalOrRemoteServerlable = "Remote Server"    
    elif TunnelDict['Type'] == 'dynamic':
        LocalOrRemoteServerlable = "Local Server (Socks)"
    else:
        LocalOrRemoteServerlable = ""
    print (f"\nTunnel name : {_B}{_fc}{TunnelDict['Name']}{_reset}")
    print (f"Tunnel code : {_B}{_fc}{TunnelDict['Code']}{_reset}")
    print (f"Type : {_B}{_fy}{TunnelDict['Type']}{_reset}")
    print (f"Source Address : {_B}{_fy}{TunnelDict['Source_Server']}:{TunnelDict['Source_port']}{_reset}")
    print (f"Final Port on {LocalOrRemoteServerlable} : {_B}{_fy}{TunnelDict['FinalPort']}{_reset}")
    print (f"SSH Server Details :")
    print (f"  - IP : {_B}{_fy}{TunnelDict['ssh_ip']}{_reset}")
    print (f"  - User : {_B}{_fy}{TunnelDict['ssh_user']}{_reset}")
    print (f"  - Port : {_B}{_fy}{TunnelDict['ssh_port']}{_reset}")
    print (f"Advanced Options :")
    print (f'  - Highly restricted network mode : {_B}{_fy}{TunnelDict["Highly_Restricted_Networks"].get("Enable",False)}{_reset}')
    print (f"  - Monitor Port : {_B}{_fy}{TunnelDict['Highly_Restricted_Networks'].get('MonitorPort',0)}{_reset} Use Only for Highly Restricted Network Mode")


def CreateTunnle(Mode = None,Msg = ''):
    _Name = ''
    _Code = ''
    _ssh_ip = ''
    _ssh_user = ''
    _ssh_port = ''
    _Source_Server = ''
    _Source_port = ''
    _FinalPort = ''
    _Type = ''
    _Keep_Alive = ''
    _Highly_Restricted_Networks_Enable = ''
    _monitorPort = ''    
    TunnelDict = {
        "Name": _Name,
        "Code": _Code,
        "ssh_ip": _ssh_ip,
        "ssh_user": _ssh_user,
        "ssh_port": _ssh_port,
        "Source_Server": _Source_Server,
        "Source_port": _Source_port,
        "FinalPort": _FinalPort,
        "Type": _Type,
        "Keep_Alive": _Keep_Alive,
        "Highly_Restricted_Networks": {
            'Enable': _Highly_Restricted_Networks_Enable,
            'MonitorPort': _monitorPort,
            'ServerAliveInterval': 60,
            'ServerAliveCountMax': 3,
            'ExitOnForwardFailure': 'yes'
        }
    }
    TunnelDict['Type'] = Mode    
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        print("")
        lib.TunnelWizard.TunnelHelpMode(Mode,ColorBox=_fc)
        PrintTunnelDetailsOnCreateTunnel(TunnelDict)        
        if Msg != '':
            print("")
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
        
        ## GET SSH Server Details
        if _ssh_ip == '':
            _ssh_ip = input(f'{_B}{_fw}\n\nEnter 🔑 SSH Server IP Address > {_fy}')
            if _ssh_ip.strip() == '':
                continue         
            else:
                TunnelDict['ssh_ip'] = _ssh_ip
                continue
        if  _ssh_user == '':
            _ssh_user = input(f'{_B}{_fw}\n\nEnter 🔑 SSH Server User Name [ {_fy}root{_fw} ] > {_fy}')
            if _ssh_user.strip() == '':
                _ssh_user = 'root'
                TunnelDict['ssh_user'] = _ssh_user
                continue
            else:
                TunnelDict['ssh_user'] = _ssh_user    
                continue
        if _ssh_port == '':
            _ssh_port = input(f'{_B}{_fw}\n\nEnter 🔑 SSH Server Port [ {_fy}22{_fw} ] > {_fy}')
            if _ssh_port.strip() == '':
                _ssh_port = '22'
                TunnelDict['ssh_port'] = _ssh_port
                continue
            elif _ssh_port.isdigit() and len(_ssh_port) < 6 and len(_ssh_port) > 0 and int(_ssh_port) > 0 and int(_ssh_port) < 65535:            
                TunnelDict['ssh_port'] = _ssh_port
                continue
            else:
                Msg = f'Invalid SSH Port, Please enter a valid port number between 1 and 65535'
                _ssh_port = ''
                continue
        if _Source_Server == '':
            _Source_Server = input(f'{_B}{_fw}\n\nEnter 🔌 Source Server IP Address [ {_fy}IP:Port / Port {_fw}] > {_fy}')
            if _Source_Server.strip() == '':
                continue
            else:
                if ':' in _Source_Server:
                    ip,port = _Source_Server.split(':')
                    if port.isdigit() and len(port) < 6 and len(port) > 0 and int(port) > 0 and int(port) < 65535:
                        SourceAddress = _Source_Server.strip()
                        TunnelDict['Source_Server'] = ip
                        TunnelDict['Source_port'] = port
                        continue
                    else:
                        Msg = f'Invalid Port on Source Adress, Please enter a valid port number between 1 and 65535'
                        _Source_Server = ''
                        continue                        
                else:
                    try:
                        if int(_Source_Server.strip()) > 0 and int(_Source_Server.strip()) < 65535:                            
                            TunnelDict['Source_Server'] = 'localhost'
                            TunnelDict['Source_port'] = _Source_Server.strip()
                            continue
                        else:
                            Msg = f'Invalid Port on Source Adress, Please enter a valid port number between 1 and 65535'
                            _Source_Server = ''
                            continue
                    except:                    
                        Msg = f'Invalid Source Adress, Please enter a valid (IP:Port or Port)'
                        _Source_Server = ''
                        continue                            
        if _FinalPort == '':
            _FinalPort = input(f'{_B}{_fw}\n\nEnter 🏁 Final Port > {_fy}')
            if _FinalPort.strip() == '':
                continue
            elif _FinalPort.isdigit() and len(_FinalPort) < 6 and len(_FinalPort) > 0 and int(_FinalPort) > 0 and int(_FinalPort) < 65535:            
                TunnelDict['FinalPort'] = _FinalPort
                continue
            else:
                Msg = f'Invalid Final Port, Please enter a valid port number between 1 and 65535'
                _FinalPort = ''
                continue
        if _Highly_Restricted_Networks_Enable == '':
            histMsg = """In normal mode, this software protects established tunnels against network disruptions,but if you are facing severe network
            disruptions or if tunnel connections are disconnected after a while due to settings made at the service provider level or infrastructure,
            it is better to activate the severe \'Highly restricted network restriction mode\'."""
            print("")
            lib.AsciArt.BorderIt(Text=histMsg,BorderColor=_fc,TextColor=_fw,WidthBorder=100)                        
            histMsg ="""If \"Highly restricted network restriction mode\" is enabled,The software will use \"Autossh\" instead of \"ssh\". Make sure this program is installed on your system."""
            lib.AsciArt.BorderIt(Text=histMsg,BorderColor=_fc,TextColor=_fw,WidthBorder=100)                                    
            _Highly_Restricted_Networks_Enable = input(f'{_B}{_fw}\n\nEnable ✨ Highly Restricted Networks [ Yes / No ] [ {_fy}Y / N{_fw} ] > {_fy}')
            if _Highly_Restricted_Networks_Enable.strip() == '':
                continue
            elif _Highly_Restricted_Networks_Enable.strip().lower() in ['y','yes']:
                _Highly_Restricted_Networks_Enable = True
                TunnelDict['Highly_Restricted_Networks']['Enable'] = _Highly_Restricted_Networks_Enable
                continue
            elif _Highly_Restricted_Networks_Enable.strip().lower() in ['n','no']:
                _Highly_Restricted_Networks_Enable = False
                TunnelDict['Highly_Restricted_Networks']['Enable'] = _Highly_Restricted_Networks_Enable
                _monitorPort = 0                
                TunnelDict['Highly_Restricted_Networks']['MonitorPort'] = _monitorPort
                continue
            else:
                Msg = f'Invalid Input, Please enter a valid input [ Yes / No ]'
                _Highly_Restricted_Networks_Enable = ''
                continue
        if _Highly_Restricted_Networks_Enable:
            if _monitorPort.strip() == '':
                _monitorPort = input(f'{_B}{_fw}\n\nEnter 🔌 Monitor Port [ {_fy}0{_fw} ] for {_fy}Disable{_fw} > {_fy}')
                if _monitorPort.strip() == '':                    
                    continue
                elif _monitorPort.isdigit():
                    if int(_monitorPort) == 0:                        
                        TunnelDict['Highly_Restricted_Networks']['MonitorPort'] = _monitorPort
                        continue                                        
                    elif int(_monitorPort.strip()) > 0 and int(_monitorPort.strip()) < 65535:                        
                        if CkeckNewMonitorPort(int(_monitorPort)):
                            TunnelDict['Highly_Restricted_Networks']['MonitorPort'] = _monitorPort
                            continue                                                                
                        else:
                            Msg = 'Monitor Port is already in use, Monitor Port must be unique in the all tunnels.'
                            _monitorPort = ''
                            continue
                    else:
                        Msg = f'Invalid Monitor Port, Please enter a valid port number between 1 and 65535'
                        _monitorPort = ''
                        continue
                else:
                    Msg = f'Invalid Monitor Port, Please enter a valid port number between 1 and 65535'
                    _monitorPort = ''
                    continue

        if _Keep_Alive == '':
            histMsg ="""If this option is enabled and the keep-alive service is started, the tunnels will remain active under any circumstances."""
            print("")
            lib.AsciArt.BorderIt(Text=histMsg,BorderColor=_fc,TextColor=_fw,WidthBorder=100)                                    
            _Keep_Alive = input(f'{_B}{_fw}\n\nEnable on 🔒 Keep Alive service [ Yes / No ] [ {_fy}Y / N{_fw} ] > {_fy}')
            if _Keep_Alive.strip() == '':
                continue
            elif _Keep_Alive.strip().lower() in ['y','yes']:
                _Keep_Alive = True
                TunnelDict['Keep_Alive'] = _Keep_Alive
                continue
            elif _Keep_Alive.strip().lower() in ['n','no']:
                _Keep_Alive = False
                TunnelDict['Keep_Alive'] = _Keep_Alive
                continue
            else:
                Msg = f'Invalid Input, Please enter a valid input [ Yes / No ]'
                _Keep_Alive = ''
                continue

        if _Code == '':
            _Code = input(f'{_B}{_fw}\n\nEnter 🔁 Tunnel Code > {_fy}')
            if _Code.strip() == '':
                continue
            _Code = _Code[0:3]
            for _t in TUNNEL_LIST:
                TUNNEL = TUNNEL_LIST[_t]
                if _Code.lower() == TUNNEL['Code'].lower():
                    Msg = f'Tunnel Code is already in use, Please enter a unique Tunnel Code.'
                    _Code = ''
                    break
            if _Code == '':                
                continue
            else:
                TunnelDict['Code'] = _Code
                continue
        if _Name.strip() == '':    
            _Name = input(f'{_B}{_fw}\n\nEnter 🏷️  Tunnel Name > {_fy}')
            if _Name.strip() == '':
                continue
            else:
                TunnelDict['Name'] = _Name
                continue
        UserInput = input(f' {_B}{_fw}\n\n Create Tunnel [ Yes / No' f' ] [ {_fy}Y / N{_fw} ] > {_fy}')
        if UserInput.lower().strip() in ['y','yes']:
            return TunnelDict
        elif UserInput.lower().strip() in ['n','no']:
            return {}
        else:
            Msg = f'Invalid Input, Please enter a valid input [ Yes / No ]'
            continue


def CkeckNewMonitorPort(NewPort = None):
    if TUNNEL_LIST == []:
        return True
    else:
        for _t in TUNNEL_LIST:
            tunnel = TUNNEL_LIST[_t]
            if tunnel["Highly_Restricted_Networks"].get('Enable',False):
                MonitorPort = tunnel["Highly_Restricted_Networks"].get('MonitorPort',0)
                if MonitorPort != 0:
                    if NewPort == MonitorPort:
                        return False
    return True


def SaveNewTunnel(TunnelDict,NoWait=False):    
    TUNNEL_LIST[TunnelDict['Code']] = TunnelDict    
    try:


        with open(TunnelJsonFilePath, 'w') as json_file:
            json.dump(TUNNEL_LIST, json_file, indent=4)
            print(f"{_B}{_fw}\nTunnel [ {_fEx_g}{TunnelDict['Name']}{_fw} ] Saved Successfully{_reset}")
            if NoWait is False:
                lib.BaseFunction.PressEnterToContinue()
            return True
    except:
        print(f"{_fr}Error on Update [ {TunnelJsonFilePath} ] operation Faild{_reset}\n")
        lib.BaseFunction.PressEnterToContinue()
        return False

def CreateTunnelModeMenu(ErrMsg = ''):
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        lib.TunnelWizard.TunnelHelp(Color=_fc)
        if ErrMsg != '':
            lib.AsciArt.BorderIt(Text=ErrMsg,BorderColor=_fr,TextColor=_fy)
            ErrMsg = ''
        msg = f'{_B}{_fw}\n Create New Tunnel [ Local / Remote / Dynamic ]{_reset}'
        userInput = input(f'{msg} {_N}{_fy} [ L / R / D ] {_N}{_fw} > {_N}')
        if userInput.lower().strip() in ['l','local']:
            return 'local'
        elif userInput.lower().strip() in ['r','remote']:
            return 'remote'
        elif userInput.lower().strip() in ['d','dynamic']:
            return 'dynamic'
        else:
            ErrMsg = f"Invalid input: [ {userInput} ], Please enter 'L', 'R', or 'D'."

def ViewTunnleStatus(TunnelDict,OnNewSession=True,ReturnDictResualt=False):
    Msg = ''
    ResualtDict= {}
    while True:
        rst = CheckStatusTunnel(TunnelDict)
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()    
        if Msg != '':
            print("")
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
            Msg = ''            
        if rst[0]:
            print(f'\nTunnel is : {_fw}{_bg} READY {_reset}')
            print(f"\nTunnel {_fb}{TunnelDict['Name']}{_fw} is running with PID : {_by}{_fbl} {rst[2]} {_reset}")
            ResualtDict["pid"] = rst[1]
            ResualtDict["isActive"] = True
            details = GetProcessDetails(rst[2])
        else:
            print(f'\nTunnel is : {_fw}{_bb} STOP {_reset}')
            print(f"\nTunnel {_fw}{TunnelDict['Name']}{_fw} is not running.{_reset}")            
            ResualtDict["pid"] = ''
            ResualtDict["isActive"] = False
        
        TunnelType = TunnelDict.get('Type','').lower()
        if TunnelType == 'local':
            LocalOrRemoteServerlable = "Local Server"
        elif TunnelType == 'remote':
            LocalOrRemoteServerlable = "Remote Server"    
        elif TunnelType == 'dynamic':            
            LocalOrRemoteServerlable = "Local Server (Socks)"
        if TunnelDict["Highly_Restricted_Networks"].get('Enable',False):
            _mode = f'{_by}{_fbl} ENABLED '
        else:
            _mode = f'{_bbl} DISABLED '        
        ModeStr = f'\nHighly restricted network mode : {_mode}{_reset}'        
        _keyPath = ''
        _authentication = TunnelDict.get("authentication","")
        if _authentication.lower() == 'password':
            _authenticationStr = f'🔑 Password Authentication'
        elif _authentication.lower() in ['key','key_path']:
            _authenticationStr = f'🔐 Key Authentication'
            _keyPath = TunnelDict.get("key_path","")
        elif _authentication.lower() == '':
            _authenticationStr = f'🔐 Use Defualt Authentication'
        else:
            _authenticationStr = f'🔐 Use Defualt Authentication'


                        
        print(f"{ModeStr}")
        print(f"\nTunnel name : {_fc}{TunnelDict['Name']}{_reset}")
        print(f"Tunnel code : {_fc}{TunnelDict['Code']}{_reset}")
        print(f"IP : {_fc}{TunnelDict['ssh_ip']}{_reset}")
        print(f"User : {_fc}{TunnelDict['ssh_user']}{_reset}")
        print(f"Port : {_fc}{TunnelDict['ssh_port']}{_reset}")
        print(f"Source Address : {_fc}{TunnelDict['Source_Server']}{_reset}")
        print(f"Final Port on {LocalOrRemoteServerlable} : {_B}{_fc}{TunnelDict['FinalPort']}{_reset}")
        print(f"Authentication Method : {_fc}{_authenticationStr}{_reset}")
        if _keyPath != '':
            print(f"Path of Key File : {_fc}{_keyPath}{_reset}")
        print (f"Advanced Options :")
        print (f"  - Monitor Port : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('MonitorPort',0)}{_reset} Use Only for Highly Restricted Network Mode")
        print (f"  - ServerAliveInterval : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ServerAliveInterval',0)}{_reset}")
        print (f"  - ServerAliveCountMax : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ServerAliveCountMax',0)}{_reset}")
        print (f"  - ExitOnForwardFailure : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure','no')}{_reset}")        

        if rst[0]:
            if details[0]:                
                print (f'\n{"-"*30} Process Details {"-"*30}')
                print(f"Process Name : {_fy}{details[1]['name']}{_reset}")
                print(f"Execute Path : {_fy}{details[1]['exe']}{_reset}")
                print(f"Command Line : {_fy}{details[1]['cmdline']}{_reset}")
                print(f"Status : {_fy}{details[1]['status']}{_reset}")
                print(f"User : {_fy}{details[1]['user']}{_reset}")
                print(f"Memory Info : ")
                print(f"  - RSS : {_fy}{details[1]['memory']['memory_info_RSS']}{_reset}")
                print(f"  - VMS : {_fy}{details[1]['memory']['memory_info_VMS']}{_reset}")
                print(f"Start Time : {_fy}{details[1]['start_time']}{_reset}")
                print(f"CPU Info : ")
                print(f"  - CPU Percent : {_fy}{details[1]['cpu_percent']}{_reset}")
                print(f"  - Parent Process : {_fy}{details[1]['parent']}{_reset}")
                print(f"  - Children Process : {_fy}{details[1]['children']}{_reset}")
                print(f"Network Connections : ")
                ResualtDict["Process"] = {}
                ResualtDict["Process"]["name"] = details[1]['name']
                ResualtDict["Process"]["exe"] = details[1]['exe']
                ResualtDict["Process"]["cmdline"] = details[1]['cmdline']
                ResualtDict["Process"]["status"] = details[1]['status']
                ResualtDict["Process"]["user"] = details[1]['user']
                ResualtDict["Process"]["memory-RSS"] = details[1]['memory']['memory_info_RSS']
                ResualtDict["Process"]["memory-VMS"] = details[1]['memory']['memory_info_VMS']
                ResualtDict["Process"]["start_time"] = details[1]['start_time']
                ResualtDict["Process"]["cpu_percent"] = details[1]['cpu_percent']
                ResualtDict["Process"]["parent_process"] = details[1]['parent']
                ResualtDict["Process"]["children_process"] = details[1]['children']                
                for _conn in details[1]['network']:
                    listofConections = []
                    listofConections.append(_conn.strip())
                    print(f"  - {_fy}{_conn}{_reset}")
                print (f'\n{"-"*30} Process Details {"-"*30}')
                ResualtDict['connections'] = listofConections
            else:                                
                print(f'{_fr}Error getting process details.{_reset}')    
                print(details[1])
        else:
            print (f'\n{"-"*50}')
        
        ## Only Return Dict Resualt for API Use / Telegram Bot
        if ReturnDictResualt:
            return ResualtDict

        if rst[0]:
            print(f'\n{_fw}( {_fc}s {_fw}) Stop Tunnel.{_reset}')
        else    :
            print(f'\n{_fw}( {_fc}s{_fw} ) Start Tunnel.{_reset}')    
        print(f'{_fw}( {_fr}d {_fw}) Delete Tunnel.{_reset}')        
        print(f'{_fw}( {_fc}0 {_fw}) Back to Start Menu.{_reset}')
        print(f'{_fw}( {_fc}Enter {_fw}) Check Status.{_reset}')
        print(f'\n{_D}q for quit{_reset}')
        UserInput = input(f'{_B}{_fw}Enter Command :  {_reset}')        
        if UserInput.strip().lower() in ['0','s','q','r','d']:
            if UserInput.lower().strip() == '0':
                if rst[0]:
                    return True
                else:
                    return False
            elif UserInput.lower().strip() == 'q':
                lib.BaseFunction.FnExit()                                
            elif UserInput.lower().strip() == 's':
                if rst[0]:
                    KillProcessByPID(rst[2])
                else:    
                    _rst = FnStartTunnel(TunnelDict,StartNewSession=OnNewSession)
                    if _rst[0] is False:
                        Msg = f'Error starting tunnel {TunnelDict["Name"]} >> {_rst[1]}'                        
            elif UserInput.lower().strip() == 'd':        
                _confirm = input(f'\n{_fr}Are you sure you want to delete the tunnel? [ Y / N ] > {_reset}')
                if _confirm.lower().strip() in ['y','yes']:
                    DeleteTunnel(TunnelDict)
                    return True
                elif _confirm.lower().strip() in ['n','no']:
                    continue
                else:
                    _msg = f'{_fr}Invalid Input, Please enter a valid input [ Yes / No ]'
                    continue

def StartAllTunnel(ReturnResualt=False):
    TUNNEL_LIST = RefreshTunnelList()
    MsgList = []    
    RstDict = {}
    for _ in TUNNEL_LIST:
        _tunnel = TUNNEL_LIST[_]        
        CheckSts = CheckStatusTunnel(_tunnel)
        RstDict[_tunnel['Code']] = {}
        RstDict[_tunnel['Code']]['status'] = CheckSts[0]
        RstDict[_tunnel['Code']]['pid'] = CheckSts[2]
        if CheckSts[0]:
            Msg = f"❕ Tunnel {_tunnel['Name']} is already running."
            print(Msg)
            RstDict[_tunnel['Code']]['msg'] = Msg
        else:
            _Rst = FnStartTunnel(_tunnel)
            if _Rst[0] is False:
                msg = f"❌ Tunnel {_tunnel['Name']} not started ❌\n\nlogs :\n{'-'*10} {_Rst[1]}\n{'-'*10}"
            else:
                msg = f"▶️ Tunnel {_tunnel['Name']} Started Successfully."
            MsgList.append(msg)
            RstDict[_tunnel['Code']]['pid'] = _Rst[2]
            RstDict[_tunnel['Code']]['msg'] = msg

    if ReturnResualt:
        return RstDict
    
    if MsgList != []:        
        for _tunnel in MsgList:
            lib.AsciArt.BorderIt(Text=_tunnel,BorderColor=_fr,TextColor=_fw)
        print()
        lib.BaseFunction.PressEnterToContinue()    

def DropAllSShTunnel(ReturnResualt=False):    
    _TUNNEL_LIST = RefreshTunnelList()
    rstDict = {}
    for _ in _TUNNEL_LIST:
        _tunnel = _TUNNEL_LIST[_]        
        Name = _tunnel['Name']
        _RST = CheckStatusTunnel(_tunnel)
        rstDict[_tunnel['Code']] = {}
        if _RST[0]:
            KillProcessByPID(_RST[2])
            msg = f"⏹️ Tunnel {_tunnel['Name']} Stopped Successfully."
            print(msg)            
            rstDict[_tunnel['Code']]['stoped'] = True
            rstDict[_tunnel['Code']]['pid'] = _RST[2]
            rstDict[_tunnel['Code']]['msg'] = msg
        else:
            rstDict[_tunnel['Code']]['stoped'] = False
            rstDict[_tunnel['Code']]['pid'] = -1
            rstDict[_tunnel['Code']]['msg'] = f'❕ Tunnel (( {Name} )) not Running.'
            
    return rstDict
            
def KillProcessByPID(pid,Verbus=False):
    try:        
        pid = int(pid)        
        os.kill(pid, signal.SIGTERM)  # SIGTERM is a graceful termination signal        
        return True,''
    except ProcessLookupError:
        errrmsg = 'No process with PID {pid} was found.'
        if Verbus:            
            print(errrmsg)
        return False,errrmsg
    except ValueError:
        errrmsg = "Invalid PID: {pid}"
        if Verbus:            
            print(errrmsg)
        return False,errrmsg
    except PermissionError:
        errrmsg = f"Permission denied to kill process {pid}."
        if Verbus:            
            print(errrmsg)
        return False,errrmsg
    except Exception as e:
        errrmsg = f"Error killing process {pid}: {e}"
        if Verbus:            
            print(errrmsg)
        return False

def GetTunnelStatusByDict(_TunnelDict):
    _Title = f"{_TunnelDict['Name']}"
    _Code = f"{_TunnelDict['Code']}"        
    _LServer = _TunnelDict.get("Source_Server","localhost")
    _LPort = _TunnelDict.get("Source_port",None)
    _SourceOrRemote = f"{_LServer}:{_LPort}"
    _sshPort = _TunnelDict.get("ssh_port",22)
    _sshIp = _TunnelDict.get("ssh_ip",None)
    _sshUser = _TunnelDict.get("ssh_user","root")
    _SshServer = f"{_sshUser}@{_sshIp}:{_sshPort}"
    _Type = _TunnelDict.get("Type","").upper()        
    _authentication = _TunnelDict.get("authentication","")
    if  _authentication.lower() == '':
        _authentication = f'Defualt'
    if _Type == "LOCAL":            
        _FinalIP = lib.BaseFunction.GetLocalIP()        
    elif _Type == "REMOTE":            
        _FinalIP = f'{_TunnelDict["ssh_ip"]}'
    elif _Type == "DYNAMIC":            
        _FinalIP = f'{_TunnelDict["ssh_ip"]}'
    else:            
        _FinalIP = ''
    _rst = CheckStatusTunnel(_TunnelDict)
    _pid = ''
    if _rst[0]:            
        _status = True
        _Final_adress = f'{_FinalIP}:{_TunnelDict["FinalPort"]}'
        _pid = _rst[2]
    else:            
        _status = False
        _Final_adress = f'{_TunnelDict["FinalPort"]}'
    
    if _TunnelDict.get('Keep_Alive',False):
        _keppAlive = f'Enable (in keep-alive service)'
    else:
        _keppAlive = f'disable'
    if _TunnelDict["Highly_Restricted_Networks"].get('Enable',False):            
        ModeChr = f'enable'
    else:
        ModeChr = f'disable'

    _isActive = _TunnelDict.get('is_active',True)

    TunnelStatus = {}
    TunnelStatus['Title'] = _Title
    TunnelStatus['source'] = _SourceOrRemote
    TunnelStatus['source'] = _SourceOrRemote
    TunnelStatus['ssh_server'] = _SshServer
    TunnelStatus['type'] = _Type
    TunnelStatus['authentication'] = _authentication
    TunnelStatus['final_adress'] = _Final_adress
    TunnelStatus['running'] = _status
    TunnelStatus['keep_alive_mode'] = _keppAlive
    TunnelStatus['highly_restricted_networks_mode'] = ModeChr
    TunnelStatus['tunnel_enabled'] = _isActive
    TunnelStatus['pid'] = _pid
    return TunnelStatus

def GetStatusAllTunnel():
    _TUNNEL_LIST = RefreshTunnelList()
    TunnelStatus = {}
    for _T in _TUNNEL_LIST:
        _TunnelDict = _TUNNEL_LIST[_T]        
        _TunnelSTS = GetTunnelStatusByDict(_TunnelDict)
        TunnelStatus[_TunnelDict['Code']] = _TunnelSTS
    return TunnelStatus

def printTunnelList(HorizontalMode = False):
    if HorizontalMode:
        printTunnelListHorizontal()
        return
    _TUNNEL_LIST = RefreshTunnelList()
    for _T in _TUNNEL_LIST:            
        _TunnelDict = _TUNNEL_LIST[_T]        
        _LServer = _TunnelDict.get("Source_Server","localhost")
        _LPort = _TunnelDict.get("Source_port",None)
        _sshPort = _TunnelDict.get("ssh_port",22)
        _sshIp = _TunnelDict.get("ssh_ip",None)
        _sshUser = _TunnelDict.get("ssh_user","root")        
        _Type = _TunnelDict.get("Type","").upper()        
        _authentication = _TunnelDict.get("authentication","")
        if _authentication.lower() == 'password':
            _authenticationStr = f'🔑 Password Authentication'
        elif _authentication.lower() in ['key','key_path']:
            _authenticationStr = f'🔐 Key Authentication'
        elif _authentication.lower() == '':
            _authenticationStr = f'🔐 Use Defualt Authentication'
        else:
            _authenticationStr = f'🔐 Use Defualt Authentication'
        if _Type == "LOCAL":
            _tColor = _fg
            _FinalIP = lib.BaseFunction.GetLocalIP()        
        elif _Type == "REMOTE":
            _tColor = _fr
            _FinalIP = f'{_TunnelDict["ssh_ip"]}'
        elif _Type == "DYNAMIC":
            _tColor = _fm
            _FinalIP = f'{_TunnelDict["ssh_ip"]}'
        else:
            _tColor = _fw
            _FinalIP = ' - '
        _rst = CheckStatusTunnel(_TunnelDict)
        if _rst[0]:
            _Icon = '▶️'
            _status = 'Running'
            _color = f'{_fEx_y}'
            _FinalPort = f'{_Icon}  {_color}{_FinalIP}:{_TunnelDict["FinalPort"]}'
            _titelColor = f'{_bg}{_fbl}'
            _StatusColor = f'{_by}{_fbl}'
        else:
            _Icon = '⏸️'
            _status = 'Stopped'
            _FinalPort = f'{_Icon}  {_TunnelDict["FinalPort"]}'
            _titelColor = f'{_bc}{_fbl}'        
            _StatusColor = f'{_bbl}{_fw}'
        if _TunnelDict.get('Keep_Alive',False):
            _keppAlive = f'🔒 {_fg}Enabled{_reset}{_D} in keep-alive service{_reset}'
        else:
            _keppAlive = f'🔓 {_D}{_fw}Disabled{_reset}'
        if _TunnelDict["Highly_Restricted_Networks"].get('Enable',False):
            ModeChr = f'✨ {_D}Highly Restricted Networks{_reset}'
        else:
            ModeChr = f'🔗 {_D}standard {_reset}'
        _Title = f"{_TunnelDict['Name']}"
        _Code = f"{_TunnelDict['Code']}"
        
        _SourceOrRemote = f"{_LServer}:{_LPort}"
        _SshServer = f"{_sshUser}@{_sshIp}:{_sshPort}"
        _FinalPort = f"{_FinalPort}"
        _type = f"{_tColor}{_Type}{_reset}"
        sp = ' ' * 10 
        print(f'\n\n{_titelColor}Title      {_reset}:{_titelColor} {_Title}{sp}{_reset}\n')
        print(f'Status     : {_StatusColor} {_status} {_reset} ')
        print(f'Code       : {_fy}{_Code} {_reset} ')
        print(f'Mode       : {ModeChr} ')
        print(f'Keep Alive : {_keppAlive} ')
        print(f'Server     : {_fc}{_SshServer}{_reset} ')        
        print(f'Source     : {_fc}{_SourceOrRemote}{_reset} ')
        print(f'Auth Type  : {_fy}{_authenticationStr}{_reset} ')        
        print(f'Type       : {_type}')
        print(f'Final Port : {_FinalPort}')




        #return f"{_Mode} {_Title} {_type} {_SourceOrRemote} {_SshServer} {_FinalPort}"

def printTunnelListHorizontal():
    TitleStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Name (code)', target_length=50, AlignmentMode='center')}{_reset}"
    TypeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Type', target_length=10, AlignmentMode='center')}{_reset}"
    SourceStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Source', target_length=18, AlignmentMode='center')}{_reset}"
    SSHServerStr = f"{_bb}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='SSH Server', target_length=30, AlignmentMode='center')}{_reset}"
    FinalPortStr = f"{_by}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Final Port', target_length=30, AlignmentMode='center')}{_reset}"
    ModeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Mode', target_length=6, AlignmentMode='center')}{_reset}"
    print(f"\n{ModeStr} {TitleStr} {TypeStr} {SourceStr} {SSHServerStr} {FinalPortStr}\n")
    for _ in TUNNEL_LIST:
        _tunnel = TUNNEL_LIST[_]
        a = GenerateTunnelLine(_tunnel)
        print(a)


def GenerateTunnelLine(Tunnel):
    _LServer = lib.BaseFunction.GetValue(Tunnel, "Source_Server")
    _LPort = lib.BaseFunction.GetValue(Tunnel, "Source_port")
    _sshPort = lib.BaseFunction.GetValue(Tunnel, "ssh_port")
    _sshIp = lib.BaseFunction.GetValue(Tunnel, "ssh_ip")
    _sshUser = lib.BaseFunction.GetValue(Tunnel, "ssh_user")
    _Type = lib.BaseFunction.GetValue(Tunnel, "Type").upper()
    if _Type == "LOCAL":
        _tColor = _fb
        _FinalIP = lib.BaseFunction.GetLocalIP()        
    elif _Type == "REMOTE":
        _tColor = _fc
        _FinalIP = f'{Tunnel["ssh_ip"]}'
    elif _Type == "DYNAMIC":
        _tColor = _fm
        _FinalIP = f'{Tunnel["ssh_ip"]}'
    else:
        _tColor = _fw
        _FinalIP = ' - '
    _rst = CheckStatusTunnel(Tunnel)
    if _rst[0]:
        _Icon = '▶️'        
        _FinalPort = f'{_Icon}  {_FinalIP}:{Tunnel["FinalPort"]}'
        _clPort = f'{_bg}{_fbl}'        
    else:
        _Icon = '⏸️'        
        _FinalPort = f'{_Icon}  {Tunnel["FinalPort"]}'
        _clPort = f'{_fw}'        
    if Tunnel.get('Keep_Alive',False):
        _keppAlive = '🔒'
    else:
        _keppAlive = '🔓'
    if Tunnel["Highly_Restricted_Networks"].get('Enable',False):
        ModeChr = f'✨ {_keppAlive}'        
    else:
        ModeChr = f'🔗 {_keppAlive}'
    #FullName = f"{Tunnel['Name']} ({_fy}{Tunnel['Code']}{_fw})"
    FullName = f"{Tunnel['Name']} ({Tunnel['Code']})"
    _Title = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=FullName, target_length=50, AlignmentMode='left')}{_reset}"
    _SourceOrRemote = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_LServer}:{_LPort}', target_length=18, AlignmentMode='left')}{_reset}"
    _SshServer = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_sshUser}@{_sshIp}:{_sshPort}', target_length=30, AlignmentMode='left')}{_reset}"
    _FinalPort = f"{_clPort}{lib.AsciArt.FnAlignmentStr(originalString=_FinalPort , target_length=30, AlignmentMode='left')}{_reset}"
    _type = f"{_tColor}{lib.AsciArt.FnAlignmentStr(_Type, target_length=10, AlignmentMode='left')}{_reset}"
    _Mode = f"{_fy}{lib.AsciArt.FnAlignmentStr(ModeChr, target_length=6, AlignmentMode='left')}{_reset}"
    return f"{_Mode} {_Title} {_type} {_SourceOrRemote} {_SshServer} {_FinalPort}"


def RunWithRoot():
    if lib.BaseFunction.User_is_root() is False:
        msg1 = """Tunnel Function requires root privileges, Attempting to restart with sudo..."""
        print('\n\n')
        lib.AsciArt.BorderIt(Text=msg1,BorderColor=_fr,TextColor=_fy,WidthBorder=100)
        print('\n\n')
        #lib.BaseFunction.PressEnterToContinue()
        try:
            # Re-run the script with sudo
            sudo_command = ['sudo', sys.executable] + sys.argv
            subprocess.run(sudo_command, check=True)
        except subprocess.CalledProcessError:
            print("Failed to run with elevated privileges.")
            lib.BaseFunction.FnExit()

def RunAsRoot():
    if lib.BaseFunction.User_is_root() is False:
        msg1 = """Tunnel Function requires root privileges"""
        print('\n\n')
        lib.AsciArt.BorderIt(Text=msg1,BorderColor=_fr,TextColor=_fy,WidthBorder=100)
        print('\n\n')        
        lib.BaseFunction.PressEnterToContinue()
        return False
    return True

##def CreateCommamd(TunnleDict,TypeOfTunnel):        
##    Highly_Restricted_Networks = TunnleDict["Highly_Restricted_Networks"].get('Enable',False)
##    if Highly_Restricted_Networks: 
##        _sshCommandMode = 'autossh'
##    else:    
##        _sshCommandMode = 'ssh'
##
##    if TypeOfTunnel == 'local':        
##        _SSHType = '-L'
##        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Source_Server']}:{TunnleDict['Source_port']}"
##    elif TypeOfTunnel == 'remote':
##        _SSHType = '-R'
##        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Source_Server']}:{TunnleDict['Source_port']}"
##    elif TypeOfTunnel == 'dynamic':
##        _SSHType = '-R' 
##        _SSHTypeServer = f"{TunnleDict['FinalPort']}"        
##    else:
##        print(f"Unknown Tunnel Type: {TypeOfTunnel} for {TunnleDict['Name']}")
##        lib.BaseFunction.PressEnterToContinue()
##    
##
##    CommandLst = []    
##
##    CommandLst.append(_sshCommandMode)
##
##    if Highly_Restricted_Networks:
##        CommandLst.append('-M')
##        CommandLst.append(str(TunnleDict["Highly_Restricted_Networks"].get('MonitorPort',0)))
##    CommandLst.append('-N')
##    CommandLst.append(_SSHType)
##    CommandLst.append(_SSHTypeServer)
##    CommandLst.append('-p')
##    CommandLst.append(str(TunnleDict.get('ssh_port','22')))
##    CommandLst.append('-i')
##    CommandLst.append(SSHKEY)
##    CommandLst.append('-o')
##    CommandLst.append(f"ServerAliveInterval={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveInterval',0)}")
##    CommandLst.append('-o')
##    CommandLst.append(f"ServerAliveCountMax={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveCountMax',0)}")
##    CommandLst.append('-o')
##    CommandLst.append(f"ExitOnForwardFailure={TunnleDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure','no')}")
##    CommandLst.append('-o')
##    CommandLst.append("StrictHostKeyChecking=no")
##    CommandLst.append('-o')
##    CommandLst.append("UserKnownHostsFile=/dev/null")
##    CommandLst.append(f"{TunnleDict['ssh_user']}@{TunnleDict['ssh_ip']}")
##    return CommandLst


def FnStartTunnel(TunnleDict = None,StartNewSession = True,DebugMode = False):
    IsActive = TunnleDict.get('is_active',True)
    if IsActive is False:
        msg = f"🔥😵🔥 Tunnel [ {TunnleDict['Name']} ] is deactivated, Please activate it first."
        return  False,msg,-1
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower(),DebugMode=DebugMode)
    TunnelCode = TunnleDict['Code']
    try:

        with open(f"{LOG_PATH}/{TunnelCode}.log", "a") as log:
            process = subprocess.Popen(
                Command,
                stdout=log,
                stderr=log,
                stdin=subprocess.DEVNULL,
                start_new_session=True
            )
        time.sleep(1)

        _rst = CheckStatusTunnel(TunnleDict)
        if _rst[0]:
            return True,'',_rst[1]
        else:
            return False,'',_rst[1]
    except Exception as e:
        print(f"Exception: {e}")
        msg = (f"🔥 Exception occurred while starting autossh: {e}")        

        return  False,msg    

def CheckAutoSSHCommand():
    """Executes a command and returns its output."""
    command = ['autossh','-V']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True  # Return the output as a string, removing leading/trailing whitespace.
    except subprocess.CalledProcessError as e:        
        return None  # Or raise an exception, depending on your needs.
    except FileNotFoundError:        
        return False
    

def GetProcessDetails(pid):
    """Get detailed information about a process if it exists."""
    details = {}
    try:
        # Check if the process exists
        process = psutil.Process(pid)
        
        # Basic process information
        #print(f"\nPID {pid} found. Process details:")
        #print("=" * 50)
        
        # Process basic info
        try:
            parent = process.parent()
            parentDetails = f"PID {parent.pid} ({parent.name()})"            
        except (psutil.NoSuchProcess, AttributeError):
            parentDetails = 'Not available'

        children = process.children()
        if children:
            for child in children[:5]:  # Limit to first 5 children
                childrenDetail = f"  PID {child.pid} ({child.name()})"                
            if len(children) > 5:                
                childrenDetail = f"  ... and {len(children) - 5} more"
        else:
            childrenDetail = 'None'
        memory_info = process.memory_info()
        create_time = datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        CMDStr = ' '.join(process.cmdline())
        connectionsList = []
        try:            
            connections = process.net_connections()
            #connections = process.connections()
            if connections:                                
                for conn in connections[:5]:  # Limit to first 5 connections
                    local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"                                                                                                    
                    connectionsList.append(f"  {str(conn.type)} - Local: {local} Remote: {remote} ({conn.status})")
                if len(connections) > 5:
                    connectionsList.append(f"  ... and {len(connections) - 5} more connections")
                    #print(f"  ... and {len(connections) - 5} more connections")
            else:
                connectionsList.append("  None")                
        except (psutil.AccessDenied, psutil.ZombieProcess):            
            connectionsList.append("  Access denied or zombie process")


        details = { 
            'name': process.name(),
            'exe': process.exe(),
            'cmdline': CMDStr,
            'status': process.status(),
            'user': process.username(),
            'memory':{
                'memory_info_RSS': f'{memory_info.rss / (1024 * 1024):.2f} MB',
                'memory_info_VMS': f'{memory_info.vms / (1024 * 1024):.2f} MB'
            },
            'start_time': create_time,
            'cpu_percent': f'{process.cpu_percent(interval=0.1):.1f}%',
            'parent': parentDetails,
            'children': childrenDetail,
            'network': connectionsList
        }
    
        return True, details
        
    except psutil.NoSuchProcess:
        msg = f"PID {pid} not found."
        return False , msg
    except psutil.AccessDenied:
        msg = f"PID {pid} found, but access was denied to get process details."
        return True, msg
    except Exception as e:
        msg = f"An error occurred: {e}"
        return False, msg

def MonitorPortIsUniq():
    """Check if the MonitorPort is unique across all tunnels."""
    MonitorPortlist = []
    for tunnel in TUNNEL_LIST:
        if tunnel["Highly_Restricted_Networks"].get('Enable',False):
            MonitorPort = tunnel["Highly_Restricted_Networks"].get('MonitorPort',0)
            if MonitorPort != 0:
                if MonitorPort in MonitorPortlist:
                    msg = f"MonitorPort {tunnel['Name']}({MonitorPort}) is not unique across tunnels."                                        
                MonitorPortlist.append(MonitorPort)

def FnHelp():
    msg = """This program manage SSH tunnels between two Linux servers, run in UI or parameter mode (for scheduled execution). also This solution can be used for all methods for bypass limitations in highly restricted networks.
Refer to the GitHub project documentation to learn how it works."""
    print("")
    lib.AsciArt.BorderIt(Text=msg,WidthBorder=100,BorderColor=_fc,TextColor=_fw)
    print(f"\n{_fw}Syntax:")
    print(f'{_fc}  ./tunnel.py    {_fw}: Run Tunnel Manegment{_reset}')
    print(f'{_fc}  ./tunnel.py -s {_fw}: Start All Tunnel{_reset}')
    print(f'{_fc}  ./tunnel.py -d {_fw}: Drop All Tunnel{_reset}')
    print(f'{_fc}  ./tunnel.py <tunnel code> {_fw}: View Tunnel Status{_reset}\n')
    

def DeleteTunnel(TunnelDict,NoWait=False):
    """Delete a tunnel from the list."""
    NewTunnelList = {}
    global TUNNEL_LIST

    for _t in TUNNEL_LIST:
        tunnel = TUNNEL_LIST[_t]
        if tunnel['Code'] != TunnelDict['Code']:
            NewTunnelList[tunnel['Code']] = tunnel

    TUNNEL_LIST = NewTunnelList
    #TUNNEL_LIST = [tunnel for tunnel in TUNNEL_LIST if tunnel['Code'] != TunnelDict['Code']]
    try:
        with open(TunnelJsonFilePath, 'w') as json_file:
            json.dump(TUNNEL_LIST, json_file, indent=4)
            print(f"{_B}{_fw}\nTunnel [ {_fEx_g}{TunnelDict['Name']}{_fw} ] Deleted Successfully!{_reset}")
            TUNNEL_LIST = NewTunnelList
            if NoWait is False:
                lib.BaseFunction.PressEnterToContinue()
            return True
    except:
        print(f"{_fr}Error on Update [ {TunnelJsonFilePath} ] operation Faild{_reset}\n")
        if NoWait is False:
            lib.BaseFunction.PressEnterToContinue()
        return False
        

def GetTunnelLogDetails(TunnelDict,NumLines=20):
    """Get the last N lines of the tunnel log file."""
    TunnelCode = TunnelDict['Code']
    LogFilePath = f"{LOG_PATH}/{TunnelCode}.log"
    if not os.path.isfile(LogFilePath):
        return False, f"Log file for tunnel {TunnelDict['Name']} does not exist."
    
    try:
        with open(LogFilePath, 'r') as log_file:
            lines = log_file.readlines()
            last_lines = lines[-NumLines:] if len(lines) >= NumLines else lines
            return True, ''.join(last_lines)
    except Exception as e:
        return False, f"❌ Error reading log file: {e}"


def ClearTunnleLog(TunnelCode):
    LogFilePath = f"{LOG_PATH}/{TunnelCode}.log"
    try:
        with open(LogFilePath, "r+") as f:
            f.truncate(0)
    except Exception as e:
        return False,f'❌ Error on Clear Logd \n{e}'
    return True, "🧹 🧹 🧹  Clear Tunnel log Successfully 🧹 🧹 🧹"


####### API

def EnableorDisableTunnelByCode(TunnelCode:str,Changeto:bool):    
    _TUNNEL_LIST = RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if _t.lower().strip() == TunnelCode.lower().strip():            
            tunnel['is_active'] = Changeto
            _rst = lib.BaseFunction.SaveJsonFile(JsonFile=TunnelJsonFilePath,JsonData=TUNNEL_LIST,Verbus=False)
            return _rst
    return False,"Tunnel Code not found"
        
def RestartTunnel(TunnelDict:dict):
    rst = CheckStatusTunnel(TunnelDict)
    if rst[0]:                
        TnlStatus1 = KillProcessByPID(pid=rst[2])
        time.sleep(2)
    TnlStatus = FnStartTunnel(TunnleDict=TunnelDict,DebugMode=False)
    return TnlStatus
    

def FnCloneTunnelbyCode(TunnelCode4Clone:str,NewTunnelCode = str):
    _TUNNEL_LIST = RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        if _t.lower().strip() == NewTunnelCode.lower().strip():
            FileTunnelName = _TUNNEL_LIST[_t]['Name']
            return False,f"Tunnel Code [ {NewTunnelCode} ] already exists for Tunnel [ {FileTunnelName} ]\n Tunnel Code must be unique."
    for _t in _TUNNEL_LIST:        
        if _t.lower().strip() == TunnelCode4Clone.lower().strip():            
            tunnel = _TUNNEL_LIST[_t]
            NewTunnel = tunnel.copy()
            NewTunnel['Code'] = NewTunnelCode
            NewTunnel['Name'] = f"{NewTunnel['Name']} (Clone)"
            NewTunnel['status'] = False
            NewTunnel['is_active'] = False            
            _TUNNEL_LIST[NewTunnelCode] = NewTunnel
            _rst = lib.BaseFunction.SaveJsonFile(JsonFile=TunnelJsonFilePath,JsonData=TUNNEL_LIST,Verbus=False)
            if _rst:
                return True,f"Tunnel [ {tunnel['Name']} ] cloned successfully to [ {NewTunnel['Name']} ] with Code [ {NewTunnelCode} ]"
            else:
                return False,"Error on save Tunnel to file."


def Fn_getTunnelStatus(TunnelDict=dict): 
    Rst = ViewTunnleStatus(TunnelDict=TunnelDict,ReturnDictResualt=True)
    MsgDict = {}
    if Rst.get("isActive",False):        
        #MsgLines.append(f"Tunnel {_tunnel.get('Name','N/A')} is running. 🚀  with PID {Rst.get('pid','N/A')}\n")        
        MsgDict["pid"] = Rst.get('pid','N/A')
    else:
        MsgDict["pid"] = ''
        #MsgLines.append(f"Tunnel {_tunnel.get('Name','N/A')} is not running. ⏹️ \n\n")
    MsgDict["Name"] = TunnelDict.get('Name','N/A')
    MsgDict["Type"] = TunnelDict.get('Type','N/A')
    MsgDict["Highly_Restricted_Networks_enalbe"] = TunnelDict.get('Highly_Restricted_Networks',{}).get('Enable',False)
    MsgDict["ssh_ip"] = TunnelDict.get('ssh_ip','N/A')
    MsgDict["ssh_user"] = TunnelDict.get('ssh_user','N/A')
    MsgDict["ssh_port"] = TunnelDict.get('ssh_port','N/A')
    MsgDict["FinalPort"] = TunnelDict.get('FinalPort','N/A')
    MsgDict["Keep_Alive"] = TunnelDict.get('Keep_Alive',False)
    MsgDict["ExitOnForwardFailure"] = TunnelDict.get('Highly_Restricted_Networks',{}).get('ExitOnForwardFailure','N/A')
    MsgDict["ServerAliveInterval"] = TunnelDict.get('Highly_Restricted_Networks',{}).get('ServerAliveInterval','N/A')
    MsgDict["ServerAliveCountMax"] = TunnelDict.get('Highly_Restricted_Networks',{}).get('ServerAliveCountMax','N/A')
    MsgDict["MonitorPort"] = TunnelDict.get('Highly_Restricted_Networks',{}).get('MonitorPort','N/A')

    if Rst.get("isActive",False):
        MsgDict["Process"] = {}
        MsgDict["Process"]["name"] = Rst.get('Process',{}).get('name','N/A')
        MsgDict["Process"]["pid"] = Rst.get('pid','N/A')
        MsgDict["Process"]["start_time"] = Rst.get('Process',{}).get('start_time','N/A')
        MsgDict["Process"]["exe"] = Rst.get('Process',{}).get('exe','N/A')
        MsgDict["Process"]["cmdline"] = Rst.get('Process',{}).get('cmdline','N/A')
        MsgDict["Process"]["status"] = Rst.get('Process',{}).get('status','N/A')
        MsgDict["Process"]["user"] = Rst.get('Process',{}).get('user','N/A')
        MsgDict["Process"]["memory-RSS"] = Rst.get('Process',{}).get('memory-RSS','N/A')
        MsgDict["Process"]["memory-VMS"] = Rst.get('Process',{}).get('memory-VMS','N/A')
        MsgDict["Process"]["cpu_percent"] = Rst.get('Process',{}).get('cpu_percent','N/A')
        MsgDict["Process"]["parent_process"] = Rst.get('Process',{}).get('parent_process','N/A')
        MsgDict["Process"]["children_process"] = Rst.get('Process',{}).get('children_process','N/A')
        MsgDict["Process"]["connections"] = Rst.get('connections',[])

        ConnectionsList = Rst.get('connections',[])        
            #MsgLines.append(f"  ▫️ {conn}\n")
        MsgDict["Process"]["connections"] = ConnectionsList
    return MsgDict


def FnSetAuthenticationMode(_TempTunnelList:dict, TunnelCode:str,Password:str='',KeyPath:str='',AuthenticationMode=''):
    """"Set the authentication mode for each tunnel - Use In API """
    if AuthenticationMode.strip() == "":
        _TempTunnelList[TunnelCode]['authentication'] = ''
        _TempTunnelList[TunnelCode]['password'] = ''
        _TempTunnelList[TunnelCode]['key_path'] = ''
    elif AuthenticationMode.lower().strip() == 'password':
        if Password is None:
            return False,f"Password cannot be empty for password authentication." 
        if Password.strip() == "":
            return False,f"Password cannot be empty for password authentication."
        _TempTunnelList[TunnelCode]['authentication'] = 'password'
        _TempTunnelList[TunnelCode]['key_path'] = ''
        _TempTunnelList[TunnelCode]['password'] = Password
    elif AuthenticationMode.lower().strip() in ['key_path','key', 'keyfile']:
        if KeyPath.strip() == "":
            return False,f"SSH Key path cannot be empty for key authentication."
        if not os.path.isfile(KeyPath):
            return False,f"SSH Key file not found at path: {KeyPath}"
        _TempTunnelList[TunnelCode]['authentication'] = 'key_path'
        _TempTunnelList[TunnelCode]['password'] = ''
        _TempTunnelList[TunnelCode]['key_path'] = KeyPath
    else:
        return False,f"Invalid Authentication Mode: {AuthenticationMode}"
    return True,"Authentication Mode set successfully.",_TempTunnelList                
    

####### Service Manegment    

signal.signal(signal.SIGINT, lib.BaseFunction.handler)
Generate_SERVICE_LIST()
######################################################
######################################################

#_debug = ['en']
#sys.argv.extend(_debug)

if __name__ == "__main__":        
    if len(sys.argv) == 1:        
        MainMenu()        
    elif len(sys.argv) == 2:        
        _errMsg = False
        if sys.argv[1] in ['-s','--start','--start-all']:
            StartAllTunnel()
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            printTunnelList()
            print('\n')
            lib.BaseFunction.FnExit()
        elif sys.argv[1] in ['-d','--drop','--drop-all']:
            DropAllSShTunnel()
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            printTunnelList()
            print('\n')
            lib.BaseFunction.FnExit()
        elif sys.argv[1] in ['-r','--restart','--reload']:
            DropAllSShTunnel()
            StartAllTunnel()
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            printTunnelList()
            print('\n')
            lib.BaseFunction.FnExit()

        elif sys.argv[1] in ['-h','--help']:            
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            FnHelp()
        else:     
            for _ in TUNNEL_LIST:
                if _["Code"].lower().strip() == sys.argv[1].lower().strip():                
                    ViewTunnleStatus(_)
                    _errMsg = True                                
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            print('\n')
            if _errMsg:                
                lib.AsciArt.BorderIt(Text=f"Tunnel Code [ {sys.argv[1]} ] not found.",BorderColor=_fr,TextColor=_fy)
            else:    
                printTunnelList()
    else:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        print(f'\n{_fw}Invalid arguments. Please use [ {_fEx_g}-h{_fw} ] or [ {_fEx_g}--help{_fw} ] for help.{_reset}\n')
        
        


