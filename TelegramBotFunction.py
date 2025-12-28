import os
import copy
from tunnel import TUNNEL_LIST,RefreshTunnelList,ViewTunnleStatus
import tunnel as TunnelManagment
import lib.BaseFunction
import lib.AsciArt
import random
current_directory = os.path.dirname(os.path.realpath(__file__))
TelegramJsonFile = os.path.join(current_directory,"conf/Telegram.json")
TelegramJsonConfig = lib.BaseFunction.LoadJsonFile(TelegramJsonFile,Verbus=True)


def CreateTunnlListwithStatus():
    global TUNNEL_LIST_WITH_STATUS
    TUNNEL_LIST = RefreshTunnelList()
    TUNNEL_LIST_WITH_STATUS = TUNNEL_LIST.copy()

    for _t in TUNNEL_LIST_WITH_STATUS:        
        Tunnel = TUNNEL_LIST_WITH_STATUS[_t]
        _rst = TunnelManagment.CheckStatusTunnel(Tunnel)
        TUNNEL_LIST_WITH_STATUS[_t]['status'] = _rst[0]
        TUNNEL_LIST_WITH_STATUS[_t]['pid'] = _rst[1]
    return TUNNEL_LIST_WITH_STATUS

def GenerateTunnelStatusSummary(TunnelCode='',UserData={}):
    _edited = " ✏️ (Edited)"
    _added = " ➕ (Added)"
    _removed = " ➖ (Removed)"        
    IgnoreFields = ["Keep_Alive",
                    "is_active",
                    "Highly_Restricted_Networks.Enable",
                    "Highly_Restricted_Networks.ExitOnForwardFailure",
                    "Highly_Restricted_Networks.ServerAliveInterval,"
                    "Highly_Restricted_Networks.ServerAliveCountMax"
                    "Highly_Restricted_Networks.MonitorPort",]
    TunnelDict= ""
    TunnelDict = copy.deepcopy(UserData['tunnel_list'][TunnelCode])
    #TunnelDict = UserData['tunnel_list'][TunnelCode]
    TunnelChangesDict =  compare_dicts(dict1=TUNNEL_LIST,dict2=UserData['tunnel_list'])    
    SummaryLines = []

    if TunnelCode in TunnelChangesDict:
        TunnelDiff = TunnelChangesDict[TunnelCode]
        # Changed Fields
        for field in TunnelDiff['changed']:
            if field in IgnoreFields:
                continue
            TunnelDict[field] = TunnelDict[field] + _edited            
        # Added Fields
        for field in TunnelDiff['added']:
            if field in IgnoreFields:
                continue
            for _key in TunnelDict:
                if _key == field:
                    TunnelDict[field] = TunnelDict[field] + _added            
        # Removed Fields
        for field in TunnelDiff['removed']:
            if field in IgnoreFields:
                continue            
            TunnelDict[field] = TunnelDict.get(field,'') + _removed            



