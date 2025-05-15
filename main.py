#! /usr/bin/python3
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import lib.TunnelWizard
import tunnel
import scp
import signal
import os
import core
import sys
import tunnel
import json
from tunnel import TunnelJsonFilePath,TUNNEL_Json,TUNNEL_LIST
from core import current_directory,JsonListFile,ServerConfigFile,SERVER_LIST,SSHKEY
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset
MatthedServer = 'ALL'

###################################################################
###################################################################

def Start():
    while True:
        global MatthedServer
        MatthedServer = MainMenuLuncher()    

def ConnectMenu(ServerCode):
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()        
        ServerLst = core.printServerInfo(ServerCode=ServerCode,PrintIt=False)
        lib.Logo.ArtText(Text=ServerLst['ServerName'],color=f'{_fEx_y}',Font='cybermedium')
        core.printServerInfo(ServerCode)        
        print(f'\n{_N}{_fw}( {_fy}S{_fw} ) {_fy}for SSH{_reset}')
        print(f'{_N}{_fw}( {_fc}c{_fw} ) {_fc}for SCP{_reset}')
        print(f'{_N}{_fw}( {_fg}T{_fw} ) {_fg}for Tunnel{_reset}')        
        #InpustStr = f"{_B}{_fw}Type [ {_fy}S{_fw} | {_fc}C{_fw} | {_fg}T{_fw} | Q ]"
        InpustStr = f"{_B}{_fw}Type [ {_fy}S{_fw} / {_fc}C{_fw} / {_fg}T{_fw} / Q ]"
        UserInput = input(f'\n{InpustStr} > {_reset}')
        if UserInput == '':
            UserInput = 's'
        if UserInput.lower().strip() in ['s','c','t','q']:
            return UserInput.lower().strip(),ServerLst
        else:
            print(f'\n{_fr}Invalid Command{_reset}')
            lib.BaseFunction.PressEnterToContinue()            


def MainMenu(msg=''):
    _SrvList = None
    UserInput = ''
    _CopdeFoundInServerlist = False
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()        
        if msg != '':
            print(f"\n{msg}")        
            msg = ''        
        if _SrvList not in [None]:
            if len(_SrvList) > 0:
                core.PrintServerList(_SrvList)
                if UserInput != '':
                    if UserInput.strip() in _SrvList:
                            _CopdeFoundInServerlist = True                           
        print(f'{_D}\nQuit ( {_N}ctrl + c{_D} ) or ( {_N}q{_D} ){_reset}')
        if _CopdeFoundInServerlist:            
            _code = UserInput
            UserInput = input(f'{_B}{_fw}Press {_fr}ENTER{_fw} for [ {_br}  {_code}  {_reset}{_fw} ] or Type for servers > {_reset}')
        else:
            UserInput = input(f'{_B}{_fw}Type for servers > {_reset}')
            
        if UserInput.lower().strip() == 'q':
            lib.BaseFunction.FnExit()
        else:
            if UserInput.strip() == '':
                if _CopdeFoundInServerlist:
                    return _code.lower().strip()
                else:
                    _SrvList = 'ALL'
            else:                
                try:
                    InputNumber = int(UserInput)
                    if InputNumber < len(_SrvList):
                        if len(_SrvList) < 10:
                            _x = 1 
                            for _ in _SrvList:
                                if _x == InputNumber:
                                    return _SrvList[_x-1]
                                _x = _x+1                                
                except:
                    pass
                _SrvList = core.FindServers(UserInput)
                if len(_SrvList) == 0:
                    msg = f'{_fr}No server found{_reset}'
                elif len(_SrvList) == 1:
                    return _SrvList[0]                                    
        _CopdeFoundInServerlist = False

def SearchCodeInParameterMode(UserInput):
    _SrvList = None
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()        
        _SrvList = core.FindServers(UserInput)
        if len(_SrvList) == 0:
            return None
        elif len(_SrvList) == 1:
            return _SrvList[0]
        else:
            core.PrintServerList(_SrvList)            
            
            if UserInput.strip() in _SrvList:
                _code = UserInput
                print(f'{_N}{_fw}\nfor Quit ( {_D}ctrl + c{_N} ) or ( {_D}q{_N} ){_reset}')
                UserInput = input(f'{_B}{_fw}Press {_fr}ENTER{_fw} for [ {_br}  {_code}  {_reset}{_fw} ] or Type for servers : {_reset}')                        
                if UserInput.lower().strip() == 'q':
                    lib.BaseFunction.FnExit()
                else:
                    if UserInput.strip() == '':
                        return _code.lower().strip()
            else:
                print(f'{_N}{_fw}\nfor Quit ( {_D}ctrl + c{_N} ) or ( {_D}q{_N} ){_reset}')
                UserInput = input(f'{_B}{_fw}Type for servers: {_reset}')
                try:
                    InputNumber = int(UserInput)
                    if InputNumber < len(_SrvList):
                        if len(_SrvList) < 10:
                            _x = 1 
                            for _ in _SrvList:
                                if _x == InputNumber:
                                    return _SrvList[_x-1]
                                _x = _x+1                                
                except:
                    pass


