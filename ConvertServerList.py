import os
import lib.BaseFunction
import lib.Logo
import lib.AsciArt
import json
from core import current_directory
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

old_file_Name = 'ServerList.json'
New_File_Name = "ServerList-cnv.json"


OldPath = os.path.join(current_directory,f'conf/{old_file_Name}')
NewPath = os.path.join(current_directory,f'conf/{New_File_Name}')
OldServerListJson = lib.BaseFunction.LoadJsonFile(JsonFile=OldPath,Verbus=True,ReternValueForFileNotFound={})
if OldServerListJson == {}:
    lib.BaseFunction.FnExit(Msg="Error in load Source File")



def ServerCodeIsUniq(NewCode = '',ServerLIst= {}):
    for _group in ServerLIst:
        GroupDict = ServerLIst[_group]["servers"]
        for _s in GroupDict:
            if _s.strip().lower() == NewCode.lower().strip():
                return False
    return True



def ConverIt():
    Count = 0
    NewServerLIst = {}
    for OldserverDict in OldServerListJson['servers']:
        _Gruop  = OldserverDict.get('Group','DEFAULT').upper().strip()
        _Code   = OldserverDict.get('Code','')
        if _Code.strip() == '':
            return False, f"Code is Empty {OldserverDict['ServerName']}"
        elif ServerCodeIsUniq(NewCode=_Code,ServerLIst=NewServerLIst) is False:
            return False, f"Code is Not Uniq {_Code}"
        if _Gruop not in NewServerLIst:
            NewServerLIst[_Gruop] = {}
            NewServerLIst[_Gruop]['servers'] = {}            
            NewTags = []
            for _T in OldserverDict['Tags']:
                NewTags.append(_T.upper().strip())

        NewServerLIst[_Gruop]['servers'][_Code] = {}
        NewServerLIst[_Gruop]['servers'][_Code]['server_name'] = OldserverDict['ServerName']
        NewServerLIst[_Gruop]['servers'][_Code]['ip'] = OldserverDict['IP']

        NewServerLIst[_Gruop]['servers'][_Code]['port'] = OldserverDict['Port']
        NewServerLIst[_Gruop]['servers'][_Code]['user'] = OldserverDict['User']
        NewServerLIst[_Gruop]['servers'][_Code]['tags'] = NewTags
        NewServerLIst[_Gruop]['servers'][_Code]['icon'] = OldserverDict['Icon']
        NewServerLIst[_Gruop]['servers'][_Code]['authentication'] = ''
        Count += 1
    return True, NewServerLIst,Count



rst = ConverIt()
if rst[0]:
    if lib.BaseFunction.SaveJsonFile(JsonData=rst[1],JsonFile=NewPath,Verbus=True):
        print(f"File : [{NewPath}] Created Successfully\n Convert [ {rst[3]} ] Server Connection Successfully.")

else:
    print(rst[1])
    