##  Find Tunnel Mode
    Mode = TunnelDict.get('Type','')
    if Mode != '':
        Modesplit = Mode.split(' ')
        if len(Modesplit) > 1:
            _Type = Modesplit[0].upper()
        else:
            _Type = Mode.upper()
    else:
        _Type = ''

    
    if _Type == "LOCAL":
        _Type = f' 🏠 Local'
        _FinalIP = lib.BaseFunction.GetLocalIP()                        
    elif _Type == "REMOTE":
        _Type = f' 🌐 Remote'
        _FinalIP = f'{TunnelDict["ssh_ip"]}'
    elif _Type == "DYNAMIC":
        _Type = f' 🔀 Dynamic'
        _FinalIP = f'{TunnelDict["ssh_ip"]}'
    else:
        _Type = f' Not Valied'
        _FinalIP = 'N/A'

    _LServer = TunnelDict.get('Source_Server','')
    _LPort = TunnelDict.get('Source_port','N/A')
    _FinalPort = TunnelDict.get('FinalPort','N/A')

    if TunnelDict.get('status',None) is None:
        _statusStr = "⁉️ Status: Unknown ⁉️"
        _FinalStr = f'N/A'
    elif TunnelDict.get('status',False) is True:
        _statusStr = f"Status: ▶️ Running ( PID {TunnelDict.get('pid','N/A')})"
        _FinalStr = f'Final Adress: {_FinalIP}:{_FinalPort}'
    else:   
        _statusStr = "Status: ⏹️ Stopped"
        _FinalStr = f'Final Port: {_FinalPort}'

    if TunnelDict["Highly_Restricted_Networks"].get('Enable',False):
        _Mode = f'✨ Highly Restricted Networks'
    else:
        _Mode = f'🔗 Standard'
    
    if TunnelDict.get('Keep_Alive',False):
        _keppAlive = f'🔒 Active (in service mode)'
    else: 
        _keppAlive = f'🔓 Disabled'


    ##  Find Authentication Mode
    authentication = TunnelDict.get('authentication','')
    if authentication != '':
        authenticationSpit = authentication.split(' ')
        if len(authenticationSpit) > 1:
            authentication_vlaue = authenticationSpit[0]
        else:
            authentication_vlaue = authentication
    else:
        authentication_vlaue = ''
        

    if authentication_vlaue in ['',None]:
        _AuthStr = '🔐 Defualt Authentication'
    elif authentication_vlaue == 'password': 
        _AuthStr = '🔑 Password Authentication'
    elif authentication_vlaue == 'key_path':
        _AuthStr = '🗝️ Key-Based Authentication'    
    else:
        _AuthStr = '❓ Unknown Authentication Mode ❓ / 🔐 Using Defualt Authentication'

    _ssh_ip = TunnelDict['ssh_ip']    
    _ssh_port = TunnelDict['ssh_port']
    _ssh_user = TunnelDict['ssh_user']
    _TunnelName = TunnelDict.get('Name','N/A')
    # Create Msg List    
    SummaryLines.append(f"\n🔰 Tunnel Name: {_TunnelName} 🔰\n\n")
    SummaryLines.append(f"⚙️ Type: {_Type}\n")
    SummaryLines.append(f'⚙️ {_statusStr}\n\n')
    SummaryLines.append(f'🔒 Auth: {_AuthStr}\n\n')
    SummaryLines.append(f"⚙️ Mode: {_Mode}\n")
    SummaryLines.append(f"💡 Keep Alive: {_keppAlive}\n")
    SummaryLines.append(f"🖥️ Server Details: \n")
    SummaryLines.append(f"    📍 {_ssh_ip}\n")
    SummaryLines.append(f"    👤 {_ssh_user}\n")
    SummaryLines.append(f"    🔌 {_ssh_port}\n\n")
    SummaryLines.append(f"↗️ Source : {_LServer}:{_LPort}\n\n")
    SummaryLines.append(f"🏁 {_FinalStr}\n")
    return ''.join(SummaryLines)


