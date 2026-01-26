#! /usr/bin/python3
import lib.BaseFunction
import lib.Logo
import lib.AsciArt
import lib.ServiceManagment
import os
import signal
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset
from lib.TunnelCore import SERVICE_LIST
from core import current_directory,LOG_PATH,SSHKEY,JsonConfigFile,JsonConfig
from passlib.context import CryptContext
###

TelegramJsonFile = os.path.join(current_directory,"conf/Telegram.json")
TelegramJsonConfig = lib.BaseFunction.LoadJsonFile(TelegramJsonFile,Verbus=True)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def Configuration_Menu(msg = ""):
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        if msg != '':
            print("")
            lib.AsciArt.BorderIt(BorderColor=_fy,Text=f'{msg}')
            #lib.BaseFunction.PressEnterToContinue()
            msg = ''
        
        print(f'\n{_fw}( {_fb}1 {_fw}) Services Configuration{_reset}')        
        print(f'{_fw}( {_fb}2 {_fw}) API Configuration{_reset}')        
        print(f'{_fw}( {_fb}3 {_fw}) Telegram Configuration{_reset}')        
        print(f'{_fw}( {_fb}0 {_fw}) Back  to ...{_reset}')        
        print(f'\n{_D}q for quit{_reset}')        
        UserInput = input(f'{_B}{_fw}Enter Command >  {_reset}')        
        if UserInput.lower().strip() == '1':
            ServiceManagmentMenu()
        elif UserInput.lower().strip() == '2':
            ApiConfigurationMenu()
        elif UserInput.lower().strip() == '3':
            TelegramBotConfigurationMenu()
        elif UserInput.lower().strip() == '0':
            return
        elif UserInput.lower().strip() == 'q':
            lib.BaseFunction.FnExit()
        else:
            if UserInput.strip() != '':
                msg  = "Command not Valid"

def ServiceManagmentMenu():
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()        
        lib.ServiceManagment.FnPrintListofService()
        
        #print(f'{_fw}( {_fb}d {_fw}) Drop all Tunnel{_reset}')
        #print(f'{_fw}( {_fb}r {_fw}) Restart all Tunnel{_reset}')            
        print(f'{_D}0 for Back{_reset}')        
        print(f'{_D}q for quit{_reset}')                
        UserInput = input(f"\n\n{_B}{_fw}Select Service > {_reset}")
        if UserInput.strip == '':
            continue
        elif UserInput.lower() == '0':
            return
        elif UserInput.lower() == 'q':
            lib.BaseFunction.FnExit()
        else:            
            count = 1
            try:
                UserInput = int(UserInput)
            except:
                pass                        
            for _s in SERVICE_LIST:
                ServiceDict = SERVICE_LIST[_s]
                if type(UserInput) == int:
                    if UserInput == count:
                        lib.ServiceManagment.ServiceDetails(ServiceDict=ServiceDict)                        
                else:
                    if _s.lower().strip() == UserInput.lower().strip():
                        lib.ServiceManagment.ServiceDetails(ServiceDict=ServiceDict)                        
                count += 1        


def TelegramBotConfigurationMenu():
    Msg = ''
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        if Msg not in ['',None]:
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fc,TextColor=_fy)
            Msg = ''
        MenuList = []
        MenuList.append("Add / Update Bot Token")
        MenuList.append("Add / Update Admin User")
        UserInput = lib.AsciArt.GenerateMenu(MenuList=MenuList,SeletedColor=_fc,Titel='Telegram Configuration ...')        
        if UserInput.strip() == '':
            continue
        elif UserInput.strip() == '1':
            Msg = Fn_ChangeBotToken()
        elif UserInput.strip() == '2':
            Msg = Fn_UpdateTelegramUser()
        elif UserInput.strip() == 'b':
            return 
        elif UserInput.strip() == 'q':
            lib.BaseFunction.FnExit()

def ApiConfigurationMenu():
    Msg = ''
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        if Msg not in ['',None]:
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fc,TextColor=_fy)
            Msg = ''
        print("")
        print(_fw + '-' * 45)
        print(_fw + '-' * 7 +  '> API Configuration')
        print(_fw + '-' * 45)
        print(f'\n{_fw}( {_fb}1 {_fw}) Change Api Secrets key{_reset}')        
        print(f'{_fw}( {_fb}2 {_fw}) Rest Password{_reset}')        
        print(f'{_fw}( {_fb}3 {_fw}) Publish port{_reset}')        
        print(f'{_fw}( {_fb}4 {_fw}) Publish on Localhost{_reset}')        
        print(f'{_fw}( {_fb}0 {_fw}) Back to ... {_reset}')        
        print(f'\n{_D}q for quit{_reset}')        
        UserInput = input(f'{_B}{_fw}Enter Command >  {_reset}')
        if UserInput.strip() == '':
            continue
        elif UserInput.strip() == '1':
            Msg = Fn_ChangeApiSecretKey()
        elif UserInput.strip() == '2':
            Msg = Fn_ResetUserPassword()
        elif UserInput.strip() == '3':
            Msg = Fn_ChangeApiPort()
        elif UserInput.strip() == '4':
            Msg = Fn_ChangHost()
        elif UserInput.strip() == '0':
            return 


