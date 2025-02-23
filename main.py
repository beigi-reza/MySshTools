#! /usr/bin/python3
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import scp
import signal
import os
import core
from core import current_directory,JsonListFile,ServerConfigFile,SERVER_LIST,SSHKEY

COLOR_LIST = ['_fw','_fy','_fb','_fbl','_fr','_fc','_fg','_fm','_fEx_w','_fEx_y','_fEx_b','_fEx_bl','_fEx_r','_fEx_c','_fEx_g','_fEx_m']

#current_directory = os.path.dirname(os.path.realpath(__file__))
#JsonListFile = os.path.join(current_directory,'conf/config.json')
#JsonConfig = lib.BaseFunction.LoadJsonFile(JsonListFile)
#ServerConfigFile = os.path.join(current_directory,'conf/ServerList.json')
#SERVER_LIST = lib.BaseFunction.LoadJsonFile(ServerConfigFile)["servers"]
#TAG_VIEW = lib.BaseFunction.GetValue(JsonConfig,"Tag_View",verbus=False,ReturnValueForNone=False)
#SSHKEY = lib.BaseFunction.GetValue(JsonConfig,"SSHKEY",verbus=False,ReturnValueForNone='')
MatthedServer = 'ALL'

_B = "[1m"
_N = "[22m"
_D = "[2m"
_reset = "[0m"
_UN = "\033[4m"
_fw = "[37m"
_fy = "[33m"
_fb = "[34m"
_fbl = "[30m"
_fr = "[31m"
_fc = "[36m"
_fg = "[32m"
_fm = "[35m"
_fEx_w = "[97m"
_fEx_y = "[93m"
_fEx_b = "[94m"
_fEx_bl = "[90m"
_fEx_r = "[91m"
_fEx_c = "[96m"
_fEx_g = "[92m"
_fEx_m = "[95m"


_bw = "[47m"
_by = "[43m"
_bb = "[44m"
_bbl = "[40m"
_br = "[41m"
_bc = "[46m"
_bg = "[42m"
_bm = "[45m"
_brst = "[49m"
_bEx_w = "[107m"
_bEx_y = "[103m"
_bEx_b = "[104m"
_bEx_bl = "[100m"
_bEx_r = "[101m"
_bEx_c = "[106m"
_bEx_g = "[102m"
_bEx_m = "[105m"



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
        ServerLst = core.printServerInfo(ServerCode)        
        print(f'\n{_N}{_fw}( {_fy}S{_fw} ) {_fy}for SSH{_reset}')
        print(f'{_N}{_fw}( {_fc}c{_fw} ) {_fc}for SCP{_reset}')
        print(f'{_N}{_fw}( {_fg}T{_fw} ) {_fg}for Tunnel{_reset}')        
        InpustStr = f"{_B}{_fw}Type [ {_fy}S{_fw} | {_fc}C{_fw} | {_fg}T{_fw} | Q ]"
        UserInput = input(f'\n{InpustStr} : {_reset}')
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
        print(f'{_N}{_fw}\nfor Quit ( {_D}ctrl + c{_N} ) or ( {_D}q{_N} ){_reset}')
        if _CopdeFoundInServerlist:            
            _code = UserInput
            UserInput = input(f'{_B}{_fw}Press {_fr}ENTER{_fw} for [ {_br}  {_code}  {_reset}{_fw} ] or Type for servers : {_reset}')
        else:
            UserInput = input(f'{_B}{_fw}Type for servers: {_reset}')
            
        if UserInput.lower().strip() == 'q':
            lib.BaseFunction.FnExit()
        else:
            if UserInput.strip() == '':
                if _CopdeFoundInServerlist:
                    return _code.lower().strip()
                else:
                    _SrvList = 'ALL'                                
            else:
                _SrvList = core.FindServers(UserInput)
                if len(_SrvList) == 0:
                    msg = f'{_fr}No server found{_reset}'
                elif len(_SrvList) == 1:
                    return _SrvList[0]                                    
        _CopdeFoundInServerlist = False

def MainMenuLuncher():
    ServerCode = MainMenu()
    UserCommand ,ServerLst = ConnectMenu(ServerCode)
    if UserCommand == 's':
        ConnectSSH(ServerLst)
    elif UserCommand == 'c':
        scp.ScpMenu(ServerLst)
    elif UserCommand == 't':
        print(f'\n{_fr}Tunnel{_reset}')
    lib.BaseFunction.PressEnterToContinue()

def ConnectSSH(ServerLst):
    Ip = ServerLst["IP"]
    Port = ServerLst["Port"]
    User = ServerLst["User"]    
    if SSHKEY != '':
        if lib.BaseFunction.isFile(SSHKEY,Title="Custom SSH KEY",Verbus=False):
            Ssh_Command = f'ssh -i {SSHKEY} -p {Port} {User}@{Ip}'
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




if __name__ == "__main__":
    if ChecCodeIUniq() is False:
        lib.BaseFunction.FnExit()
    Start()