##def old_GenerateTunnelStatusSummary(TunnelCode = '',UserData={}):    
##    msg = GenerateTunnelStatusSummary(TunnelCode=TunnelCode,UserData=UserData)
##    MsgList = []
##    #TUNNEL_LIST_WITH_STATUS = CreateTunnlListwithStatus()    
##     # for Detect User Change Fields    
##    _UserDataTunnel = {}
##    for _t in TUNNEL_LIST_WITH_STATUS:        
##        _tunnel = TUNNEL_LIST_WITH_STATUS[_t]
##        if _tunnel.get('Code','') == TunnelCode:            
##            _UserDataTunnel = UserData.get("tunnel_list",{}).get(TunnelCode,{})            
##            # Check for Name Change
##            if _UserDataTunnel["Name"] != _tunnel.get('Name',''):
##                TunnelName = _UserDataTunnel["Name"] + "(Edited) ✏️"
##            else:
##                TunnelName = _tunnel.get('Name','N/A')
##
##
##
##
##            if _UserDataTunnel.get('Type') != _tunnel.get('Type',''):            
##                _Type  = _UserDataTunnel.get('Type').upper()
##                EditedTypeStr = f' (Edited) ✏️'
##            else:
##                _Type = _tunnel.get('Type','N/A').upper()
##                EditedTypeStr = ''
##
##            if _UserDataTunnel.get('Source_Server','') != _tunnel.get('Source_Server',''):
##                _LServer = _UserDataTunnel.get('Source_Server','') + ' (Edited) ✏️'
##            else:
##                _LServer = _tunnel.get('Source_Server','N/A')
##            if _UserDataTunnel.get('Source_port','') != _tunnel.get('Source_port',''):
##                _LPort = str(_UserDataTunnel.get('Source_port','')) + ' (Edited) ✏️'
##            else:
##                _LPort = _tunnel.get('Source_port','N/A')
##
##            if _UserDataTunnel.get('FinalPort') != _tunnel.get('FinalPort',''):                            
##                _FinalPort = _UserDataTunnel.get('FinalPort','N/A') + ' (Edited) ✏️'
##            else:
##                _FinalPort = _tunnel.get('FinalPort','N/A')
##            
##            if _Type == "LOCAL":
##                _Type = f' 🏠 LOCAL' + EditedTypeStr
##                _FinalIP = lib.BaseFunction.GetLocalIP()                        
##            elif _Type == "REMOTE":
##                _Type = f' 🌐 LOCAL' + EditedTypeStr
##                _FinalIP = f'{_tunnel["ssh_ip"]}'
##            elif _Type == "DYNAMIC":
##                _Type = f' 🔀 DYNAMIC' + EditedTypeStr
##                _FinalIP = f'{_tunnel["ssh_ip"]}'
##            else:                
##                _FinalIP = ' - '
##            if _tunnel.get('status',None) is None:
##                statusStr = "⁉️ Status: Unknown ⁉️"
##                _FinalStr = f'N/A'
##            elif _tunnel.get('status',False) is True:
##                statusStr = f"Status: ▶️ Running ( PID {_tunnel.get('pid','Unknown')})"
##                _FinalStr = f'Final Adress: {_FinalIP}:{_FinalPort}'
##            else:   
##                statusStr = "Status: ⏹️ Stopped"
##                _FinalStr = f'Final Port: {_FinalPort}'
##
##            if _tunnel["Highly_Restricted_Networks"].get('Enable',False):
##                ModeChr = f'Highly Restricted Networks is ✨Enabled✨'
##            else:
##                ModeChr = f'Highly Restricted Networks is disabled'
##
##            if _tunnel.get('Keep_Alive',False):
##                _keppAlive = f'🔒 Active (in service mode)'
##            else: 
##                _keppAlive = f'🔓 Disabled'
##
##
##            if _UserDataTunnel.get('authentication','') != _tunnel.get('authentication',''):
##                authentication = _UserDataTunnel.get('authentication','')
##                if authentication in ['',None]:
##                    _AuthStr = '🔐 Defualt Authentication' + ' (Edited) ✏️'
##                elif authentication == 'password': 
##                    _AuthStr = '🔑 Password Authentication' + ' (Edited) ✏️'
##                elif authentication == 'key_path':
##                    _AuthStr = '🗝️ Key-Based Authentication' + ' (Edited) ✏️'        
##            else:
##                _AuthStr = '🔐 Defualt Authentication'
##
##            authentication = _UserDataTunnel.get('authentication','')
##            
##            if _UserDataTunnel.get('ssh_ip','') != _tunnel.get('ssh_ip',''):
##                _tunnel['ssh_ip'] = _UserDataTunnel.get('ssh_ip','') + ' (Edited) ✏️'
##            if _UserDataTunnel.get('ssh_port','') != _tunnel.get('ssh_port',''):
##                _tunnel['ssh_port'] = str(_UserDataTunnel.get('ssh_port','')) + ' (Edited) ✏️'
##            if _UserDataTunnel.get('ssh_user','') != _tunnel.get('ssh_user',''):
##                _tunnel['ssh_user'] = _UserDataTunnel.get('ssh_user','') + ' (Edited) ✏️'
##
##
##            # Create Msg List
##            MsgList.append(f"\n🔰 Tunnel Name: {TunnelName} 🔰\n\n")
##            MsgList.append(f'⚙️ {TunnelName} ( {statusStr} )\n')
##            MsgList.append(f"🔄 Tunnel Type: {_Type}\n\n")
##            MsgList.append(f'🔒 Auth Mode: {_AuthStr}\n')
##            MsgList.append(f"⚙️ Mode: {ModeChr}\n")
##            MsgList.append(f"💡 Keep Alive: {_keppAlive}\n\n")
##            MsgList.append(f"🖥️ Server Details: \n")
##            MsgList.append(f"    📍 {_tunnel.get('ssh_ip','N/A')}\n")
##            MsgList.append(f"    👤 {_tunnel.get('ssh_user','N/A')}\n")
##            MsgList.append(f"    🔌 {_tunnel.get('ssh_port','N/A')}\n\n")
##            MsgList.append(f"↗️ Source : {_LServer}:{_LPort}\n\n")
##            MsgList.append(f"🏁 {_FinalStr}\n")
##            break
##    return ''.join(MsgList)


