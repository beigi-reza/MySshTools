import lib.BaseFunction
import lib.AsciArt
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset


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
    



    SShServeraddr = f'{ServerDict["User"]}@{ServerDict["IP"]}:{ServerDict["Port"]}'
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
            if tunnel["Highly_Restricted_Networks"].get('Enable',False):
                MonitorPort = tunnel["Highly_Restricted_Networks"].get('MonitorPort',0)
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
            for TUNNEL in TUNNEL_LIST:
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



if __name__ == "__main__":        
    print(f"{_B}{_fy}You should not run this file directly")
