import lib.AsciArt
import lib.BaseFunction
import lib.Logo
import core
import os
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

SourceLst = [] 
destinationLst = [] 
SourcePath = ''
DestPath = ''

def ScpMenu(ServerList):
    global SourceLst
    global destinationLst
    global SourcePath
    global DestPath
    SourceLst = [] 
    destinationLst = [] 
    SourcePath = ''
    DestPath = ''
    SelectedServerRole = SpecifyingFomOrTo(ServerList)
    if SelectedServerRole == 'FROM':
        # Copy From Remote
        SourceLst = ServerList
        SourcePath = GetAddress(InLocal=False,EnterIsValid=False,mode='sfile')
        destinationLst = ServerSelect(Mode='Destination',LocalIsValid=True,mode='to')
        DestPath = GetAddress(InLocal=False,EnterIsValid=True,mode='dfile')
        if DestPath in ['','.']:
            if destinationLst['IP'] == 'localhost':
                DestPath = '.'
            else:
                if destinationLst['User'] == 'root':
                    DestPath = '/root'
                else:
                    DestPath = f'/home/{destinationLst["User"]}'            
    else:
        destinationLst = ServerList
        SourceLst = ServerSelect(Mode='Source',LocalIsValid=True,mode='both')
        SourcePath = lib.BaseFunction.GetValue(SourceLst,"FileName",ReturnValueForNone='',verbus=False)
        if SourcePath == '':
            SourcePath = GetAddress(InLocal=True,EnterIsValid=False,mode='sfile')
        DestPath = GetAddress(InLocal=False,EnterIsValid=True,mode='dfile')

    RunScpCommand()
    
    
def RunScpCommand():
    lib.BaseFunction.clearScreen()
    lib.Logo.SshToolsLogoScp()    
    lib.Logo.ScpProgress(SourceLst=SourceLst,destinationLst=destinationLst,SourcePath=SourcePath,DestPath=DestPath,mode='confirm')    
    UserInput = input(f'\n{_B}{_fw}Press {_fg}ENTER{_fw} for Copy or {_fr}other key{_fw} for Cancel :{_reset}')
    if UserInput.strip() == '':
        ScpCommand()
    else:        
        lib.BaseFunction.FnExit()    

def ScpCommand():
    from main import SSHKEY
    if SSHKEY != '':
        ScpCommand = f'scp -r -i {SSHKEY} -P '
    else:
        ScpCommand = 'scp -r -P'        
        
    if SourceLst["IP"] == 'localhost':
        _Port = destinationLst['Port']
        _User = destinationLst['User']                
        _IP = destinationLst['IP']
        ScpCommand = f'{ScpCommand} {_Port} {SourcePath} {_User}@{_IP}:{DestPath}'
    elif destinationLst["IP"] == 'localhost':
        _Port = SourceLst['Port']
        _User = SourceLst['User']                
        _IP = SourceLst['IP']
        ScpCommand = f'{ScpCommand} {_Port} {_User}@{_IP}:{SourcePath} {DestPath}'
    else:
        _s_Port  = SourceLst["Port"]
        _s_IP  = SourceLst["IP"]
        _s_User  = SourceLst["User"]
        _d_Port = destinationLst["Port"]
        _d_IP  = destinationLst["IP"]
        _d_User  = destinationLst["User"]
        if customSSHPortOnBothServer() is False:
            ScpCommand = f'{ScpCommand} {_s_Port} {_s_User}@{_s_IP}:{SourcePath} {_d_User}@{_d_IP}:{DestPath}'
        else:
            if SSHKEY != '':
                ScpCommand = f'scp -i {SSHKEY}-P'
            else:
                ScpCommand = 'scp -P'
            ScpCommand = f'{ScpCommand} {_s_Port} -P {_d_Port} -r -o "ProxyJump={_s_User}@{_s_IP}:{_s_Port}" {_d_User}@{_d_IP}:{_d_Port}:{DestPath} {SourcePath}'
                
    _Rst = os.system(ScpCommand)
    if _Rst == 0:
        lib.AsciArt.BorderIt(Text='Copy successfully finished',BorderColor=_fb,TextColor=_fw)
    else:
        lib.AsciArt.BorderIt(Text='Copy failed !!!',BorderColor=_fr,TextColor=_fw)
    lib.BaseFunction.FnExit()


def customSSHPortOnBothServer():
    if SourceLst["IP"] != "localhost":       
        if destinationLst["IP"] != 'localhost':          
            if SourceLst["Port"] != '22':
                if destinationLst["Port"] != '22':
                    if SourceLst["Port"] != destinationLst["Port"]:                        
                        return True
    return False

    
def SpecifyingFomOrTo(ServerList):
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogoScp()
        lib.Logo.ScpProgress(SourceLst=SourceLst,destinationLst=destinationLst,SourcePath=SourcePath,DestPath=DestPath,mode='')
        core.printServerInfo(ServerList["Code"])        
        print(f'\n\n{_B}{_fw}Server [ {_fEx_y}{ServerList["ServerName"]} ( {_bEx_y}{_fbl}{ServerList["IP"]}{_reset}{_B} {_fEx_y}) ]{_fw} is {_fEx_g}Source{_fw} or {_fEx_c}Destination{_fw} ?{_reset}')
        #UserInput = input(f'{_B}{_fEx_g}ENTER{_fw} for source or {_fEx_c}Any Key{_fw} for destination{_reset} : ')        
        UserInput = input(f'{_B}{_fw}Type [ {_fEx_g}f / s {_fw}] for Source or [ {_fEx_c}d / t{_fw} ] for Destination  > {_reset}')
        if UserInput.strip() in ['','f','s','source','from']:
            return 'FROM'
        elif UserInput.strip() in ['d','destination','to','t']:
            return 'TO'
    