def GetTunnelStatusByCode(TunnelCode=''):
    TUNNEL_LIST_WITH_STATUS = CreateTunnlListwithStatus()
    for _t in TUNNEL_LIST_WITH_STATUS:
        if _t == TunnelCode:
            _tunnel = TUNNEL_LIST_WITH_STATUS[_t]
            return _tunnel
    return None
            
def StartTunnelByCode(TunnelCode='',DEBUG=False):
    TUNNEL_LIST = RefreshTunnelList()
    for _t in TUNNEL_LIST:
        _tunnel = TUNNEL_LIST[_t]
        TunnelCodeInList = _tunnel.get('Code','')
        if TunnelCodeInList.strip().lower() == TunnelCode.strip().lower():
            TnlStatus = TunnelManagment.FnStartTunnel(TunnleDict=_tunnel,DebugMode=DEBUG)
            break
    if TnlStatus[0]:
        return True, f"✅ Tunnel '{_tunnel.get('Name','Unknown')}' started successfully."
    else:
        return False, f"❌ Failed to start tunnel '{_tunnel.get('Name','Unknown')}': {TnlStatus[1]}"
            
def StopTunnelByCode(TunnelCode=''):
    TUNNEL_LIST = RefreshTunnelList()
    for _t in TUNNEL_LIST:
        _tunnel = TUNNEL_LIST[_t]
        TunnelCodeInList = _tunnel.get('Code','')
        if TunnelCodeInList.strip().lower() == TunnelCode.strip().lower():
            StatusTunnel = TunnelManagment.CheckStatusTunnel(_tunnel)
            rst = TunnelManagment.KillProcessByPID(StatusTunnel[1])
            break
    if rst[0]:
        return True, f"✅ Tunnel '{_tunnel.get('Name','Unknown')}' Stop successfully."
    else:
        return False, f"❌ Failed to Stop tunnel '{_tunnel.get('Name','Unknown')}': {rst[1]}"
    



def DeleteTunnelByCode(TunnelCode='',UserData={}):
    global TUNNEL_LIST
    NewTunellList = {}
    for _ in TUNNEL_LIST:        
        _tunnel = TUNNEL_LIST[_]
        TunnelCodeInList = _tunnel.get('Code','')
        if TunnelCodeInList.strip().lower() == TunnelCode.strip().lower():
            # First, stop the tunnel if it's running
            StatusTunnel = TunnelManagment.CheckStatusTunnel(_tunnel)
            if StatusTunnel[0]:
                TunnelManagment.KillProcessByPID(StatusTunnel[1])
            # Then, remove the tunnel from the list
            rst = TunnelManagment.DeleteTunnel(TunnelDict=_tunnel,NoWait=True)            
            for _user_tunnel in UserData.get('tunnel_list',{}):
                if UserData['tunnel_list'][_user_tunnel].get('Code','') == TunnelCodeInList:
                    del UserData['tunnel_list'][_user_tunnel]
                    break
            continue
        else:
            NewTunellList[_] = _tunnel
    if rst:
        TUNNEL_LIST = NewTunellList        
        return True, f"🗑️ Tunnel '{_tunnel.get('Name','Unknown')}' \n Deleted successfully. 🗑️"
    else:
        return False, f"❌ Failed to Delete tunnel '{_tunnel.get('Name','Unknown')}."


def GetTelegramStickerID(StikerName= None):
    Stikers = TelegramJsonConfig.get('stickers','')
    StikerIds = Stikers.get(StikerName,'')
    if StikerIds == '':
        return None
    elif len(StikerIds) == 1:
        return StikerIds[0]
    elif type(StikerIds) is list:
        randomIndex = random.randint(0,len(StikerIds)-1)
        return StikerIds[randomIndex]




