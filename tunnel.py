#! /usr/bin/python3
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import os
import subprocess
import signal
from core import (
    current_directory,
    JsonListFile,
    ServerConfigFile,
    SERVER_LIST,
    SSHKEY,
    TUNNEL_LIST,
    RunAsSudo,
    HIGHLY_RESTRICTED_NETWORKS
)

if HIGHLY_RESTRICTED_NETWORKS == {}:
    HighlyRestrictedNetworksEnable = False
    ExitOnForwardFailure = ''
    ServerAliveInterval = 0
    ServerAliveCountMax = 0
    MonitorPort = 0
else:
    HighlyRestrictedNetworksEnable = lib.BaseFunction.GetValue(HIGHLY_RESTRICTED_NETWORKS,'Enable',verbus=False,ReturnValueForNone=False)
    if HighlyRestrictedNetworksEnable:        
        ExitOnForwardFailure = HIGHLY_RESTRICTED_NETWORKS.get('ExitOnForwardFailure','yes')
        ServerAliveInterval = HIGHLY_RESTRICTED_NETWORKS.get('ServerAliveInterval',60)
        ServerAliveCountMax = HIGHLY_RESTRICTED_NETWORKS.get('ServerAliveCountMax',3)
        MonitorPort = HIGHLY_RESTRICTED_NETWORKS.get('MonitorPort',0)
    else:
        ExitOnForwardFailure = ''
        ServerAliveInterval = 0
        ServerAliveCountMax = 0        
    

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


######################################################
######################################################



    

def MainMenu(Msg = ''):
    while True:        
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()
        PrintConfig()
        printTunnelList()                
        if Msg != '':
            print("")
            print("")
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fy,TextColor=_fEx_r)
            Msg = ''
        print(f'\n\n{_fw}( {_fg}s{_fw} ) Start all Tunnel{_reset}')
        print(f'{_fw}( {_fr}d {_fw}) Drop all Tunnel{_reset}')
        print(f'{_fw}( {_fr}r {_fw}) Restart all Tunnel{_reset}')
        print(f'{_fw}( {_fy}c {_fw}) Chek Tunnel{_reset}')
        print(f'{_fw}( {_fy}t {_fw}) Test Connection{_reset}')
        print(f'\n{_D}q for quit{_reset}')
        UserInput = input(f'{_B}{_fw}Or Enter tunnel name :  {_reset}')        
        if UserInput.strip().lower() in ['q','s','d','r','c','t']:
            return UserInput.lower().strip()
        else:
            for _ in TUNNEL_LIST:
                if _["Code"].lower() == UserInput.lower().strip():
                    return UserInput.lower().strip()
                elif _["Name"].lower() == UserInput.lower().strip():
                    return UserInput.lower().strip()
                else:
                    if UserInput != '':
                        Msg = f"No server found ( {UserInput} )"
        

def MainMenuLuncher():
        UserInput = MainMenu()
        if UserInput == 'q':
            lib.BaseFunction.FnExit()
        elif UserInput == 's':
            print("Start All")
        elif UserInput == 'd':
            print("Drop All")
        elif UserInput == 'r':
            print("Restart All")
        elif UserInput == 'c':
            print("Check Tunnel")
        elif UserInput == 't':
            print("Test Connection")
        else:
            for _ in TUNNEL_LIST:
                if _["Code"].strip().lower() == UserInput.lower().strip():
                    FnStartTunnel(_)
        
        

def printTunnelList():
    TitleStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Name', target_length=15, AlignmentMode='center')}{_reset}"
    TypeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Type', target_length=10, AlignmentMode='center')}{_reset}"
    SourceStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Source', target_length=18, AlignmentMode='center')}{_reset}"
    SSHServerStr = f"{_bb}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='SSH Server', target_length=30, AlignmentMode='center')}{_reset}"
    FinalPortStr = f"{_by}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Final Port', target_length=20, AlignmentMode='center')}{_reset}"
    CodeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Code', target_length=8, AlignmentMode='center')}{_reset}"
    print(f"\n{CodeStr} {TitleStr} {TypeStr} {SourceStr} {SSHServerStr} {FinalPortStr}\n")
    for _ in TUNNEL_LIST:
        a = GenerateTunnelLine(_)
        print(a)


def GenerateTunnelLine(Tunnel):
    _LServer = lib.BaseFunction.GetValue(Tunnel, "Local_or_Rempte_server")
    _LPort = lib.BaseFunction.GetValue(Tunnel, "Local_or_Rempte_port")
    _sshPort = lib.BaseFunction.GetValue(Tunnel, "ssh_port")
    _sshIp = lib.BaseFunction.GetValue(Tunnel, "ssh_ip")
    _sshUser = lib.BaseFunction.GetValue(Tunnel, "ssh_user")
    _Type = lib.BaseFunction.GetValue(Tunnel, "Type").upper()
    if _Type == "LOCAL":
        _tColor = _fb
        _FinalIP = 'Localhost'
    elif _Type == "REMOTE":
        _tColor = _fc
        _FinalIP = f'{Tunnel["ssh_ip"]}'
    elif _Type == "DYNAMIC":
        _tColor = _fm
        _FinalIP = 'Localhost'
    else:
        _tColor = _fw
        _FinalIP = ' - '
        
    if CheckStatusTunnel(Tunnel['Name']):
        _Icon = '▶️'        
        _FinalPort = f'{_Icon}  {_FinalIP}:{Tunnel["FinalPort"]}'
        _clPort = f'{_bg}{_fbl}'        
    else:
        _Icon = '⏸️'        
        _FinalPort = f'{_Icon}  {Tunnel["FinalPort"]}'
        _clPort = f'{_fw}'
    _Title = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=Tunnel['Name'], target_length=15, AlignmentMode='left')}{_reset}"
    _SourceOrRemote = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_LServer}:{_LPort}', target_length=18, AlignmentMode='left')}{_reset}"
    _SshServer = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_sshUser}@{_sshIp}:{_sshPort}', target_length=30, AlignmentMode='left')}{_reset}"
    _FinalPort = f"{_clPort}{lib.AsciArt.FnAlignmentStr(originalString=_FinalPort , target_length=20, AlignmentMode='left')}{_reset}"
    _type = f"{_tColor}{lib.AsciArt.FnAlignmentStr(_Type, target_length=10, AlignmentMode='left')}{_reset}"
    _code = f"{_fy}{lib.AsciArt.FnAlignmentStr(originalString=Tunnel['Code'], target_length=8, AlignmentMode='left')}{_reset}"
    return f"{_code} {_Title} {_type} {_SourceOrRemote} {_SshServer} {_FinalPort}"


