import lib.BaseFunction
import lib.AsciArt
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset
import lib.Logo
import os
import json

from core import ServerConfigFile,SERVER_LIST,GetServerDictbyCode
SourceAddress = ''
DestinationPort = ''


def CreateNewTunnelMenu():
    while True:        
        msg = f'{_B}{_fw}\n Create New Tunnel [ Local / Remote / Dynamic ]{_reset}'
        userInput = input(f'{msg} {_N}{_fy} [ L / R / D ] {_N}{_fw} > {_N}')
        if userInput.lower().strip() in ['l','local']:
            return 'local'
        elif userInput.lower().strip() in ['r','remote']:
            return 'remote'
        elif userInput.lower().strip() in ['d','dynamic']:
            return 'dynamic'


def tunnleProgress(ServerDict = None ,Mode = 'local',GetValue = None):
    NC = f'{_bw}{_fbl}'
    SelecteingColor = f'{_by}{_fbl}'    
    SelecttedColor = f'{_bg}{_fbl}'
    DC = f'{_B}{_fw}'
    S_Clr = NC
    D_clr = NC

    if GetValue == 'source_address':        
        S_Clr = SelecteingColor
    elif GetValue == 'final_port':                
        S_Clr = SelecttedColor
        D_clr = SelecteingColor
    elif GetValue == 'confirm':
        S_Clr = SelecttedColor
        D_clr = SelecttedColor

    if SourceAddress == '':
        SourceStr = f'Source Address'
    else:
        SourceStr = SourceAddress

    if DestinationPort == '':
        _DestStr = f'Final Port'        
    else:
        _DestStr = DestinationPort
    



    SShServeraddr = f'{ServerDict["user"]}@{ServerDict["ip"]}:{ServerDict["port"]}'
    S_SrvStr = f"{lib.AsciArt.FnAlignmentStr(originalString = f'🔌 {SourceStr}',target_length=20)}"
    SShAdr = f"{lib.AsciArt.FnAlignmentStr(originalString = f'🔑  {SShServeraddr}',target_length=30)}"
    FinalPortTitle = f"{lib.AsciArt.FnAlignmentStr(originalString = f'🏁 {_DestStr}',target_length=12)}"
    ThisPc = f"{lib.AsciArt.FnAlignmentStr(originalString = '💻 This computer',target_length=18)}"
    
    FirewallStr = f'🔥 Firewall'
    R_Aro = f'➡'        
        

    LineUp = '┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'
    LineDown = '└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘'

    
    if Mode == 'local':        
        TitleStr = f' {S_Clr}{S_SrvStr}{_reset} {R_Aro} {DC}{SShAdr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset}: {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'remote':
        TitleStr = f' {DC}{ThisPc}{_reset}{R_Aro} {S_Clr}{S_SrvStr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{SShAdr}{_reset} : {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'dynamic':    
        TitleStr = f' {S_Clr}{S_SrvStr}{_reset} {R_Aro} {DC}{SShAdr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset}'        
    print(f'{_fy}{LineUp}{_reset}')
    if Mode == 'dynamic':
        _sp = ' ' * 19
    else:
        _sp = ' ' * 3    
    print(f'{_fy}│ {_reset}{TitleStr}{_sp}{_fy}│{_reset}')    
    print(f'{_fy}{LineDown}{_reset}')

def TunnelHelp(Color = _fy):
    print('\n')
    TunnelHelpMode(Mode = 'local',ColorBox = Color)
    TunnelHelpMode(Mode = 'remote',ColorBox = Color)
    TunnelHelpMode(Mode = 'dynamic',ColorBox = Color)
    print('')

