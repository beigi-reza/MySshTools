#! /usr/bin/python3
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import os
import subprocess
import signal
from datetime import datetime, timedelta
import time
import sys
import psutil
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
        RunWithRoot()
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
                Msg = ''
                if _["Code"].lower() == UserInput.lower().strip():
                    rst = CheckStatusTunnel(_)
                    if rst[0]:
                        #DropTunnel(rst[0])
                        KillProcessByPID(rst[1])
                    else:
                        rst = FnStartTunnel(_)
                        if rst[0] is False:
                            if rst[1] == '':
                                Msg = f"Tunnel {UserInput} failed to start."
                            findCode = False
                            break
                        else:    
                            findCode = True
                            break
            if findCode == False:                
                if Msg == '':
                    Msg = f"No server found ( {UserInput} )"

def StartAllTunnel():
    for _ in TUNNEL_LIST:
        if CheckStatusTunnel(_)[0]:
            print(f"Tunnel {_['Name']} is already running.")
        else:
            FnStartTunnel(_)

def DropAllSShTunnel():
    for _ in TUNNEL_LIST:                        
        _RST = CheckStatusTunnel(_)
        if _RST[0]:
            KillProcessByPID(_RST[1])


            
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
    _rst = CheckStatusTunnel(Tunnel)
    if _rst[0]:
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


def RunWithRoot():            
    if lib.BaseFunction.User_is_root() is False:
        msg1 = """Tunnel Funcyion requires root privileges, Attempting to restart with sudo..."""
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
    try:
        process = subprocess.Popen(
            Command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,        
            stdin=subprocess.DEVNULL,
            start_new_session=True,            
            )            
        #time.sleep(1)        
        _rst = CheckStatusTunnel(TunnleDict)
        if _rst[0]:
            return True,''
        else:
            return False,''
    except Exception as e:
        msg = (f"🔥 Exception occurred while starting autossh: {e}")        
        return  False,msg
    
def FnAutoRestartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())
    while True:        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _LineLog = f"{timestamp},{TunnleDict['Name']},None,Trying to Start Tunnel"
        print (f"{_LineLog}")
        SaveLogWebsite(_LineLog)
        process = subprocess.Popen(
            Command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,        
            stdin=subprocess.DEVNULL,
            start_new_session=False,
            )            
        time.sleep(1)
        _rst = CheckStatusTunnel(TunnleDict)
        Pid = process.pid
        if _rst[0] is False:            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _LineLog = f"{timestamp},{TunnleDict['Name']},{Pid},Error: Unable to start tunnel"
            SaveLogWebsite(_LineLog)
            print (f"{_LineLog}")
            time.sleep(5)
            continue                   
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _LineLog = f"{timestamp},{TunnleDict['Name']},None,Started Tunnel"
            SaveLogWebsite(_LineLog)
            print (f"{_LineLog}")
        while True:
            retcode = process.poll()
            if retcode is not None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
                _LineLog = f"{timestamp},{TunnleDict['Name']},{Pid},Tunnel disconnected! Restarting..."
                SaveLogWebsite(_LineLog)
                print (f"{_LineLog}")        
                break
            time.sleep(5)
        print("waitt for 2 sec")    
        time.sleep(2)

def SaveLogWebsite(LogLine:str ):        
    """آماده سازی لاگ برای ذخیره با فرمت CSV
    به دست آوردن اسم فایل و بررسی وجود

    Args:
        ResponseDict (DICT): Dict of website status.
    """
    RealPath_of_LogFile = os.path.join(current_directory,'logs','KeepAlivelog.csv')    
    if os.path.isfile(RealPath_of_LogFile) is False:
        _Titel = "Time,Name,PID,Msg"
        Saveit(RealPath_of_LogFile,_Titel)        
    Saveit(RealPath_of_LogFile,LogLine)

def Saveit(FileName,Line):    
    """ثبت لاگ دپر فایل

    Args:
        FileName (STR): Realpath of log filwe
        Line (STR): Log for Save To log
    """
    Line = f"{Line}\n"
    try:
        f = open(FileName, "a")
        try:        
            f.write(Line)            
        except:
            print("Something went wrong when writing to the log file [ " + _fr + FileName + _reset + " ]")
        finally:
            f.close()
    except:
        print("Something went wrong when writing to the log file [ " + _B +  _fr + FileName + _reset + " ]")


#def CheckStatusTunnel(_Tunnle):        
#    _Highly_Restricted_Networks = _Tunnle["Highly_Restricted_Networks"].get('Enable',False)
#    ProcessDict = GetProcessList(_Tunnle)
#    if _Tunnle['Type'] == 'local':        
#        _SSHType = '-L'
#        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Local_or_Rempte_server']}:{_Tunnle['Local_or_Rempte_port']}"
#    elif _Tunnle['Type'] == 'remote':
#        _SSHType = '-R'
#        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Local_or_Rempte_server']}:{_Tunnle['Local_or_Rempte_port']}"
#    elif _Tunnle['Type'] == 'dynamic':
#        _SSHType = '-R' 
#        _SSHTypeServer = f"{_Tunnle['FinalPort']}"        
#
#    UserIP = f'{_Tunnle["ssh_user"]}@{_Tunnle["ssh_ip"]}'
#    for _process in ProcessDict:
#        if UserIP in ProcessDict[_process]:
#            if _SSHType in ProcessDict[_process]:
#                if _SSHTypeServer in ProcessDict[_process]:
#                    return True, _process
#             
#    return False,''

def CheckStatusTunnel(_Tunnle):
    Highly_Restricted_Networks_mode = _Tunnle["Highly_Restricted_Networks"].get('Enable',False)
    if _Tunnle['Type'] == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Local_or_Rempte_server']}:{_Tunnle['Local_or_Rempte_port']}"
    elif _Tunnle['Type'] == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Local_or_Rempte_server']}:{_Tunnle['Local_or_Rempte_port']}"
    elif _Tunnle['Type'] == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{_Tunnle['FinalPort']}"        
    
    if Highly_Restricted_Networks_mode:
        CommandStr = 'autossh'
    else:
        CommandStr = 'ssh'

    UserIP = f'{_Tunnle["ssh_user"]}@{_Tunnle["ssh_ip"]}'            
    try:
        # Check if the process exists
        for proc in psutil.process_iter(['cmdline', 'pid', 'name']):
            if proc.name().lower().strip() == CommandStr.lower().strip():
                if UserIP in proc.cmdline():
                    if _SSHType in proc.cmdline():
                        if _SSHTypeServer in proc.cmdline():
                            return True, proc.pid                                    
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False,''
    return False,''
    



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
    
#def WritePIDToFile(Pid, TunnelName):
#    if 'Pids' not in os.listdir(current_directory):
#        os.makedirs(os.path.join(current_directory, 'Pids'))
#    PidFile = os.path.join(current_directory, 'Pids', f'{TunnelName}.pid')
#    with open(PidFile, 'w') as f:
#        f.write(str(Pid))
#
#def GetPIDFromFile(TunnelName):
#    PidFile = os.path.join(current_directory, 'Pids', f'{TunnelName}.pid')
#    if os.path.exists(PidFile):
#        with open(PidFile, 'r') as f:
#            return int(f.read().strip())
#    else:
#        return None


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
            if connections:                                
                for conn in connections[:5]:  # Limit to first 5 connections
                    local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"                                                                                
                    connectionsList.append(f"  {conn.type} - Local: {local} Remote: {remote} ({conn.status})")
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


signal.signal(signal.SIGINT, lib.BaseFunction.handler)

######################################################
######################################################


if __name__ == "__main__":
    MainMenu()