def PrintConfig():    
    RootAccessStr = f'{_fw}\nCreate tunnel with root Privilage : {_bg}{_fbl} {RunAsSudo} {_reset}'
    Highly_Restricted_Networks_Str = f'{_fw}Highly Restricted Networks Mode is Enable :{_by}{_fbl} {HighlyRestrictedNetworksEnable} {_reset}'
    ExitOnForwardFailureStr = f'{_fw}Force Exit if port forwarding fails for any reason : {_by}{_fbl} {ExitOnForwardFailure.upper()} {_reset}'
    ServerAliveIntervalStr = f'{_fw}Send keep-alive messages every : {_by}{_fbl}  {ServerAliveInterval}  {_reset}'
    ServerAliveCountMaxStr = f'{_fw}How many keep-alive messages the client sends before considering the connection dead :  {_by}{_fbl}  {ServerAliveCountMax}  {_reset}'    
    print (RootAccessStr)
    print (Highly_Restricted_Networks_Str)
    if HighlyRestrictedNetworksEnable:
        AutoSShCommadStatus = CheckAutoSSHCommand()
        if AutoSShCommadStatus is None:
            lib.AsciArt.BorderIt(Text='Unspecified error in autossh detection',BorderColor=_fr,TextColor=_fw)
            lib.BaseFunction.FnExit()            
        if AutoSShCommadStatus:
            print(ExitOnForwardFailureStr)
            print(ServerAliveIntervalStr)
            print(ServerAliveCountMaxStr)
        elif AutoSShCommadStatus is False:            
            msg1 = """`Autossh` is required.
To run in `Highly Restricted Networks Mode`, you need the `autossh` program. First, install the version relevant to your operating system and run this program again.
            """
            lib.AsciArt.BorderIt(Text=msg1,BorderColor=_fr,TextColor=_fw,WidthBorder=100)
            lib.BaseFunction.FnExit()

            
def CreateCommamd(TunnleDict,TypeOfTunnel):    
    if HighlyRestrictedNetworksEnable:
        _sshCommandMode = 'autossh'        
    else:    
        _sshCommandMode = 'ssh'

    if TypeOfTunnel == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"{TunnleDict['Local_or_Rempte_port']}:localhost:{TunnleDict['FinalPort']}"
    elif TypeOfTunnel == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"{TunnleDict['FinalPort']}:localhost:{TunnleDict['Local_or_Rempte_port']}"
    elif TypeOfTunnel == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{TunnleDict['FinalPort']}"        
    

    CommandLst = []    
    if RunAsSudo:
        CommandLst.append('sudo')
    CommandLst.append(_sshCommandMode)
    CommandLst.append('-M')
    CommandLst.append(str(MonitorPort))
    CommandLst.append('-N')
    CommandLst.append(_SSHType)
    CommandLst.append(_SSHTypeServer)
    CommandLst.append('-p')
    CommandLst.append(str(TunnleDict.get('ssh_port','22')))
    CommandLst.append('-i')
    CommandLst.append(SSHKEY)
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveInterval={ServerAliveInterval}")
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveCountMax={ServerAliveCountMax}")
    CommandLst.append('-o')
    CommandLst.append(f"ExitOnForwardFailure={ExitOnForwardFailure}")
    CommandLst.append(f"{TunnleDict['ssh_user']}@{TunnleDict['ssh_ip']}")


#    CommandLst = [
#    _sshCommandMode,
#    "-M",str(MonitorPort),
#    "-N",
#    f"{_SSHType}",f"{_SSHTypeServer}",
#    "-p",f"{str(TunnleDict.get('ssh_port','22'))}",
#    "-i",f"{SSHKEY}",
#    "-o",f"ServerAliveInterval={ServerAliveInterval}",
#    "-o",f"ServerAliveCountMax={ServerAliveCountMax}",
#    "-o",f"ExitOnForwardFailure={ExitOnForwardFailure}",
#    f"{TunnleDict['ssh_user']}@{TunnleDict['ssh_ip']}"
#    ]
    return CommandLst


def FnStartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())
    print(Command)
    process = subprocess.Popen(Command)
    retcode = process.poll()
    Pid = process.pid
    WritePIDToFile(Pid, TunnleDict['Name'])
    print(f"Tunnel PID : {Pid}")

def CheckStatusTunnel(TunnelName):    
    return False
    
    
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
    
def WritePIDToFile(Pid, TunnelName):
    if os.path.join(current_directory, 'Pids') not in os.listdir(current_directory):
        os.makedirs(os.path.join(current_directory, 'Pids'))
    PidFile = os.path.join(current_directory, 'Pids', f'{TunnelName}.pid')
    with open(PidFile, 'w') as f:
        f.write(str(Pid))

signal.signal(signal.SIGINT, lib.BaseFunction.handler)

######################################################
######################################################


if __name__ == "__main__":
    MainMenuLuncher()