import lib.BaseFunction
import lib.Logo
import lib.AsciArt
import os
import json
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

current_directory = os.path.dirname(os.path.realpath(__file__))
JsonConfigFile = os.path.join(current_directory,'conf/config.json')
JsonConfig = lib.BaseFunction.LoadJsonFile(JsonConfigFile)
ServerConfigFile = os.path.join(current_directory,'conf/ServerList.json',)
SERVER_LIST = lib.BaseFunction.LoadJsonFile(JsonFile=ServerConfigFile,ReternValueForFileNotFound={},Verbus=False)
TAG_VIEW = JsonConfig.get("Tag_View",False)
#TAG_VIEW = lib.BaseFunction.GetValue(JsonConfig,"Tag_View",verbus=False,ReturnValueForNone=False)
SSHKEY = lib.BaseFunction.GetValue(JsonConfig,"SSHKEY",verbus=False,ReturnValueForNone='')

TunnelJsonFilePath = os.path.join(current_directory,'conf/tunnel.json')
TUNNEL_LIST = lib.BaseFunction.LoadJsonFile(JsonFile=TunnelJsonFilePath,Verbus=False,ReternValueForFileNotFound={})
LOG_PATH = os.path.join(JsonConfig.get('log_path','/var/log'),'ssh-log')
GROUP_LIST = []
for _g in SERVER_LIST:
    GROUP_LIST.append(_g)
######################################################
######################################################

if os.path.exists(SSHKEY) == False:
    lib.BaseFunction.clearScreen()
    lib.Logo.SshToolsLogo()
    lib.AsciArt.BorderIt(Text=f'canot find the SSH key File ({SSHKEY})',BorderColor=_fr,TextColor=_fw)
    lib.BaseFunction.FnExit(1)

def RefreshServerList():
    global SERVER_LIST
    SERVER_LIST = lib.BaseFunction.LoadJsonFile(JsonFile=ServerConfigFile,ReternValueForFileNotFound={},Verbus=False)
    return SERVER_LIST
    

def FindServers(SerachKey):
    """Search for servers based on the entered key
    Args:
        SerachKey (str): The key to search for in the server list
    return: list of servers
    """
    FndServerLst = []
    for _serverGruop in SERVER_LIST:
        for _s in SERVER_LIST[_serverGruop].get('servers',{}):
            _server = SERVER_LIST[_serverGruop]["servers"][_s] 
            ## Server Name
            if lib.BaseFunction.FindString(string=_server["server_name"],substring=SerachKey):
                FndServerLst.append(_s.lower().strip())
                continue
            # IP
            if lib.BaseFunction.FindString(string=_server["ip"],substring=SerachKey):
                FndServerLst.append(_s.lower().strip())
                continue
            # Code
            if lib.BaseFunction.FindString(string=_s,substring=SerachKey):
                FndServerLst.append(_s.lower().strip())
                continue
            # Group
            if lib.BaseFunction.FindString(string=_serverGruop,substring=SerachKey):
                FndServerLst.append(_s.lower().strip())
                continue
            for _ in _server["tags"]:
                if lib.BaseFunction.FindString(string=_,substring=SerachKey):
                    FndServerLst.append(_s.lower().strip())
                    continue
    return FndServerLst