def TunnelHelpMode(Mode = 'local',ColorBox = _fy):

    FirewallStr = f'🔥 Firewall'
    R_Aro = f'➡'        
    SourceStr = f'🔌 Source Address '
    SShServr = f'🔑 SSH Server'
    FinalPortTitle = f'🏁 Final Port'
    ThisPc = f'🖥️  This Server '
    DC = f'{_B}{_fw}'
    S_Clr = f'{_B}{_fw}'
    D_clr = f'{_B}{_fw}'


    if Mode == 'local':        
        TitleStr = f' {S_Clr}{SourceStr}{_reset}{R_Aro} {DC}{SShServr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset} {R_Aro} {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'remote':
        TitleStr = f' {DC}{ThisPc}{_reset}{R_Aro} {S_Clr}{SourceStr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{SShServr}{_reset} {R_Aro} {D_clr}{FinalPortTitle} {_reset}'
    elif Mode == 'dynamic':    
        TitleStr = f' {S_Clr}{SourceStr}{_reset} {R_Aro} {DC}{SShServr}{_reset} {R_Aro} {DC}{FirewallStr}{_reset} {R_Aro} {DC}{ThisPc}{_reset}'        

    LineUp = '┌─────────────────────────────────────────────────────────────────────────────────────┐'
    LineDown = '└─────────────────────────────────────────────────────────────────────────────────────┘'

    ModeTitle = lib.AsciArt.FnAlignmentStr(originalString = f'{Mode.upper()} >', target_length = 13)
    if Mode == 'dynamic':
        _sp = ' ' * 17
    else:
        _sp = ' '
    print(f'{" "*13}{ColorBox}{LineUp}{_reset}')
    print(f'{ColorBox}{ModeTitle}│ {_reset}{TitleStr}{ColorBox}{_sp}│{_reset}')    
    print(f'{" "*13}{ColorBox}{LineDown}{_reset}')


def getSourceAddress(msg = ''):
    global SourceAddress
    SourceAddress = ''
    while True:
        if msg != '':
            print(f'\n{_N}{_fw} {msg}{_reset}')
            msg = ''

        UserInput = input(f'{_B}{_fw}\nEnter 🔌  {_fy}Source Address{_fw} [ {_fy}IP:Port{_fw} / {_fy}Port{_fw} ] > {_reset}')
        if UserInput.strip() == '':
            continue
        else:
            if ':' in UserInput:
                ip,port = UserInput.split(':')
                if lib.BaseFunction.FnIsValidIP(ip) or ip.lower().strip() == 'localhost':
                    if port.isdigit() and len(port) < 6 and len(port) > 0 and int(port) > 0 and int(port) < 65535:
                        SourceAddress = UserInput.strip()
                        return SourceAddress
                else:
                    msg = f'{_fr}Invalid IP or Port{_reset}'
            else:
                try:
                    if int(UserInput.strip()) > 0 and int(UserInput.strip()) < 65535:
                        SourceAddress = f'localhost:{UserInput.strip()}'                        
                        return SourceAddress
                    else:
                        msg = f'{_fr}Invalid Port{_reset}'    
                except:                        
                    msg = f'{_fr}Invalid IP or Port{_reset}'
                

def GetFinalport(msg = ''):
    global DestinationPort
    DestinationPort = ''
    while True:
        if msg != '':
            print(f'\n{_N}{_fw} {msg}{_reset}')
            msg = ''
        UserInput = input(f'{_B}{_fw}\nEnter 🏁 {_fy}Final Port{_fw} [ {_fy}Port{_fw} ] > {_reset}')
        if UserInput.strip() == '':
            continue
        else:
            try:
                if int(UserInput.strip()) > 0 and int(UserInput.strip()) < 65535:
                    DestinationPort = UserInput.strip()
                    return DestinationPort
                else:
                    msg = f'{_fr}Invalid Port{_reset}'
            except:                        
                msg = f'{_fr}Invalid Port{_reset}'


def CreatetunnelConfirm(msg = ''):
    while True:
        if msg != '':
            print(f'\n{_N}{_fw} {msg}{_reset}')
            msg = ''
        UserInput = input(f'{_B}{_fw}\nConfirm{_fw} [ Yes / Save / No ] {_fy}[ Y / S / N ]{_fw} > {_reset}')
        if UserInput.lower().strip() in ['yes','y','']:
            return True,'run'
        elif UserInput.lower().strip() in ['s','save']:
            return True,'save'            
        else:
            if UserInput.lower().strip() in ['n','no']:
                return False,''
            else:
                msg = f'{_fr}Invalid Input{_reset}'

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
    print (f"  - Keep Alive : {_B}{_fy}{TunnelDict['Keep_Alive']}{_reset}")
    print (f"SSH Server Details :")
    print (f"  - IP : {_B}{_fy}{TunnelDict['ssh_ip']}{_reset}")
    print (f"  - User : {_B}{_fy}{TunnelDict['ssh_user']}{_reset}")
    print (f"  - Port : {_B}{_fy}{TunnelDict['ssh_port']}{_reset}")
    print (f"Advanced Options :")
    print (f'  - Highly restricted network mode : {_B}{_fy}{TunnelDict["Highly_Restricted_Networks"].get("Enable",False)}{_reset}')
    print (f"  - Monitor Port : {_B}{_fy}{TunnelDict['Highly_Restricted_Networks'].get('MonitorPort',0)}{_reset} Use Only for Highly Restricted Network Mode")
    