def MainMenuLuncher(UserParameter = ''):
    if UserParameter == '':
        ServerCode = MainMenu()
    else:
        ServerCode = SearchCodeInParameterMode(UserParameter)
        if ServerCode == None:
            lib.AsciArt.BorderIt(Text=f'No server were found to match your search',BorderColor=_fr,TextColor=_fw)
            lib.BaseFunction.FnExit()
    UserCommand ,ServerLst = ConnectMenu(ServerCode)
    if UserCommand == 's':
        ConnectSSH(ServerLst)
    elif UserCommand == 'c':
        scp.ScpMenu(ServerLst)
    elif UserCommand == 't':
        #print(f'\n{_fr}Tunnel{_reset}')
        #if tunnel.RunAsRoot() is False:
        #tunnel.MainMenu()
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()
        #tunnel.printTunnelListHorizontal()        
        lib.TunnelWizard.TunnelHelp()
        TunnelType = lib.TunnelWizard.CreateNewTunnelMenu()
        StartSshTunnel(TunnelType,ServerLst)
        
        ## Renove This Line
        lib.BaseFunction.PressEnterToContinue()            



def StartSshTunnel(TunnelType,ServerDict):
    lib.BaseFunction.clearScreen()
    lib.Logo.SshTunnelLogo()        
    lib.TunnelWizard.tunnleProgress(Mode = TunnelType,ServerDict=ServerDict,GetValue='source_address')
    
    SourceAddress = lib.TunnelWizard.getSourceAddress()

    if TunnelType != 'dynamic':
        lib.BaseFunction.clearScreen()
        lib.Logo.SshTunnelLogo()        
        lib.TunnelWizard.tunnleProgress(Mode = TunnelType,ServerDict=ServerDict,GetValue='final_port')
        Finalport = lib.TunnelWizard.GetFinalport()
    else:
        Finalport = 'N/A'
    
    lib.BaseFunction.clearScreen()
    lib.Logo.SshTunnelLogo()        
    lib.TunnelWizard.tunnleProgress(Mode = TunnelType,ServerDict=ServerDict,GetValue='confirm')
    Createtunnel = lib.TunnelWizard.CreatetunnelConfirm()    
    ip,port = SourceAddress.split(':')
    if Createtunnel[0] == True:
        _tunnel = {
            "Name": "",
            "Code": "",
            "ssh_ip" : ServerDict['IP'],
            "ssh_user" : ServerDict['User'],
            "ssh_port" : ServerDict['Port'],
            "FinalPort": Finalport,
            "Source_Server": ip,
            "Source_port": port,
            "Type" : TunnelType,
            "Keep_Alive": False,
            "Highly_Restricted_Networks":{
                "Enable" : False,
                "ExitOnForwardFailure" :"no",
                "ServerAliveInterval":1,
                "ServerAliveCountMax":3,
                "MonitorPort": 0
            }                
        }
        if Createtunnel[1] == 'save':
            SaveTunnel(_tunnel)
            tunnel.ViewTunnleStatus(_tunnel)
        elif Createtunnel[1] == 'run':  
            tunnel.ViewTunnleStatus(_tunnel,OnNewSession=False)