def PrintServerList(ServersList,highlight_text=''):
    lib.BaseFunction.clearScreen()
    lib.Logo.SshToolsLogo()    
    if TAG_VIEW:
        _lenName = 40
        _lenIP = 18
        _lenTags = 35
        _lenCode = 10
    else:    
        _lenName = 65
        _lenIP = 24
        _lenTags = 0
        _lenCode = 15
    _Count = 1
    TitleHeaderStr = f"{_B}{_bb}{_fw}{lib.AsciArt.FnAlignmentStr(originalString='Server Name',AlignmentMode='left',target_length=_lenName)}{_reset}"
    IpHeaderStr = f"{_B}{_bb}{_fw}{lib.AsciArt.FnAlignmentStr(originalString='ip',AlignmentMode='left',target_length=_lenIP)}{_reset}"
    TagsHeaderStr = f"{_B}{_bb}{_fw}{lib.AsciArt.FnAlignmentStr(originalString='Tags',AlignmentMode='left',target_length=_lenTags)}{_reset}"
    CodeHeaderStr = f"{_B}{_by}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='Code',AlignmentMode='left',target_length=_lenCode)}{_reset}"
    if TAG_VIEW:
        print(f"\n\n{TitleHeaderStr} {IpHeaderStr} {CodeHeaderStr} {TagsHeaderStr}{_reset}")
    else:
        print(f"\n\n{TitleHeaderStr} {IpHeaderStr} {CodeHeaderStr}{_reset}") 
    for _gruop in GROUP_LIST:
        if ServersList == 'ALL':
            GroupNameStr = f"{_fy}{lib.AsciArt.FnAlignmentStr(originalString=_gruop,AlignmentMode='left',target_length=55)}{_reset}"            
            print(f"\n{GroupNameStr}")            
            for _Server in SERVER_LIST:            
                if _Server["Group"] == _gruop:                    
                    PrintServerLine(ServerDict=_Server,
                                    lenName=_lenName,
                                    lenIP=_lenIP,
                                    lenTags=_lenTags,
                                    lenCode=_lenCode,
                                    LineNumber=_Count,
                                    HighlightText=highlight_text)
                    _Count += 1
        else:
            Founded = False            
            for _ServerCode in SERVER_LIST[_gruop]["servers"]:                
                if _ServerCode in ServersList:
                    _Server = SERVER_LIST[_gruop]["servers"][_ServerCode]                    
                    _Server['code'] = _ServerCode
                    if Founded is False:
                        Founded = True
                        GroupNameStr = f"{_fy}{lib.AsciArt.FnAlignmentStr(originalString=_gruop.upper(),AlignmentMode='left',target_length=55)}{_reset}"
                        print(f"\n{GroupNameStr}")
                    PrintServerLine(ServerDict=_Server,
                                    lenName=_lenName,
                                    lenIP=_lenIP,
                                    lenTags=_lenTags,
                                    lenCode=_lenCode,
                                    LineNumber=_Count,
                                    HighlightText=highlight_text)
                    _Count += 1
        
                            
    if TAG_VIEW:
        print(f"\n\n{TitleHeaderStr} {IpHeaderStr} {CodeHeaderStr} {TagsHeaderStr}{_reset}")
    else:
        print(f"\n\n{TitleHeaderStr} {IpHeaderStr} {CodeHeaderStr}{_reset}")
        
def PrintServerLine(ServerDict,lenName,lenIP,lenTags,lenCode,LineNumber=0,HighlightText=''):
    Icon = ServerDict.get('icon',' ')
    TagStr = f'{_reset}'
    if LineNumber > 0:
        #LineNumberStr = f" {_B}{_by}{_fbl}#{LineNumber} {_reset}"
        LineNumberStr = f" {_fc}#{LineNumber} {_reset}"
    else:
        LineNumberStr = ''    
    _tags = ServerDict.get('tags',[] )
    if len(_tags) > 0:
        for _ in _tags:
            if _.lower().strip() == HighlightText.lower().strip():
                TagStr += f"{_fbl}{_bw} {_} {_reset} "
            elif HighlightText.lower().strip() in _.lower().strip():
                TagStr += f"{_fbl}{_bb} {_} {_reset} "                
            else:
                TagStr += f"{_fbl}{_bc} {_} {_reset} "    

    _ServerName = lib.AsciArt.FnAlignmentStr(originalString=ServerDict["server_name"],AlignmentMode='left',target_length=lenName)
    _ServerIP = lib.AsciArt.FnAlignmentStr(originalString=ServerDict["ip"],AlignmentMode='left',target_length=lenIP)
    #_ServerTags = lib.AsciArt.FnAlignmentStr(originalString=str(ServerDict["Tags"]).upper(),AlignmentMode='left',target_length=lenTags)
    _ServerCode = lib.AsciArt.FnAlignmentStr(originalString=ServerDict["code"],AlignmentMode='left',target_length=lenCode)
    if TAG_VIEW:
        print(f"{_fw}{LineNumberStr} {Icon} {_ServerName} {_ServerIP} {_B}{_fy}{_ServerCode}{_reset} {_D}{_fb}{TagStr} {_reset}\n")
    else:    
        print(f"{_fw}{LineNumberStr} {Icon} {_ServerName} {_ServerIP} {_B}{_fy}{_ServerCode}{_reset} {_reset}")            
    
