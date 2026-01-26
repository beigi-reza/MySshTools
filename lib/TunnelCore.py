
import os
import time
import psutil
from datetime import datetime, timedelta
import subprocess
import lib.BaseFunction
from core import current_directory,LOG_PATH,SSHKEY,JsonConfigFile,JsonConfig
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

#current_directory = os.path.dirname(os.path.realpath(__file__))
#JsonListFile = os.path.join(current_directory,'conf/config.json')
#JsonConfig = lib.BaseFunction.LoadJsonFile(JsonListFile)
#LOG_PATH = os.path.join(JsonConfig.get('log_path','/var/log'),'ssh-log')

SERVICE_LIST = {}

def Generate_SERVICE_LIST():
    global SERVICE_LIST
    SERVICE_LIST = { "service-api":{},"keep-alive":{},"telegram-bot":{}}
    for _s in SERVICE_LIST:        
        if SERVICE_LIST[_s].get('name','') == '':
            SERVICE_LIST[_s]['name'] = _s        
        if SERVICE_LIST[_s].get('description','') == '':
            SERVICE_LIST[_s]['description'] = f'{_s} description'
        if SERVICE_LIST[_s].get('exec','') == '':
            SERVICE_LIST[_s]['exec'] = f'{_s}.py'
        if SERVICE_LIST[_s].get('user','') == '':
            SERVICE_LIST[_s]['user'] = 'root'
        if SERVICE_LIST[_s].get('working_dir','') == '':
            SERVICE_LIST[_s]['working_dir'] = current_directory    
    return SERVICE_LIST


def FnAutoRestartTunnel(TunnleDict):
    Command = CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower())
    while True:        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _LineLog = f"{timestamp},{TunnleDict['Name']},None,Trying to Start Tunnel"
        print (f"{_LineLog}")
        SaveLogWebsite(_LineLog)

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
        except Exception as e:
            print(f"Exception: {e}")
            msg = (f"🔥 Exception occurred while starting autossh: {e}")        
            return  False,msg

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

def CreateCommamd(TunnleDict, TypeOfTunnel,DebugMode = False):
    Highly_Restricted_Networks = TunnleDict["Highly_Restricted_Networks"].get('Enable', False)
    if Highly_Restricted_Networks: 
        _sshCommandMode = 'autossh'
    else:    
        _sshCommandMode = 'ssh'

    if TypeOfTunnel == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Source_Server']}:{TunnleDict['Source_port']}"
    elif TypeOfTunnel == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"0.0.0.0:{TunnleDict['FinalPort']}:{TunnleDict['Source_Server']}:{TunnleDict['Source_port']}"
    elif TypeOfTunnel == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{TunnleDict['FinalPort']}"        
    else:
        print(f"Unknown Tunnel Type: {TypeOfTunnel} for {TunnleDict['Name']}")
        lib.BaseFunction.PressEnterToContinue()
    
    CommandLst = []    
    CommandLst.append(_sshCommandMode)
    if DebugMode:
        CommandLst.append('-vvv')

    if Highly_Restricted_Networks:
        CommandLst.append('-M')
        CommandLst.append(str(TunnleDict["Highly_Restricted_Networks"].get('MonitorPort', 0)))
    
    CommandLst.append('-N')
    CommandLst.append(_SSHType)
    CommandLst.append(_SSHTypeServer)
    CommandLst.append('-p')
    CommandLst.append(str(TunnleDict.get('ssh_port', '22')))
    
    # Authentication: check for key or password
    auth_method = TunnleDict.get('authentication', 'key')  # default to key authentication
    
    if auth_method.lower().strip() == 'key':
        ssh_key = TunnleDict.get('ssh_key', SSHKEY)  # use provided key or default SSHKEY        
        CommandLst.append('-i')
        CommandLst.append(ssh_key)
    elif auth_method.lower().strip() == 'key_path':
        CommandLst.append('-i')
        CommandLst.append(TunnleDict.get('key_path',''))
    elif auth_method.lower().strip() == 'password':
        # For password authentication, we need to use sshpass
        # Insert sshpass at the beginning of the command
        ssh_password = TunnleDict.get('password', '')
        if ssh_password:
            #ssh_password = f'\'{ssh_password}\''  # Ensure password is properly quoted 
            CommandLst.insert(0, ssh_password)
            CommandLst.insert(0, '-p')
            CommandLst.insert(0, 'sshpass')
    
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveInterval={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveInterval', 0)}")
    CommandLst.append('-o')
    CommandLst.append(f"ServerAliveCountMax={TunnleDict['Highly_Restricted_Networks'].get('ServerAliveCountMax', 0)}")
    CommandLst.append('-o')
    CommandLst.append(f"ExitOnForwardFailure={TunnleDict['Highly_Restricted_Networks'].get('ExitOnForwardFailure', 'no')}")
    CommandLst.append('-o')
    CommandLst.append("StrictHostKeyChecking=no")
    CommandLst.append('-o')
    CommandLst.append("UserKnownHostsFile=/dev/null")
    CommandLst.append(f"{TunnleDict['ssh_user']}@{TunnleDict['ssh_ip']}")
    
    return CommandLst


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

def CheckStatusTunnel(_Tunnle):

    Highly_Restricted_Networks_mode = _Tunnle["Highly_Restricted_Networks"].get('Enable',False)
    if _Tunnle['Type'] == 'local':        
        _SSHType = '-L'
        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Source_Server']}:{_Tunnle['Source_port']}"
    elif _Tunnle['Type'] == 'remote':
        _SSHType = '-R'
        _SSHTypeServer = f"0.0.0.0:{_Tunnle['FinalPort']}:{_Tunnle['Source_Server']}:{_Tunnle['Source_port']}"
    elif _Tunnle['Type'] == 'dynamic':
        _SSHType = '-R' 
        _SSHTypeServer = f"{_Tunnle['FinalPort']}"        
    
    if Highly_Restricted_Networks_mode:
        CommandStr = 'autossh'
    else:
        CommandStr = 'ssh'

    UserIP = f'{_Tunnle["ssh_user"]}@{_Tunnle["ssh_ip"]}'            
    TunnelIsEnable = _Tunnle.get('isActive',True)    
    try:
        # Check if the process exists
        if TunnelIsEnable: # Only check for Tunneles that are enabled
            for proc in psutil.process_iter(['cmdline', 'pid', 'name']):
                if proc.name().lower().strip() == CommandStr.lower().strip():                                
                    CmdLine = proc.info['cmdline']
                    if CmdLine is not None:
                        if UserIP in CmdLine:
                            if _SSHType in CmdLine:
                                if _SSHTypeServer in CmdLine:
                                    return True, '',proc.pid                                        
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):        
        return False,'error',-1
    except Exception as e:
        msg = (f"🔥 {e}")        
        return False,msg,-1
    return False,'',-1



if __name__ == "__main__":    
    print(f"You should not run this file directly")