def SearchServer(msg='',Mode = 'Destination',LocalIsValid = True,mode=''):
    _SrvList = None
    UserInput = ''
    _CopdeFoundInServerlist = False
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogoScp()        
        lib.Logo.ScpProgress(SourceLst=SourceLst,destinationLst=destinationLst,SourcePath=SourcePath,DestPath=DestPath,mode=mode)        
        if Mode == 'Source':
            ListFilesDict = PrintListOfFileInCurrentDir()                                
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
            if LocalIsValid:
                print(f'{_N}{_fw}for Select local Server Press ( {_D}Enter {_N} ) or type ( {_D}.{_N} ){_reset}')            
                if Mode == 'Source':
                    print(f'{_N}{_fw}or Enter the {_D}File number{_N}, {_D}file name{_N} or {_D}Full address{_reset}')
            UserInput = input(f'{_B}{_fw}Type for {_fr}{Mode}{_fw} servers > {_reset}')
        if UserInput.lower().strip() in ['q']:
            lib.BaseFunction.FnExit()            
        else:
            if LocalIsValid:
                if UserInput.lower().strip() in ['','.','127.0.0.1','local','localhost']:
                    return 'local'
            if Mode == 'Source':
                try:
                    FileNumber = int(UserInput)
                    if FileNumber <= 40:
                        filename = ListFilesDict[FileNumber]
                        lst = {}
                        lst["IP"] = "localhost"
                        lst["ServerName"] = "localhost"
                        lst["FileName"] = filename
                        return lst
                except:
                    if lib.BaseFunction.IsExist(UserInput):
                        lst = {}
                        lst["IP"] = "localhost"                        
                        lst["ServerName"] = "localhost"
                        lst["FileName"] = UserInput
                        return lst
                
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


def ServerSelect(Mode = 'Destination',LocalIsValid = False,mode = ''):
    while True:
        ServerCode = SearchServer(Mode=Mode,LocalIsValid=LocalIsValid,mode=mode)
        if type(ServerCode) is dict:
            return ServerCode
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogoScp()
        if mode == 'both':
            mode = 'from'
        lib.Logo.ScpProgress(SourceLst=SourceLst,destinationLst=destinationLst,SourcePath=SourcePath,DestPath=DestPath,mode=mode)
        ServerLst = core.printServerInfo(ServerCode)                
        
        print(f'\n{_B}{_fw}Are you Shure to Select Server [{_fy}{ServerLst["ServerName"]} ( {_bEx_y}{_fbl} {ServerLst["IP"]} {_reset}{_fy} )]{_fw} for {_fEx_r}{Mode}{_reset}:')
        UserInput = input(f'{_fEx_g}ENTER{_fEx_w} for Select as {_fEx_g}{Mode}{_fEx_w} or Any Key for destination : {_reset}')
        if UserInput.strip() == '':
            return ServerLst
        
def GetAddress(InLocal = False,EnterIsValid = False,mode = ''):
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.SshToolsLogoScp()
        lib.Logo.ScpProgress(SourceLst=SourceLst,destinationLst=destinationLst,SourcePath=SourcePath,DestPath=DestPath,mode=mode)
        if InLocal:
            ListFilesDict = PrintListOfFileInCurrentDir()            
        print(f'{_fw}\n - Enter the full path address of the {_fb}file{_fw} or {_fb}directory{_fw}.')
        if InLocal:
            print(f'{_fw}- If the {_fb}file{_fw} or {_fb}directory{_fw} is in the current path, we can enter its {_fy}name{_fw} or {_fy}number{_fw}.{_reset}')
        UserInput = input(f'{_B}{_fw}Enter FileName > {_reset}')
        
        ## VALIDATE
        if UserInput.lower().strip() in ['','.']:
            if EnterIsValid:
                return '.'
        else:
            if InLocal:
                try:
                    FileNumber = int(UserInput)
                    if FileNumber <= 40:
                        filename = ListFilesDict[FileNumber]
                        return filename
                except:
                    if lib.BaseFunction.IsExist(UserInput):
                        return UserInput                        
            return UserInput.strip()

def PrintListOfFileInCurrentDir(FileNumber=40):
    print(f'\n{_fw}List of files...\n{_reset}')
    ListFiles = os.listdir()       
    i = 0
    ListDict = {}
    for _ in ListFiles:
        i += 1
        print ("   # {no:<12} --->  [ {Filename} ]".format(no=f"{_fy}{i}{_reset}", Filename = f"{_fy}{_}{_reset}"))
        ListDict[i]= _
        if i > FileNumber:
            print(f"\n\n {_fw}more ...{_reset}")            
    print("")
    return ListDict


if __name__ == "__main__":    
    print(f"You should not run this file directly")