def SaveTunnel(TunnelDict,msg = ''):
        TUNNEL_LIST.append(TunnelDict)
        TunnelJson = {
            "tunnel" : TUNNEL_LIST
        }
        TunnelCode = ''
        TunnelName = ''
        while True:
            lib.BaseFunction.clearScreen()
            lib.Logo.SshTunnelLogo() 

            if msg != '':
                print(f"\n{_N}{_fr} {msg}{_reset}")
                msg = ''
            if {TunnelDict['Type'] == 'local'}:
                LocalOrRemoteServerlable = "Local Server"
            else:
                LocalOrRemoteServerlable = "Remote Server"    

            print(f"\nName : {_B}{_fy}{TunnelCode}{_reset}")
            print(f"Code : {_B}{_fy}{TunnelName}{_reset}")
            print(f"Type : {_B}{_fc}{TunnelDict['Type']}{_reset}")
            print(f"IP : {_fc}{TunnelDict['ssh_ip']}{_reset}")
            print(f"User : {_fc}{TunnelDict['ssh_user']}{_reset}")
            print(f"Port : {_fc}{TunnelDict['ssh_port']}{_reset}")
            print(f"Final Port on {LocalOrRemoteServerlable} : {_B}{_fc}{TunnelDict['FinalPort']}{_reset}")
            print (f"Advanced Options :")
            print (f"  - Monitor Port : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('MonitorPort',0)}{_reset} Use Only for Highly Restricted Network Mode")
            print (f"  - ServerAliveInterval : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ServerAliveInterval',0)}{_reset}")
            print (f"  - ServerAliveCountMax : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ServerAliveCountMax',0)}{_reset}")
            print (f"  - ExitOnForwardFailure : {_fc}{TunnelDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure','no')}{_reset}")        
            
            if TunnelCode == '':                
                TunnelCode = input(f' \n{_B}{_fw}Enter Code for Tunnel > {_reset}')
                if TunnelCode.strip() == '':
                    continue
                for _ in TUNNEL_LIST:
                    if _['Code'].lower().strip() == TunnelCode.strip().lower():
                            msg = 'Tunnel Code Already Exist'                        
                            TunnelCode = ''
                            break
                if msg != '':
                    tunnelCode = ''
                continue    
            if TunnelName == '':                
                TunnelName = input(f'{_B}{_fw}\nEnter Name for Tunnel > {_reset}')                
                continue
            else:
                TunnelDict['Code'] = TunnelCode
                TunnelDict['Name'] = TunnelName
                try:
                    with open(TunnelJsonFilePath, 'w') as json_file:
                        json.dump(TunnelJson, json_file, indent=4)
                        print(f"{_B}{_fw}\nTunnel [ {_fEx_g}{TunnelName}{_fw} ] Saved Successfully{_reset}")
                        lib.BaseFunction.PressEnterToContinue()
                        return True
                except:
                    print(f"{_fr}Error on Update [ {TunnelJsonFilePath} ] operation Faild{_reset}\n")
                    lib.BaseFunction.PressEnterToContinue()
                    return False    


def ConnectSSH(ServerLst):
    Ip = ServerLst["IP"]
    Port = ServerLst["Port"]
    User = ServerLst["User"]    
    if SSHKEY != '':
        if lib.BaseFunction.isFile(SSHKEY,Title="Custom SSH KEY",Verbus=False):
            Ssh_Command = f'ssh -i {SSHKEY} -p {Port} {User}@{Ip}'
        else:
            Ssh_Command = f'ssh -p {Port} {User}@{Ip}'        
    else:
            Ssh_Command = f'ssh -p {Port} {User}@{Ip}'    
                
    print(f'\n{_fw}Connecting to {_fy}{ServerLst["ServerName"]}{_reset}')        
    os.system(Ssh_Command)
    lib.BaseFunction.FnExit()
    
def ChecCodeIUniq():
    _DuplicateSet = set()
    for _Server in SERVER_LIST:
        _name = _Server["ServerName"]
        _code = _Server["Code"]
        _ip = _Server["IP"]
        for _Server4Search in SERVER_LIST:
            _Code4Search = _Server4Search["Code"]
            _Name4Search = _Server4Search["ServerName"]
            if _Code4Search.lower().strip() == _code.lower().strip():
                if _Server["IP"] == _Server4Search["IP"]:
                    continue
                else:                    
                    _DuplicateSet.add(_name)
                    _DuplicateSet.add(_Name4Search)
    if len(_DuplicateSet) == 0:
        return True
    else:
        print(f"\n{_B}{_fr}Doplicate Code Found {_fw}{_DuplicateSet}{_reset}")
        return False
    
        

###################################################################
###################################################################

signal.signal(signal.SIGINT, lib.BaseFunction.handler)

#_debug = ['zzz']
#sys.argv.extend(_debug)



if __name__ == "__main__":
    if ChecCodeIUniq() is False:
        lib.BaseFunction.FnExit()    
    if len(sys.argv) == 1:        
        Start()
    else:
        MainMenuLuncher(sys.argv[1])