def CkeckNewMonitorPort(NewPort = None,TUNNEL_LIST = None):
    if TUNNEL_LIST == []:
        return True
    else:
        for tunnel in TUNNEL_LIST:
            TunnelDict = TUNNEL_LIST[tunnel]
            if TunnelDict["Highly_Restricted_Networks"].get('Enable',False):
                MonitorPort = TunnelDict["Highly_Restricted_Networks"].get('MonitorPort',0)
                if MonitorPort != 0:
                    if NewPort == MonitorPort:
                        return False
    return True

def CreateTunnle(Mode = None,Msg = '',TUNNEL_LIST = []):
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
        TunnelHelpMode(Mode,ColorBox=_fc)
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

                        if CkeckNewMonitorPort(NewPort=int(_monitorPort),TUNNEL_LIST=TUNNEL_LIST):
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
            _Keep_Alive = input(f'{_B}{_fw}\n\nEnable 🔒 Keep Alive [ Yes / No ] [ {_fy}Y / N{_fw} ] > {_fy}')
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
                if _Code.lower() == TUNNEL_LIST[_t]['Code'].lower():
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

def CreateNewConnection(ServerLIST = {}):
    _Msg = ''
    _ServerName = ''
    _ip = ''
    _port = ''
    _user = ''
    _tags = []
    _code = ''
    _group = ''
    _icon = None
    _authentication = ''
    _key_file = ''
    _password = ''
    _FINISH = False
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()
        if _Msg != '':
            lib.AsciArt.BorderIt(Text=_Msg,BorderColor=_fr,TextColor=_fy)
            _Msg = ''            
        print(f"\n{_B}{_fw}Create New Server ...{_reset}")
        print(f'\n{_fw}Group Name     : {_fy}{_group}{_reset}')
        print(f'{_fw}Code           : {_fy}{_code}{_reset}')
        print(f'{_fw}Server Name    : {_fy}{_ServerName}{_reset}')
        print(f'{_fw}Server IP      : {_fy}{_ip}{_reset}')
        print(f'{_fw}Server Port    : {_fy}{_port}{_reset}')
        print(f'{_fw}Server User    : {_fy}{_user}{_reset}')
        print(f'{_fw}Tags:          : {_fy}{_tags}{_reset}')
        print(f'{_fw}Authentication : {_fy}{_authentication}{_reset}')

        if _group == '':            
            SrvLst = f'{_reset}'
            for _s in ServerLIST:
                SrvLst = SrvLst + f'{_bEx_bl}{_fw} {_s.upper()} {_reset} '
            print(f'{_D}{_fw}\n\nExisted Group : {SrvLst}')
            _groupInputed = input(f'{_B}{_fw}\nEnter {_fc}Group Name{_fw} [ {_fy}Default{_fw} ] > {_fy}')
            if _groupInputed.strip() == '':
                _group = 'Default'.lower()
            else:
                _group = _groupInputed.strip().lower()
        elif _code == '':
            _codeInputed = input(f'{_B}{_fw}\nEnter Server {_fc}Code{_fw} > {_reset}')
            if _codeInputed == '':
                _Msg = 'Code not empty'
                continue
            elif len(_codeInputed) > 5:
                _Msg = 'Code in 5 cht'
                continue
            elif ServerCodeIsUniq(NewCode=_codeInputed,ServerLIst=ServerLIST):
                _code = _codeInputed.lower().strip()
            else:
                _Msg = f'Entered Code ( {_codeInputed} ) is Not Uniq'
                continue
        elif _ServerName == '':
            _serverNameInputed = input(f'{_B}{_fw}\nEnter Server {_fc}Name{_fw} > {_reset}')
            if _serverNameInputed.strip() == '':                
                continue
            else:
                _ServerName = _serverNameInputed.strip()
        elif _ip == '':
            _ipInputed = input (f'\n{_B}{_fw}Enter {_fc}SSH{_fw} Server {_fc}IP or Hostname{_fw} > {_reset}')
            if _ipInputed.strip() == '':
                continue
            else:
                _ip = _ipInputed.strip()
        elif _port == '':
            _portInputed = input (f'\n{_B}{_fw}Enter {_fc}SSH{_fw} Server {_fc}Port{_fw} [ {_fy}22{_fw} ]> {_reset}')
            if _portInputed == '':
                _port = 22
            else:
                try:
                    _port = int(_portInputed)
                except:
                    _Msg = "SSH Port is not a valid number"
                    continue                    
                if not (1 <= _port <= 65535):
                    _Msg = 'SSH Port is out of valid range (1-65535)'
                    _port = ''
                    continue
        elif _user == '':
            _UserInputed = input (f'\n{_B}{_fw}Enter {_fc}SSH User{_fw} [ {_fy}root{_fw} ]> {_reset}')
            if _UserInputed.lower().strip() == '':
                _user = 'root'
            else:
                _user = _UserInputed.strip()
        elif _tags == []:
            _Tagst = ListofTags(ServerList=ServerLIST)
            print(f'\n\n{_D}{_fw}Existed Tags {_reset}{_Tagst}')
            _enterdTags = input(f'\n{_B}{_fw}Enter {_fc}Tags{_fw} >{_reset} ')
            TagSpilted = _enterdTags.split(' ')
            for _t in TagSpilted:
                _tags.append(_t.upper())
        elif _icon == None:
            print('\n')
            PrintListof_Emoji()
            SelectedIcon = input(f'\n\n{_D}{_fw}Select {_fc}Icon{_fw} and Copy/Pate [ {_fy}No Icon{_fw} ] {_reset} > ')
            if SelectedIcon.strip() == '':
                _icon = ''
            elif len(SelectedIcon.strip()) > 1:
                _Msg = 'The number of characters allowed for an icon is a number.'
                continue
            else:
                _icon = SelectedIcon.strip()
        elif _authentication == '':
            menuItem = []
            menuItem.append('Use defualt authentication')
            menuItem.append('Enter Path on key file')
            menuItem.append('Enter Password')
            UserSelect = lib.AsciArt.GenerateMenu(Titel='Authentication Method',
                                        InputMsg='Select Authentication method >',
                                        MenuList=menuItem)
            if UserSelect == 'q':
                lib.BaseFunction.FnExit()
            elif UserSelect == 'b':
                continue
            elif UserSelect == '1':
                _authentication = 'defualt'
                _FINISH = True
            elif UserSelect == '2':
                _authentication = 'key_file'
                continue
            elif UserSelect == '3':
                _authentication = 'password'
                continue
        elif _authentication == 'key_file':
            if _key_file == '':
                _inputkeyfile = input (f'\n{_B}{_fw}Enter Path of {_fc}Key file{_fw} > {_reset}')
                if _inputkeyfile.strip() == '':
                    continue
                else:
                    if not os.path.isfile(_inputkeyfile.strip()):
                        _Msg = f"The specified key file does not exist: {_inputkeyfile}\nPlease check the path and try again."
                        continue
                    else:
                        _key_file = _inputkeyfile.strip()
                        _FINISH = True
        elif _authentication == 'password':
            if _password == '':
                _inputPassword = input (f'\n{_B}{_fw}Enter {_fc}Password{_fw} > {_reset}')
                if _inputPassword == '':
                    continue
                else:
                    _password = _inputPassword.strip()
                    _FINISH = True
        if _FINISH:
            print("\n")
            _rst = lib.AsciArt.FnConfirmChange(MsgStr=f"Save {_fc + _ServerName + _fw} with code {_fc +  _code + _fw} ?",YesTxt='Yes',NoText='No try again')
            if _rst == None:
                continue
            elif _rst:
                if ServerLIST.get(_group,False) is False:
                    ServerLIST[_group] = {}
                    ServerLIST[_group]["servers"] = {}
                ServerLIST[_group]["servers"][_code] = {}
                ServerLIST[_group]["servers"][_code]["server_name"] = _ServerName
                ServerLIST[_group]["servers"][_code]["ip"] = _ip
                ServerLIST[_group]["servers"][_code]["port"] = _port
                ServerLIST[_group]["servers"][_code]["user"] = _user
                ServerLIST[_group]["servers"][_code]["tags"] = _tags
                ServerLIST[_group]["servers"][_code]["icon"] = _icon
                ServerLIST[_group]["servers"][_code]["authentication"] = _authentication
                if _authentication == 'password':
                    ServerLIST[_group]["servers"][_code]["password"] = _password
                elif _authentication == 'key_file':
                    ServerLIST[_group]["servers"][_code]["key_file"] = _key_file
                try:
                    with open(ServerConfigFile, 'w') as json_file:
                        json.dump(ServerLIST, json_file, indent=4)
                        print(f"{_B}{_fw}\nTunnel [ {_fEx_g}{_ServerName}{_fw} ] Saved Successfully{_reset}")
                        lib.BaseFunction.PressEnterToContinue()
                        return True
                except:
                    print(f"{_fr}Error on Update [ {ServerConfigFile} ] operation Faild{_reset}\n")
                    lib.BaseFunction.PressEnterToContinue()
                    return False    
            else:
                _ServerName = ''
                _ip = ''
                _port = ''
                _user = ''
                _tags = []
                _code = ''
                _group = ''
                _icon = ''    
                _authentication = ''
                _key_file = ''
                _password = ''
                _FINISH = False


                


