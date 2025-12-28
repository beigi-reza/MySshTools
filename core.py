import lib.BaseFunction
import lib.Logo
import lib.AsciArt
import os
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

current_directory = os.path.dirname(os.path.realpath(__file__))
JsonListFile = os.path.join(current_directory,'conf/config.json')
JsonConfig = lib.BaseFunction.LoadJsonFile(JsonListFile)
ServerConfigFile = os.path.join(current_directory,'conf/ServerList.json')
SERVER_LIST = lib.BaseFunction.LoadJsonFile(ServerConfigFile)["servers"]
TAG_VIEW = JsonConfig.get("Tag_View",False)
#TAG_VIEW = lib.BaseFunction.GetValue(JsonConfig,"Tag_View",verbus=False,ReturnValueForNone=False)
SSHKEY = lib.BaseFunction.GetValue(JsonConfig,"SSHKEY",verbus=False,ReturnValueForNone='')


######################################################
######################################################

if os.path.exists(SSHKEY) == False:
    lib.BaseFunction.clearScreen()
    lib.Logo.SshToolsLogo()
    lib.AsciArt.BorderIt(Text=f'canot find the SSH key File ({SSHKEY})',BorderColor=_fr,TextColor=_fw)
    lib.BaseFunction.FnExit(1)



def FindServers(SerachKey):
    """Search for servers based on the entered key
    Args:
        SerachKey (str): The key to search for in the server list
    return: list of servers
    """
    FndServerLst = []
    for _server in SERVER_LIST:
        ## Server Name
        if lib.BaseFunction.FindString(string=_server["ServerName"],substring=SerachKey):
            FndServerLst.append(_server["Code"])
            continue
        # IP
        if lib.BaseFunction.FindString(string=_server["IP"],substring=SerachKey):
            FndServerLst.append(_server["Code"])
            continue
        # Code
        if lib.BaseFunction.FindString(string=_server["Code"],substring=SerachKey):
            FndServerLst.append(_server["Code"])
            continue
        # Group
        if lib.BaseFunction.FindString(string=_server["Group"],substring=SerachKey):
            FndServerLst.append(_server["Code"])
            continue
        for _ in _server["Tags"]:
            if lib.BaseFunction.FindString(string=_,substring=SerachKey):
                FndServerLst.append(_server["Code"])
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
    IpHeaderStr = f"{_B}{_bb}{_fw}{lib.AsciArt.FnAlignmentStr(originalString='IP',AlignmentMode='left',target_length=_lenIP)}{_reset}"
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
                    PrintServerLine(_Server,lenName=_lenName,lenIP=_lenIP,lenTags=_lenTags,lenCode=_lenCode,HighlightText=highlight_text)
        else:
            Founded = False
            for _Server in SERVER_LIST:            
                if _Server["Code"] in ServersList:
                    if _Server["Group"] == _gruop:
                        if Founded is False:
                            Founded = True
                            GroupNameStr = f"{_fy}{lib.AsciArt.FnAlignmentStr(originalString=_gruop,AlignmentMode='left',target_length=55)}{_reset}"
                            print(f"\n{GroupNameStr}")
                        PrintServerLine(_Server,lenName=_lenName,lenIP=_lenIP,lenTags=_lenTags,lenCode=_lenCode,LineNumber=_Count,HighlightText=highlight_text)
                        _Count += 1
                            
    if TAG_VIEW:
        print(f"\n\n{TitleHeaderStr} {IpHeaderStr} {CodeHeaderStr} {TagsHeaderStr}{_reset}")
    else:
        print(f"\n\n{TitleHeaderStr} {IpHeaderStr} {CodeHeaderStr}{_reset}")
        
def PrintServerLine(ServerDict,lenName,lenIP,lenTags,lenCode,LineNumber=0,HighlightText=''):
    Icon = ServerDict["Icon"]    

    TagStr = f'{_reset}'
    if len(ServerDict["Tags"]) > 0:
        for _ in ServerDict["Tags"]:
            if _.lower().strip() == HighlightText.lower().strip():
                TagStr += f"{_fbl}{_bw} {_} {_reset} "
            elif HighlightText.lower().strip() in _.lower().strip():
                TagStr += f"{_fbl}{_bb} {_} {_reset} "                
            else:
                TagStr += f"{_fbl}{_bc} {_} {_reset} "            
    if Icon == '':
        Icon = ' '
    if LineNumber > 0:
        LineNumberStr = f"{_B}{_fy}{LineNumber}.{_reset}"
    else:
        LineNumberStr = ''    

    _ServerName = lib.AsciArt.FnAlignmentStr(originalString=ServerDict["ServerName"],AlignmentMode='left',target_length=lenName)
    _ServerIP = lib.AsciArt.FnAlignmentStr(originalString=ServerDict["IP"],AlignmentMode='left',target_length=lenIP)
    #_ServerTags = lib.AsciArt.FnAlignmentStr(originalString=str(ServerDict["Tags"]).upper(),AlignmentMode='left',target_length=lenTags)
    _ServerCode = lib.AsciArt.FnAlignmentStr(originalString=ServerDict["Code"],AlignmentMode='left',target_length=lenCode)
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
            _Dict["ServerName"] = "Localhost"
            _Dict["IP"] = "localhost"
            _Dict["Icon"] = "🖥️"
            return _Dict
    except:
        pass
    for _ in SERVER_LIST:
        if _["Code"] == ServerCode:            
            if PrintIt:
                if _['Icon'] != '':
                    Icon =  f'{_["Icon"]}  '
                else:
                    Icon = ''  
                print(f"\n{_fw}Server Name : {_reset}{Icon}{_fEx_b}{_['ServerName']}{_reset}")
                print(f"{_fw}IP          : {_fy}{_['IP']}{_reset}")
                print(f"{_fw}User        : {_fEx_b}{_['User']}{_reset}")
                print(f"{_fw}Port        : {_fEx_b}{_['Port']}{_reset}")
                print(f"{_fw}Group       : {_fEx_b}{_['Group']}{_reset}")
                TagsStr = ''
                for _t in _['Tags']:
                    TagsStr += f"{_fw}{_bb} {_t} {_reset} "
                print(f"{_fw}Tags        : {TagsStr}{_reset}")
            return _



def CreategroupList(GroupBy='Group'):
    GroupList = []
    for _Server in SERVER_LIST:
        if _Server["Group"] not in GroupList:
            GroupList.append(_Server["Group"])
    return GroupList

GROUP_LIST = CreategroupList()


if __name__ == "__main__":    
    print(f"You should not run this file directly")