def Fn_ResetUserPassword():
    UserInput = ''
    PasswordInput = ''
    HashedPassword = ''
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()        
        print(f"\n{_fw}User : {_fy}{UserInput}{_reset}")
        print(f"{_fw}password : {_fy}{PasswordInput} {_fw}[ {_D}{HashedPassword}{_reset}{_fw} ]{_reset}")
        if UserInput == '':
            OldUser = JsonConfig.get('api_config',{}).get("user",'root')
            print(f'\n{_D}0 for back{_reset}')
            print(f'{_D}q for quit{_reset}')
            UserInput = input(f"{_B + _fw}Enter username / Press enter for [ {_fc}{OldUser}{_fw} ] > {_reset}")
            if UserInput.strip() == '':
                UserInput = OldUser
            elif UserInput.strip() == '0':
                return ''
            elif UserInput.strip().lower() == 'q':
                lib.BaseFunction.FnExit()
            continue
        if PasswordInput == '':
            print(f'\n{_D}0 for back{_reset}')
            print(f'{_D}q for quit{_reset}')
            PasswordInput = input(f"{_B + _fw}Enter Password > {_reset}")
            if PasswordInput.strip() == '':
                continue
            elif PasswordInput.strip().lower() == 'q':
                lib.BaseFunction.FnExit()
            elif PasswordInput.strip().lower() == '0':
                return ''
            else:
                HashedPassword = get_password_hash(PasswordInput)                
            continue
        else:            
            if FnConfirmChange(MsgStr='Are You sure save New User & password ?'):
                JsonConfig['api_config']["user"] = UserInput
                JsonConfig['api_config']["password"] = HashedPassword
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=JsonConfigFile ,JsonData=JsonConfig,Verbus=False)
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                if _Rst[0]:
                    Msg = "Reset Password sucs...."
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'User & Password Changed'
            else:
                Msg = f"Error in save key [{_Rst[1]}]"
                lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                lib.BaseFunction.PressEnterToContinue()            
                return 'Error in key change'

def Fn_UpdateTelegramUser():
    UserAdmin = TelegramJsonConfig.get('primession',{}).get('admin',[])    
    Msg = ""
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()            
        print(f'\n{_D}b for back{_reset}')
        print(f'{_D}q for quit{_reset}')
        UserInput = input(f'{_B}{_fw}Enter Telegram User ID >{_reset}')        
        
        if UserInput.strip == "":
            continue
        elif UserInput.lower() == 'b':
            return ''
        elif len(UserInput) < 9:
            Msg = "Telegram User Id is Not Valid"            
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
            lib.BaseFunction.PressEnterToContinue()        
            continue
        else:
            try:
                _userDigit = int(UserInput)
            except:
                Msg = "Telegram User Id is Not Valid"            
                lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                lib.BaseFunction.PressEnterToContinue()        
                continue
            if FnConfirmChange():
                TelegramJsonConfig['primession']['admin'] = [UserInput]
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=TelegramJsonFile ,JsonData=TelegramJsonConfig,Verbus=False)
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                if _Rst[0]:
                    Msg = "Update Telegram User Id"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'telegram UserId updated'
                else:
                    Msg = f"Error in save key [{_Rst[1]}]"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Error in update telegram Use ID'            

def Fn_ChangeBotToken():
    BotToken = TelegramJsonConfig.get('bot_token','')
    Msg = ""
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()            
        print(f'\n{_D}b for back{_reset}')
        print(f'{_D}q for quit{_reset}')
        UserInput = input(f'{_B}{_fw}Enter Bot Token Telegram >{_reset}')        
        if UserInput.strip == "":
            continue
        elif UserInput.lower() == 'b':
            return ''
        elif len(UserInput) < 40:
            Msg = "Telegram Bot token Must less than 40 charachter"            
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
            lib.BaseFunction.PressEnterToContinue()
        else:
            if FnConfirmChange():
                TelegramJsonConfig['bot_token'] = UserInput
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=TelegramJsonFile ,JsonData=TelegramJsonConfig,Verbus=False)
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                if _Rst[0]:
                    Msg = "Update Bot token"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'telegram Bot token updated'
                else:
                    Msg = f"Error in save key [{_Rst[1]}]"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Error in update telegram bot token'            

        

    