def PrintListof_Emoji():    
    IconInLine = 0
    MsgStr = ''
    for _em in lib.AsciArt.LIST_OF_EMOJI:
        MsgStr = MsgStr + f' {_em} '
        if IconInLine == 20:
            MsgStr =  MsgStr + '\n'
            IconInLine = 0
        else:
            IconInLine += 1
    print(MsgStr)


def ListofTags(ServerList):    
    SetofTags = set()
    for _g in ServerList:
        _Servers = ServerList[_g]['servers']
        for _s in _Servers:
            TagsList = _Servers[_s]['tags']
            for tag in TagsList:
                SetofTags.add(tag.upper())
    ListOfTags = list(SetofTags)

    Count = 0
    TagsinLine = 0
    TagStr = ''
    for tag in ListOfTags:
        TagStr = TagStr +  f'{_bEx_bl}{_fw} {tag.upper()} {_reset} '
        if TagsinLine == 10:
            TagStr = TagStr + '\n'
            TagsinLine = 0
        Count +=1
    return TagStr

def FnListOfGroup(ServerList):
    ServerLst = []
    for Group in ServerList:
        ServerLst.append(Group)
    return ServerLst


def ServerCodeIsUniq(NewCode = '',ServerLIst= {}):
    for _group in ServerLIst:
        GroupDict = ServerLIst[_group]["servers"]
        for _s in GroupDict:
            if _s.strip().lower() == NewCode.lower().strip():
                return False
    return True


