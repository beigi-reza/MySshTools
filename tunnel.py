#! /usr/bin/python3
from click import Command
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import os
import subprocess
import signal
import time
from core import (
    current_directory,
    JsonListFile,
    ServerConfigFile,
    SERVER_LIST,
    SSHKEY,
)

TunnelDict = os.path.join(current_directory,'conf/tunnel.json')
TUNNEL_Json = lib.BaseFunction.LoadJsonFile(JsonFile=TunnelDict,Verbus=False,ReternValueForFileNotFound={})

TUNNEL_LIST = TUNNEL_Json["tunnel"]

#if HIGHLY_RESTRICTED_NETWORKS == {}:
#    HighlyRestrictedNetworksEnable = False
#    ExitOnForwardFailure = ''
#    ServerAliveInterval = 0
#    ServerAliveCountMax = 0
#    MonitorPort = 0
#else:
#    HighlyRestrictedNetworksEnable = lib.BaseFunction.GetValue(HIGHLY_RESTRICTED_NETWORKS,'Enable',verbus=False,ReturnValueForNone=False)
#    if HighlyRestrictedNetworksEnable:        
#        ExitOnForwardFailure = HIGHLY_RESTRICTED_NETWORKS.get('ExitOnForwardFailure','yes')
#        ServerAliveInterval = HIGHLY_RESTRICTED_NETWORKS.get('ServerAliveInterval',60)
#        ServerAliveCountMax = HIGHLY_RESTRICTED_NETWORKS.get('ServerAliveCountMax',3)
#        MonitorPort = HIGHLY_RESTRICTED_NETWORKS.get('MonitorPort',0)
#    else:
#        ExitOnForwardFailure = 'no'
#        ServerAliveInterval = 0
#        ServerAliveCountMax = 0        
#        MonitorPort = 0    

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
        if UserInput.strip().lower() in ['q','s','d','r','']:
            if UserInput == 'q':
                lib.BaseFunction.FnExit()
            elif UserInput == 's':
                StartAllTunnel()
            elif UserInput == 'd':
                DropAllSShTunnel()
            elif UserInput == 'r':
                DropAllSShTunnel()
                StartAllTunnel()
            elif UserInput.strip() == '':
                continue
        else:
            for _ in TUNNEL_LIST:                
                findCode = False
                if _["Code"].lower() == UserInput.lower().strip():
                    if CheckStatusTunnel(_):
                        DropTunnel(_)
                    else:    
                        FnStartTunnel(_)
                    findCode = True
                    break
                elif _["Name"].lower() == UserInput.lower().strip():
                    if CheckStatusTunnel(_):
                        DropTunnel(_)
                    else:    
                        FnStartTunnel(_)
                    findCode = True
                    break
            if findCode == False:
                Msg = f"No server found ( {UserInput} )"

def DropAllSShTunnel():
    for _ in TUNNEL_LIST:
        IP = _["ssh_ip"]
        pids = os.popen("ps ax | grep " + IP + " | grep -v grep")
        try:
            for line  in pids:
                fields = line.split()
                pid = fields[0]                       
                os.kill(int(pid), signal.SIGKILL)                       
        except:
            pass                 
def StartAllTunnel():
    for _ in TUNNEL_LIST:
        if CheckStatusTunnel(_):
            print(f"Tunnel {_['Name']} is already running.")
        else:
            FnStartTunnel(_)
            
def DropTunnel(TunnleDict):    
    Pid = GetPIDFromFile(TunnleDict['Name'])    
    if Pid is not None:
        if KillProcessByPID(Pid) is False:
            print(f"Failed to stop proccess {TunnleDict['Name']} ({Pid})")
            lib.BaseFunction.PressEnterToContinue()

def KillProcessByPID(pid,Verbus=False):
    try:        
        pid = int(pid)        
        os.kill(pid, signal.SIGTERM)  # SIGTERM is a graceful termination signal        
        return True
    except ProcessLookupError:
        if Verbus:
            print(f"No process with PID {pid} was found.")
        return False
    except ValueError:
        if Verbus:
            print(f"Invalid PID: {pid}")
        return False
    except PermissionError:
        if Verbus:
            print(f"Permission denied when trying to kill process {pid}.")
        return False
    except Exception as e:
        if Verbus:
            print(f"Error killing process {pid}: {e}")
        return False