def Fn_ChangHost():
    PublishOnLocalhost = JsonConfig.get('api_config',{}).get('publish_on_localhost',True)    
    while True:
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        print(f'\n{_D}0 for back{_reset}')
        print(f'{_D}q for quit{_reset}')
        if PublishOnLocalhost:
            print(f'\n{_fw}API Service Publish on  [ {_fc}LocalHost{_fw}]{_reset}')
            PortInput = input(f'{_B + _fw}Change to {_fy}ExternalIP{_fw} [ Y / N ] >{_reset}')
            NewValue = False
        else:
            print(f'{_B + _fw}API Service Publish on  [ {_fc}External IP{_fw}]{_reset}')
            PortInput = input(f'{_B + _fw}Change to {_fy}localhost{_fw} [ Y / N ]{_reset}')
            NewValue = True
        
        if PortInput == "":
            continue
        elif PortInput.lower().strip() in ['y','yes']:
            if FnConfirmChange():
                JsonConfig['api_config']["publish_on_localhost"] = NewValue
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=JsonConfigFile ,JsonData=JsonConfig,Verbus=False)
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                if _Rst[0]:
                    Msg = "Change Publish Adress"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Publish Adress Changed'
                else:
                    Msg = f"Error in save key [{_Rst[1]}]"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Error in change Publish in'
        elif PortInput.lower().strip() in ['n','no']:
            return ''
        else:
            continue
        




def Fn_ChangeApiPort():
    PublishedPort = JsonConfig.get('api_config',{}).get('publish_port',8000)
    while True:        
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()
        print(f'{_D}0 for back{_reset}')
        print(f'{_D}q for quit{_reset}')
        PortInput = input(f'{_B + _fw}Enter port [ {_fc}{PublishedPort} {_fw}] > {_reset}')
        if PortInput.strip() == '':
            return ''
        else:
            Msg = ''
            try:
                PortInput = int(PortInput.strip())
                if PortInput < 1 or PortInput > 65535:
                    Msg = "Invalid port number. Please enter a value between 1 and 65535"
            except:
                    Msg = "Invalid port number. Please enter a numeric value"
            if Msg != '':
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                lib.BaseFunction.PressEnterToContinue()
                Msg = ''
                continue
        if type(PortInput) == int:
            
            if FnConfirmChange(MsgStr='Are You sure to change Port'):
                JsonConfig['api_config']["publish_port"] = PortInput
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=JsonConfigFile ,JsonData=JsonConfig,Verbus=False)
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                if _Rst[0]:
                    Msg = "Change port sucs...."
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Port Changed'
                else:
                    Msg = f"Error in save key [{_Rst[1]}]"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Error in port change'
            else:
                return
                



def FnConfirmChange(MsgStr = "Are You Sure ?"):            
    while True:
        print(f'\n{_D}0 for back{_reset}')
        print(f'{_D}q for quit{_reset}')
        SaveInput = input(f'{_B}{_fw}{MsgStr} [ {_bg} YES {_reset}{_B + _fw} / {_br} NO {_reset}{_B + _fw} ] >{_reset}')
        if SaveInput.strip() == '':
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()
            print("")
        elif SaveInput.lower() in ['0','n','no']:
            return False
        elif SaveInput.lower() == 'q':
            lib.BaseFunction.FnExit()
        elif SaveInput.lower() in ['y','yes']:
            return True



def get_password_hash(password):
    return pwd_context.hash(password)


def Fn_ChangeApiSecretKey():    
    while True:        
        lib.BaseFunction.clearScreen()
        lib.Logo.sshTunnel()        
        lib.AsciArt.BorderIt(Text="Warning: Change secret key",BorderColor=_fr,TextColor=_fy,)
        print(f'{_D}0 for back{_reset}')
        print(f'{_D}q for quit{_reset}')
        UserKeyInput = input(f"{_B + _fw}Enter New Key > ")
        if UserKeyInput.strip() == '':
            continue
        elif UserKeyInput.lower().strip() == 'q':
            lib.BaseFunction.FnExit()
        elif UserKeyInput.strip() == '0':
            return ''
        elif len(UserKeyInput) < 10 :
            Msg = "Key is low"
            lib.BaseFunction.clearScreen()
            lib.Logo.sshTunnel()                
            lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
            lib.BaseFunction.PressEnterToContinue()
        else:
            if FnConfirmChange(MsgStr="Are you Shure change Key ?"):
                JsonConfig['api_config']["api_secret_key"] = UserKeyInput
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=JsonConfigFile ,JsonData=JsonConfig,Verbus=False)
                lib.BaseFunction.clearScreen()
                lib.Logo.sshTunnel()                
                if _Rst[0]:
                    Msg = "Secret Key Change"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fg,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'secret key is changed'
                else:
                    Msg = f"Error in save key [{_Rst[1]}]"
                    lib.AsciArt.BorderIt(Text=Msg,BorderColor=_fr,TextColor=_fy)
                    lib.BaseFunction.PressEnterToContinue()            
                    return 'Error in key change'       
            else:
                return



signal.signal(signal.SIGINT, lib.BaseFunction.handler)

if __name__ == "__main__":
    Configuration_Menu()