def SaveUserTunnelChange(UserDataTunnels = {}):    
    ConfigFile = os.path.join(current_directory,"conf/tunnel.json")
    ## Save Changes to Tunnel.json
    _rst = lib.BaseFunction.SaveJsonFile(ConfigFile,UserDataTunnels,Verbus=False)
    if _rst[0]:
        # Refresh Tunnel List
        RefreshTunnelList()
        return True, "✅ Changes applied successfully."        
    else:
        return False, f"❌ Failed to apply changes: {_rst[1]}"


def compare_dicts(dict1, dict2, ignore_fields=None):
    """
    Compare two dictionaries and return the differences.
    
    Args:
        dict1: First dictionary (original)
        dict2: Second dictionary (new)
        ignore_fields: List of field paths to ignore (e.g., ['status', 'pid', 'sq.ssh_ip'])
    
    Returns:
        Dictionary with changes, additions, and removals for each top-level key
    """
    if ignore_fields is None:
       ignore_fields  = ["status", "pid"]

#    if ignore_fields is None:
#        ignore_fields = []
    
    # Convert ignore list to set for faster lookup
    #ignore_set = set(ignore_fields)
    
    def should_ignore(path):
        """Check if a field path should be ignored"""
        PathSplit = path.split('.')
        if len(PathSplit) <= 1:
            return False
        if PathSplit[1].lower() in ignore_fields:
            return True
        return False
    
    def compare_nested(obj1, obj2, path=""):
        """Recursively compare nested structures"""
        changed = []
        added = []
        removed = []
        
        # Handle None values
        if obj1 is None and obj2 is None:
            return changed, added, removed
        
        if obj1 is None:
            if not should_ignore(path):
                added.append(path)
            return changed, added, removed
        
        if obj2 is None:
            if not should_ignore(path):
                removed.append(path)
            return changed, added, removed
        
        # If both are dictionaries, compare recursively
        if isinstance(obj1, dict) and isinstance(obj2, dict):
            all_keys = set(obj1.keys()) | set(obj2.keys())
            
            for key in all_keys:
                new_path = f"{path}.{key}" if path else key
                
                if should_ignore(new_path):
                    continue
                
                if key not in obj2:
                    removed.append(new_path)
                elif key not in obj1:
                    added.append(new_path)
                else:
                    c, a, r = compare_nested(obj1[key], obj2[key], new_path)
                    changed.extend(c)
                    added.extend(a)
                    removed.extend(r)
        
        # If values are different (and not both dicts)
        elif obj1 != obj2:
            if not should_ignore(path):
                changed.append(path)
        
        return changed, added, removed
    
    result = {}
    
    # Get all top-level keys from both dictionaries
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    for key in all_keys:
        # Check if entire key should be ignored
        if should_ignore(key):
            continue
        
        obj1 = dict1.get(key)
        obj2 = dict2.get(key)
        
        if obj1 is None and obj2 is not None:
            # Key was added
            result[key] = {
                "changed": [],
                "added": [key],
                "removed": []
            }
        elif obj2 is None and obj1 is not None:
            # Key was removed
            result[key] = {
                "changed": [],
                "added": [],
                "removed": [key]
            }
        else:
            # Compare the nested structures
            changed, added, removed = compare_nested(obj1, obj2, key)
            
            # Remove the key prefix from paths since we're already in that key's context
            changed = [p.replace(f"{key}.", "", 1) for p in changed]
            added = [p.replace(f"{key}.", "", 1) for p in added]
            removed = [p.replace(f"{key}.", "", 1) for p in removed]
            
            # Only add to result if there are actual differences
            if changed or added or removed:
                result[key] = {
                    "changed": changed,
                    "added": added,
                    "removed": removed
                }
    
    return result