def printServerInfo(ServerCode,PrintIt=True):
    try:
        if ServerCode == 'local':    
            if PrintIt:
                print(f"\n{_fw}Server Name : {_reset}{'🖥️   '}{_fEx_b}{'Localhost'}{_reset}")                       
            _Dict = {}
            _Dict["server_name"] = "Localhost"
            _Dict["ip"] = "localhost"
            _Dict["icon"] = "🖥️"
            return _Dict
    except:
        pass
    for _group in SERVER_LIST:
        for _code in SERVER_LIST[_group]['servers']:
            _ = SERVER_LIST[_group]['servers'][_code]
            if _code.lower().strip() == ServerCode.lower().strip():
                if PrintIt:
                    if _['icon'] != '':
                        Icon =  f'{_["icon"]}  '
                    else:
                        Icon = ''
                    print(f"\n{_fw}Server Name : {_reset}{Icon}{_fEx_b}{_['server_name']} {_bw}{_fbl} {_code} {_reset}")
                    print(f"{_fw}IP          : {_fy}{_['ip']}{_reset}")
                    print(f"{_fw}User        : {_fEx_b}{_['user']}{_reset}")
                    print(f"{_fw}Port        : {_fEx_b}{_['port']}{_reset}")
                    print(f"{_fw}Group       : {_fEx_b}{_group}{_reset}")
                    TagsStr = ''
                    for _t in _['tags']:
                        TagsStr += f"{_fw}{_bb} {_t} {_reset} "
                    print(f"{_fw}tags        : {TagsStr}{_reset}")
                return _



def CreategroupList(GroupBy='Group'):
    GroupList = []
    for _Server in SERVER_LIST:
        if _Server["Group"] not in GroupList:
            GroupList.append(_Server["Group"])
    return GroupList

def DeleteServerConnection(SeverCode):
    NewServerList = {}
    for _g in SERVER_LIST:        
        _group = SERVER_LIST[_g]['servers']
        for _s in _group:
            if _s.lower().strip() != SeverCode.lower().strip():
                ServerDict = _group[_s]            
                if _g not in NewServerList:
                    NewServerList[_g] = {}
                    NewServerList[_g]['servers'] = {}                
                NewServerList[_g]['servers'][_s] = ServerDict                    
    
    rst = lib.BaseFunction.SaveJsonFile(JsonData=NewServerList,JsonFile=ServerConfigFile,Verbus=False)
    if rst:
        print(f"{_B}{_fw}\nTunnel [ {_fEx_g}{ServerDict['server_name']}{_fw} ] Deleted Successfully{_reset}")
        lib.BaseFunction.PressEnterToContinue()
        return True
    else:
        print(f"{_fr}Error on Update [ {ServerConfigFile} ] operation Faild{_reset}\n")
        lib.BaseFunction.PressEnterToContinue()
        return False    

def GetServerDictbyCode(Code):
    """
    Input Server Code
    return 
    [0] > ServerDict
    [1] > Group Name    
    """
    for _g in SERVER_LIST:
        ServerList = SERVER_LIST[_g]['servers']
        for _s in ServerList:
            if _s.lower().strip() == Code.lower().strip():
                return SERVER_LIST[_g]['servers'][_s],_g
    return None        

if __name__ == "__main__":    
    print(f"You should not run this file directly")