def printTunnelList():
    TitleStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Name (code)', target_length=20, AlignmentMode='center')}{_reset}"
    TypeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Type', target_length=10, AlignmentMode='center')}{_reset}"
    SourceStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Source', target_length=18, AlignmentMode='center')}{_reset}"
    SSHServerStr = f"{_bb}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='SSH Server', target_length=30, AlignmentMode='center')}{_reset}"
    FinalPortStr = f"{_by}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Final Port', target_length=30, AlignmentMode='center')}{_reset}"
    ModeStr = f"{_bw}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Mode', target_length=6, AlignmentMode='center')}{_reset}"
    print(f"\n{ModeStr} {TitleStr} {TypeStr} {SourceStr} {SSHServerStr} {FinalPortStr}\n")
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
        
    if CheckStatusTunnel(Tunnel):
        _Icon = '▶️'        
        _FinalPort = f'{_Icon}  {_FinalIP}:{Tunnel["FinalPort"]}'
        _clPort = f'{_bg}{_fbl}'        
    else:
        _Icon = '⏸️'        
        _FinalPort = f'{_Icon}  {Tunnel["FinalPort"]}'
        _clPort = f'{_fw}'
    if Tunnel["Highly_Restricted_Networks"].get('Enable',False):
        ModeChr = ' ✨'
    else:
        ModeChr = ' 🔗'
    #FullName = f"{Tunnel['Name']} ({_fy}{Tunnel['Code']}{_fw})"
    FullName = f"{Tunnel['Name']} ({Tunnel['Code']})"
    _Title = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=FullName, target_length=20, AlignmentMode='left')}{_reset}"
    _SourceOrRemote = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_LServer}:{_LPort}', target_length=18, AlignmentMode='left')}{_reset}"
    _SshServer = f"{_fw}{lib.AsciArt.FnAlignmentStr(originalString=f'{_sshUser}@{_sshIp}:{_sshPort}', target_length=30, AlignmentMode='left')}{_reset}"
    _FinalPort = f"{_clPort}{lib.AsciArt.FnAlignmentStr(originalString=_FinalPort , target_length=30, AlignmentMode='left')}{_reset}"
    _type = f"{_tColor}{lib.AsciArt.FnAlignmentStr(_Type, target_length=10, AlignmentMode='left')}{_reset}"
    _Mode = f"{_fy}{lib.AsciArt.FnAlignmentStr(ModeChr, target_length=6, AlignmentMode='left')}{_reset}"
    return f"{_Mode} {_Title} {_type} {_SourceOrRemote} {_SshServer} {_FinalPort}"


def PrintConfig():            
    if lib.BaseFunction.User_is_root() is False:
        msg1 = """Root Access Required for Use Tunnel."""
        print('\n\n')
        lib.AsciArt.BorderIt(Text=msg1,BorderColor=_fr,TextColor=_fy,WidthBorder=100)
        print('\n\n')
        lib.BaseFunction.FnExit()

            
def CreateCommamd(TunnleDict,TypeOfTunnel):    
    Highly_Restricted_Networks = TunnleDict["Highly_Restricted_Networks"].get('Enable',False)
    if Highly_Restricted_Networks: 
        _sshCommandMode = 'autossh'        
    else:    
        _sshCommandMode = 'ssh'

    if TypeOfTunnel == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Local_or_Rempte_server']}:{TunnleDict['Local_or_Rempte_port']}"
    elif TypeOfTunnel == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Local_or_Rempte_server']}:{TunnleDict['Local_or_Rempte_port']}"
    elif TypeOfTunnel == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{TunnleDict['FinalPort']}"        
    else:
        print(f"Unknown Tunnel Type: {TypeOfTunnel} for {TunnleDict['Name']}")
        lib.BaseFunction.PressEnterToContinue()
    

    CommandLst = []    
    CommandLst.append(_sshCommandMode)
    if Highly_Restricted_Networks:
        CommandLst.append('-M')
        CommandLst.append(str(TunnleDict["Highly_Restricted_Networks"].get('MonitorPort',0)))
    CommandLst.append('-N')
    CommandLst.append(_SSHType)
    CommandLst.append(_SSHTypeServer)
    CommandLst.append('-p')
    CommandLst.append(str(TunnleDict.get('ssh_port','22')))
    CommandLst.append('-i')
    CommandLst.append(SSHKEY)
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveInterval={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveInterval',0)}")
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveCountMax={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveCountMax',0)}")
    CommandLst.append('-o')
    CommandLst.append(f"ExitOnForwardFailure={TunnleDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure','no')}")
    CommandLst.append(f"{TunnleDict['ssh_user']}@{TunnleDict['ssh_ip']}")
    return CommandLst


def FnStartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())
    print(Command)
    process = subprocess.Popen(
        Command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True               
        )
    retcode = process.poll()
    Pid = process.pid
    WritePIDToFile(Pid, TunnleDict['Name'])
    print(f"\n\n\nTunnel {TunnleDict['Name']} started with PID: {Pid}")    
    return Pid

def FnAutorestartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())
    while True:
        process = subprocess.Popen(
            Command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True
        )
        Pid = process.pid
        WritePIDToFile(Pid, TunnleDict['Name'])
        while True:
            retcode = process.poll()
            if retcode is not None:
                print(f"autossh tunnel disconnected! Restarting... {TunnleDict['Name']}")
                break
            time.sleep(5)
        print(f"Check ... {TunnleDict['Name']}")
        time.sleep(2)


def CheckStatusTunnel(TunnleDict):    
    Pid = GetPIDFromFile(TunnleDict['Name'])    
    if Pid is not None:
        pidDetail = os.popen("ps ax | grep " + str(Pid) + " | grep -v grep")
        if pidDetail.read() == "":
            return False
        else:
            return True
    else:
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
    if 'Pids' not in os.listdir(current_directory):
        os.makedirs(os.path.join(current_directory, 'Pids'))
    PidFile = os.path.join(current_directory, 'Pids', f'{TunnelName}.pid')
    with open(PidFile, 'w') as f:
        f.write(str(Pid))

def GetPIDFromFile(TunnelName):
    PidFile = os.path.join(current_directory, 'Pids', f'{TunnelName}.pid')
    if os.path.exists(PidFile):
        with open(PidFile, 'r') as f:
            return int(f.read().strip())
    else:
        return None


signal.signal(signal.SIGINT, lib.BaseFunction.handler)

######################################################
######################################################


if __name__ == "__main__":
    MainMenu()