def GenerateDiffReport(DiffResult={}):
    ReportLines = []
    for tunnel_key in DiffResult:
        tunnel_diff = DiffResult[tunnel_key]
        ReportLines.append(f"\n🔰 Changes in Tunnel: {tunnel_key} 🔰\n")
        
        if tunnel_diff['changed']:
            ReportLines.append("✏️ Changed Fields:\n")
            for field in tunnel_diff['changed']:
                ReportLines.append(f"   - {field}\n")
        
        if tunnel_diff['added']:
            ReportLines.append("➕ Added Fields:\n")
            for field in tunnel_diff['added']:
                ReportLines.append(f"   - {field}\n")
        
        if tunnel_diff['removed']:
            ReportLines.append("➖ Removed Fields:\n")
            for field in tunnel_diff['removed']:
                ReportLines.append(f"   - {field}\n")
    return ''.join(ReportLines)

def getTunnelLogs(TunnelCode=''):
    _tunnel = None
    for _t in TUNNEL_LIST:
        if TUNNEL_LIST[_t].get('Code','') == TunnelCode:
            _tunnel = TUNNEL_LIST[_t]
            break   
    if _tunnel is None:
        return False, f"❌ Tunnel with code '{TunnelCode}' not found."    
    Rst = ViewTunnleStatus(TunnelDict=_tunnel,ReturnDictResualt=True)
    MsgLines = []
    if Rst.get("isActive",False):        
        MsgLines.append(f"Tunnel {_tunnel.get('Name','N/A')} is running. 🚀  with PID {Rst.get('pid','N/A')}\n")        
    else:
        MsgLines.append(f"Tunnel {_tunnel.get('Name','N/A')} is not running. ⏹️ \n\n")
    
    MsgLines.append(f"Tunnel Name : {_tunnel.get('Name','N/A')}\n\n")
    MsgLines.append(f"Type : {_tunnel.get('Type','N/A')}\n\n")
    MsgLines.append(f"Highly restricted network mode : {'Enabled' if _tunnel.get('Highly_Restricted_Networks',{}).get('Enable',False) else 'Disabled'}\n\n")
    MsgLines.append(f"IP : {_tunnel.get('ssh_ip','N/A')}\n")
    MsgLines.append(f"User : {_tunnel.get('ssh_user','N/A')}\n")
    MsgLines.append(f"Port : {_tunnel.get('ssh_port','N/A')}\n")
    MsgLines.append(f"Final Port : {_tunnel.get('FinalPort','N/A')}\n\n")    
    MsgLines.append("📄 Advanced Options :\n")
    MsgLines.append(f"  ▫️ Keep Alive : {'Enabled' if _tunnel.get('Keep_Alive',False) else 'Disabled'}\n")
    MsgLines.append(f"  ▫️ Exit On Forward Failure : {_tunnel.get('Highly_Restricted_Networks',{}).get('ExitOnForwardFailure','N/A')}\n")
    MsgLines.append(f"  ▫️ Server Alive Interval : {_tunnel.get('Highly_Restricted_Networks',{}).get('ServerAliveInterval','N/A')}\n")
    MsgLines.append(f"  ▫️ Server Alive Count Max : {_tunnel.get('Highly_Restricted_Networks',{}).get('ServerAliveCountMax','N/A')}\n")
    MsgLines.append(f"  ▫️ Monitor Port : {_tunnel.get('Highly_Restricted_Networks',{}).get('MonitorPort','N/A')} Use Only for Highly Restricted Network Mode\n")
    if Rst.get("isActive",False):
        MsgLines.append(f"⚙️ Process Details :\n")        
        MsgLines.append(f"  ▫️ Process name : {Rst.get('Process',{}).get('name','N/A')}\n")
        MsgLines.append(f"  ▫️ Process PID : {Rst.get('pid','N/A')}\n")
        MsgLines.append(f"  ▫️ start time : {Rst.get('Process',{}).get('start_time','N/A')}\n")
        MsgLines.append(f"  ▫️ Execute path : {Rst.get('Process',{}).get('exe','N/A')}\n")
        MsgLines.append(f"  ▫️ CMD : {Rst.get('Process',{}).get('cmdline','N/A')}\n")
        MsgLines.append(f"  ▫️ Stayus : {Rst.get('Process',{}).get('status','N/A')}\n")
        MsgLines.append(f"  ▫️ User : {Rst.get('Process',{}).get('user','N/A')}\n\n")        
        MsgLines.append(f"⚙️ Memory Info :\n")         
        MsgLines.append(f"  ▫️ Memort-RSS (Resident) : {Rst.get('Process',{}).get('memory-RSS','N/A')}\n")
        MsgLines.append(f"  ▫️ Memory-VMS (Virtual Memory) : {Rst.get('Process',{}).get('memory-VMS','N/A')}\n")
        MsgLines.append(f"⚙️ CPU Info :\n")         
        cpu_persent = Rst.get('Process',{}).get('cpu_percent','N/A')
        BarsGraph = lib.AsciArt.GenerateBarGraph(length=10,UsedPercent=cpu_persent,UseEmoji=True)
        MsgLines.append(f"  ▫️ CPU Usage : {BarsGraph}({cpu_persent})%\n")
        MsgLines.append(f"  ▫️ Parent Process : {Rst.get('Process',{}).get('parent_process','N/A')}\n\n")
        MsgLines.append(f"  ▫️ Children Process : {Rst.get('Process',{}).get('children_process','N/A')}\n\n")                
        MsgLines.append(f"⚙️ Network Connections :\n")
        ConnectionsList = Rst.get('connections',[])
        for conn in ConnectionsList:
            MsgLines.append(f"  ▫️ {conn}\n")
    return Rst.get("isActive",False), ''.join(MsgLines)    