def EditServerConnection(ServerCode):
    _Rst = GetServerDictbyCode(Code=ServerCode)
    ServerDict = _Rst[0]
    Group = _Rst[1]
    _Msg = ''
    GetName = GetIp = GetPort = GetUser = GetTags = GetIcon = GetAuthentication = GetAuthentication_step2 =  False
    FINISH = False
    if ServerDict == None:
        return False, 'Error In Find Server For Edit'
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogo()
        if _Msg != '':
            lib.AsciArt.BorderIt(Text=_Msg,BorderColor=_fr,TextColor=_fy)
            _Msg = ''            
        print(f"\n{_B}{_fw}Edit Server Connection ...{_reset}")
        print(f'\n{_fw}Group Name     : {_fw}{Group}{_reset}')
        print(f'{_fw}Code           : {_fw}{ServerCode}{_reset}')
        print(f'{_fw}Server Name    : {_fy}{ServerDict["server_name"]}{_reset}')
        print(f'{_fw}Icon           : {_fy}{ServerDict["icon"]}{_reset}')
        print(f'{_fw}Server IP      : {_fy}{ServerDict["ip"]}{_reset}')
        print(f'{_fw}Server User    : {_fy}{ServerDict["user"]}{_reset}')
        print(f'{_fw}Server Port    : {_fy}{ServerDict["port"]}{_reset}')
        print(f'{_fw}Tags:          : {_fy}{ServerDict["tags"]}{_reset}')
        print(f'{_fw}Authentication : {_fy}{ServerDict["authentication"]}{_reset}')
        if GetName is False:
            NameInputed = input(f'\n{_B}{_fw}Enter Name [ {_fy}{ServerDict["server_name"]} {_fw}]{_reset} > ')
            if NameInputed.strip() == '':
                GetName = True
            else:
                ServerDict['server_name'] = NameInputed.lower()
                GetName = True
        elif GetIp is False:
            IpInputed  = input(f'\n{_B}{_fw}Enter ip [ {_fy}{ServerDict["ip"]} {_fw}]{_reset} > ')
            if IpInputed.strip() == '':
                GetIp = True
            else:
                GetIp = True
                ServerDict['ip'] = IpInputed.strip()
        elif GetUser is False:
            UserInputed = input(f'\n{_B}{_fw}Enter Usernane [ {_fy}{ServerDict["user"]} {_fw}]{_reset} > ')
            if UserInputed.strip == '':
                GetUser = True
            else:
                GetUser = True
                ServerDict['user'] = UserInputed.strip()
        elif GetPort is False:
            PortInputed = input(f'\n{_B}{_fw}Enter ssh port [ {_fy}{ServerDict["port"]} {_fw}]{_reset} > ')
            if PortInputed.strip() == '':
                GetPort = True
            else:
                try:
                    _port = int(PortInputed)
                except:
                    _Msg = 'SSH Port is not a valid number'
                    continue
                if not (1 <= _port <= 65535):
                    _Msg = 'SSH Port is out of valid range (1-65535)'
                    continue
                GetPort = True
                ServerDict['port'] = _port
        elif GetTags is False:
            _Tagst = ListofTags(ServerList=SERVER_LIST)
            print(f'\n\n{_D}{_fw}Existed Tags {_reset}{_Tagst}')
            TagsInputed = input(f'\n{_B}{_fw}Enter Server Tag/s [ {_fy}{ServerDict["tags"]} {_fw}]{_reset} > ')
            if TagsInputed.strip() == '':
                GetTags = True
            else:
                TagsInputed = TagsInputed.split(' ')
                TagList = []
                for _t in TagsInputed:
                    TagList.append(_t.upper())
                ServerDict['tags'] = TagList
                GetTags = True
        elif GetIcon is False:
            print('\n')
            PrintListof_Emoji()
            IconInputed = input(f'\n{_B}{_fw}Select icon [ {_fy}{ServerDict["icon"]} {_fw}]{_reset} > ')
            if IconInputed.strip() == '':
                GetIcon = True
            else:
                if len(IconInputed) > 1 :
                    _Msg = 'The number of characters allowed for an icon is a number.'
                    continue
                else:
                    ServerDict['icon'] = IconInputed.strip()
                    GetIcon = True
        elif GetAuthentication is False:
            _authentication = ServerDict["authentication"]
            if _authentication.strip() == '':
                _authentication = 'defualt'
            authenticationInputed = input(f'\n{_B}{_fw}Select Authentication Method [ {_fy}{_authentication} {_fw}] for Change [ {_fr}C{_fw} ]{_reset} > ')
            if authenticationInputed.strip() == '':
                GetAuthentication = True
            elif authenticationInputed.strip().lower() == 'c':
                menuItem = []
                menuItem.append('Use defualt authentication')
                menuItem.append('Enter Path on key file')
                menuItem.append('Enter Password')
                UserSelect = lib.AsciArt.GenerateMenu(Titel='Authentication Method',
                                            InputMsg='Select Authentication method >',
                                            MenuList=menuItem)           
                if UserSelect == 'q':
                    lib.BaseFunction.FnExit()
                elif UserSelect == 'b':
                    continue
                elif UserSelect == '1':
                    _authentication = 'defualt'
                    GetAuthentication = True                    
                    GetAuthentication_step2 = True
                    ServerDict['authentication'] = ''
                    ServerDict['password'] = ''
                    ServerDict['key_file'] = ''
                    FINISH = True
                    continue
                elif UserSelect == '2':
                    _authentication = 'key_file'
                    GetAuthentication = True
                    continue
                elif UserSelect == '3':
                    _authentication = 'password'
                    GetAuthentication = True
                    continue
        elif GetAuthentication_step2 is False:            
            if _authentication == 'key_file':
                _key_file = ServerDict.get('key_file','')
                if _key_file == '':
                    _inputkeyfile = input (f'\n{_B}{_fw}Enter Path of {_fc}Key file{_fw} > {_reset}')
                    if _inputkeyfile.strip() == '':
                        continue
                    else:
                        if not os.path.isfile(_inputkeyfile.strip()):
                            _Msg = f"The specified key file does not exist: {_inputkeyfile}\nPlease check the path and try again."
                            continue
                        else:
                            _key_file = _inputkeyfile.strip()
                            GetAuthentication_step2 = True
                            ServerDict['key_file'] = _key_file.strip()
                            FINISH = True
            elif _authentication == 'password':
                _password = ServerDict.get('password','')
                if _password == '':
                    _inputPassword = input (f'\n{_B}{_fw}Enter {_fc}Password{_fw} > {_reset}')
                    if _inputPassword == '':
                        continue
                    else:
                        _password = _inputPassword.strip()
                        GetAuthentication_step2 = True
                        ServerDict['password'] = _password.strip()
                        FINISH = True
            elif _authentication == 'defualt':
                ServerDict['authentication'] = ''
                ServerDict['password'] = ''
                ServerDict['key_file'] = ''
                FINISH = True


        if FINISH:
            print("\n")
            rst = lib.AsciArt.FnConfirmChange(MsgStr="Save Change/s ?",YesTxt="Yes, SaveIt",NoText="No,Cancel")
            if rst:                
                SERVER_LIST[Group]['servers'][ServerCode]['server_name'] = ServerDict['server_name']
                SERVER_LIST[Group]['servers'][ServerCode]['ip'] = ServerDict['ip']
                SERVER_LIST[Group]['servers'][ServerCode]['port'] = ServerDict['port']
                SERVER_LIST[Group]['servers'][ServerCode]['user'] = ServerDict['user']
                SERVER_LIST[Group]['servers'][ServerCode]['tags'] = ServerDict['tags']
                SERVER_LIST[Group]['servers'][ServerCode]['icon'] = ServerDict['icon']
                SERVER_LIST[Group]['servers'][ServerCode]['ip'] = ServerDict['ip']
                SERVER_LIST[Group]['servers'][ServerCode]['authentication'] = ServerDict['authentication']
                if ServerDict['authentication'] == 'password':
                    SERVER_LIST[Group]['servers'][ServerCode]['password'] = ServerDict['password']
                    SERVER_LIST[Group]['servers'][ServerCode]['key_file'] = ''
                elif ServerDict['authentication'] == 'key_file':
                    SERVER_LIST[Group]['servers'][ServerCode]['password'] = ''
                    SERVER_LIST[Group]['servers'][ServerCode]['key_file'] = ServerDict['key_file']
                elif ServerDict['authentication'] in ['','defualt']:
                    SERVER_LIST[Group]['servers'][ServerCode]['authentication'] = ''
                    SERVER_LIST[Group]['servers'][ServerCode]['password'] = ''
                    SERVER_LIST[Group]['servers'][ServerCode]['key_file'] = ''
                SaveRst = lib.BaseFunction.SaveJsonFile(JsonFile=ServerConfigFile,JsonData=SERVER_LIST)
                if SaveRst[0]:
                    print(f"{_B}{_fw}\nTunnel [ {_fEx_g}{ServerDict['server_name']}{_fw} ] Saved Successfully{_reset}")
                    lib.BaseFunction.PressEnterToContinue()
                    return True
                else:
                    print(f"Error is Saved Tunnel [ {SaveRst[1]} ]")

                
                






                        





                


        
                





if __name__ == "__main__":        
    print(f"{_B}{_fy}You should not run this file directly")


