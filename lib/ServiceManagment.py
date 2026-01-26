import copy
import lib.AsciArt
import lib.BaseFunction
import lib.Logo
#from tunnel import SERVICE_LIST,current_directory
import lib.ServiceManagmentCore
from core import current_directory
from lib.TunnelCore import SERVICE_LIST
from lib.ServiceManagmentCore import ServiceManager
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset
import lib.TunnelCore


manager = ServiceManager()

SERVICE_LIST = lib.TunnelCore.Generate_SERVICE_LIST()

RunModeStr = 'RunAsService'
def FnPrintListofService():        
    _ServiceListWithStatus = copy.deepcopy(SERVICE_LIST)
    Count = 0
    for _s in _ServiceListWithStatus:
        Count += 1
        ServiceDict = _ServiceListWithStatus[_s]   
        Name = ServiceDict.get('name',None)
        if Name is None:
            continue            
        PrntLst = FnPrintServiceDitails(ServiceDict=ServiceDict,Count=Count)
        print(PrntLst)
        #import json
        #print(json.dumps(_ServiceListWithStatus, indent=4))

def FnPrintServiceDitails(ServiceDict=None,Count=0):
    Name = ServiceDict.get('name',None)        
    _rst = manager.status_service(Name,ReturnLog=False,Verbus=False)        
    IsActive = _rst[0]
    _Status = _rst[1]
    ServiceDict['status'] = IsActive
    ServiceDict['active_state'] = _Status["active_state"].lower()
    ServiceDict['enabled_state'] = _Status["enabled_state"]
    ServiceDict['status_display'] = _Status["status_display"]
    ServiceDict['enabled_display'] = _Status["enabled_display"]
    active_state = ServiceDict['active_state']
    status = ServiceDict['status']
    if active_state.lower() == 'active':             
        _titelColor = f'{_bg}{_fbl}'
    else:
        _titelColor = f'{_bc}{_fbl}'
    if status:
        statusStr = f"{_by}{_fbl}  Running  {_reset}"
    else:
        statusStr = f"{_bbl}{_fw}  Stoped  {_reset}"
    if Count > 0:
        CountStr = f'{_by+_fbl} #{Count} {_reset}'
    else:
        CountStr = ''
    sp = ' ' * 20        
    FullExecPath = current_directory + '/' + ServiceDict['exec']
    WorkDir = ServiceDict.get("working_dir",current_directory)        
    MsgLineList = []
    MsgLineList.append(f"\n\n{_titelColor}Service Name      {_reset} : {CountStr}{_titelColor} {ServiceDict['name']}{sp}{_reset}\n\n")
    MsgLineList.append(f"Status:            : {statusStr}\n")
    MsgLineList.append(f"Description        : {_fc}{ServiceDict['description']}{_reset}\n")
    MsgLineList.append(f"Exececute          : {_fc}{ServiceDict['exec']}{_reset} {_D} {FullExecPath}{_reset}\n")
    MsgLineList.append(f"user               : {_fc}{ServiceDict['user']}{_reset}\n")
    MsgLineList.append(f"working dir        : {_fc}{WorkDir}{_reset}\n")
    MsgLineList.append(f"Service is         : {_fy}{ServiceDict['enabled_state']}{_reset} {_fw}( {ServiceDict['status_display']} ){_reset}\n")
    return ''.join(MsgLineList)
def ServiceDetails(ServiceDict= None,Msg = ''):
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        FullExecPath = current_directory + '/' + ServiceDict['exec'] + f' {RunModeStr}'
        WorkDir = ServiceDict.get("working_dir",current_directory)        

        if Msg != '':
            print("")
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fy)            
            Msg = ""

        PrntLst = FnPrintServiceDitails(ServiceDict=ServiceDict)
        print(PrntLst)

        print(f'\n{_fw}( {_fy}1 {_fw}) Create Service{_reset}')        
        print(f'{_fw}( {_fy}2 {_fw}) Install Service (reload daemon){_reset}')
        print(f'{_fw}( {_fy}3 {_fw}) Enable Service{_reset}')
        print(f'{_fw}( {_fy}4 {_fw}) Disable Service{_reset}')
        print(f'{_fw}( {_fc}5 {_fw}) Start Service{_reset}')
        print(f'{_fw}( {_fc}6 {_fw}) Stop Service{_reset}')
        print(f'{_fw}( {_fc}7 {_fw}) Restart Service{_reset}')
        print(f'{_fw}( {_fb}8 {_fw}) View Logs{_reset}')
        print(f'{_fw}( {_fr}9 {_fw}) Delete Service{_reset}')
        print(f'{_fw}( {_fb}0 {_fw}) Back to ...{_reset}')
        print(f'{_D}q for quit{_reset}')        
        UserInput = input(f"\n\n{_B}{_fw}Enter Command > ")        
        if UserInput.strip() == '':
            continue
        elif UserInput.strip() == '1':
                _res = manager.create_service(name=ServiceDict['name'],
                                                description=ServiceDict['description'],
                                                exec_start=FullExecPath,
                                                user=ServiceDict['user'],
                                                working_dir=WorkDir,
                                                verbus=False
                                                )
                if _res[0]:
                    lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
                else:
                    lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
                Msg = _res[1]
                lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '2':
            _res = manager.install_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '3':
            _res = manager.enable_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '4':
            _res = manager.disable_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '5':
            _res = manager.start_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '6':
            _res = manager.stop_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '7':
            _res = manager.restart_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '8':
            Logs = manager.get_log(name=ServiceDict['name'],lines=20)
            print(f'\n{_reset}{_fw}{"="* 50}{_D}{_fw}\n')
            print(Logs)
            print(f'\n{_reset}{_fw}{"="* 50}{_reset}')
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '9':
            _res = manager.delete_service(name=ServiceDict['name'],verbus=False)
            if _res[0]:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy)
            else:
                lib.AsciArt.BorderIt(Text=_res[1],BorderColor=_fy,TextColor=_fr)
            Msg = _res[1]
            lib.BaseFunction.PressEnterToContinue()
        elif UserInput.strip() == '0':
            return

if __name__ == "__main__":
        print(f"You should not run this file directly")