def TunnelIsValidForActive(TunnelDict={}):
    NeedToReviewList = []
    NeedToReviewList.append(f"🙁 This tunnel cannot be activated due to the following missing or invalid fields:\n")
    if TunnelDict.get('ssh_ip','').strip() == '':
        NeedToReviewList.append('📍 SSH IP is empty\n')

    sshport = TunnelDict.get('ssh_port',None)
    if sshport not in [None,'']:
        try:
            sshport_int = int(sshport)
            if not (1 <= sshport_int <= 65535):
                NeedToReviewList.append('🔌 SSH Port is out of valid range (1-65535)\n')
        except ValueError:
            NeedToReviewList.append('🔌 SSH Port is not a valid number\n')    

    if TunnelDict.get('Type','').strip().lower() not in ['local','remote','dynamic']:        
        NeedToReviewList.append('⚙️ Tunnel Type is invalid\n')
    if TunnelDict.get('Source_Server','').strip() == '':
        NeedToReviewList.append('Source Server is empty\n')
    SourcePort = TunnelDict.get('Source_port',None)
    if SourcePort not in [None,'']:
        try:
            SourcePort_int = int(SourcePort)
            if not (1 <= SourcePort_int <= 65535):
                NeedToReviewList.append('Source Port is out of valid range (1-65535)\n')
        except ValueError:
            NeedToReviewList.append('Source Port is not a valid number\n')
    FinalPort = TunnelDict.get('FinalPort',None)
    if FinalPort not in [None,'']:
        try:
            FinalPort_int = int(FinalPort)
            if not (1 <= FinalPort_int <= 65535):
                NeedToReviewList.append('Final Port is out of valid range (1-65535)\n')
        except ValueError:
            NeedToReviewList.append('Final Port is not a valid number\n')
    
    
    if len(NeedToReviewList) > 1:
        return False, "\n".join(NeedToReviewList)
    else:
        return True, []
    
def GetTunnelCommand(TunnelCode = ''):
    TunnleDict = TUNNEL_LIST[TunnelCode]
    TunnleName = TunnleDict['Name']
    CommandLIST = TunnelManagment.CreateCommamd(TunnleDict=TunnleDict,TypeOfTunnel=TunnleDict["Type"].lower(),DebugMode=False)
    FullCommandLine = ''
    MsgLine = []
    for _ in CommandLIST:
        FullCommandLine += f' {_}'
        MsgLine.append(f"{_}")
    
    FullCommandLine = FullCommandLine.strip()    
    CommandSpilit = '\n'.join(MsgLine)
    finallyMasseage = f"Command Line for Tunnel {TunnleName}\n\n🐧 Full Commnd:\n\n{FullCommandLine}\n\n⌨️ Details:\n\n{CommandSpilit}"
    return finallyMasseage

    

    


    
    


if __name__ == "__main__":           
    print(f"You should not run this file directly")
    
