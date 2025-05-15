import lib.BaseFunction
import lib.AsciArt
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset
import art
#########################
##########################


def SshToolsLogo():
    print (f"{_fy}┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐{_reset}")
    print (f"{_fy}│ ──{_fb}╔═══╦═══╦╗{_fy}─{_fb}╔╗╔════╗{_fy}────{_fb}╔╗{_fy}─────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╔═╗║╔═╗║║{_fy}─{_fb}║║║╔╗╔╗║{_fy}────{_fb}║║{_fy}─────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╚══╣╚══╣╚═╝║╚╝║║╠╩═╦══╣║╔══╗{_fy}─────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}╚══╗╠══╗║╔═╗║{_fy}──{_fb}║║║╔╗║╔╗║║║══╣{_fy}─────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╚═╝║╚═╝║║{_fy}─{_fb}║║{_fy}──{_fb}║║║╚╝║╚╝║╚╬══║{_fy}─────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}╚═══╩═══╩╝{_fy}─{_fb}╚╝{_fy}──{_fb}╚╝╚══╩══╩═╩══╝{_fy}─────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}└────────────────────────────────────────────────────────────────────────────────────────────────────────┘{_reset}")
    
def SshToolsLogoScp():
    print (f"{_fy}┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐{_reset}")
    print (f"{_fy}│ ──{_fb}╔═══╦═══╦╗{_fy}─{_fb}╔╗╔════╗{_fy}────{_fb}╔╗{_fy}──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╔═╗║╔═╗║║{_fy}─{_fb}║║║╔╗╔╗║{_fy}────{_fb}║║{_fy}──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╚══╣╚══╣╚═╝║╚╝║║╠╩═╦══╣║╔══╗{_fy}──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}╚══╗╠══╗║╔═╗║{_fy}──{_fb}║║║╔╗║╔╗║║║══╣{_fy}──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╚═╝║╚═╝║║{_fy}─{_fb}║║{_fy}──{_fb}║║║╚╝║╚╝║╚╬══║{_fy}──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}╚═══╩═══╩╝{_fy}─{_fb}╚╝{_fy}──{_fb}╚╝╚══╩══╩═╩══╝{_fy}──────────────────────────────────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘{_reset}")
    

def SshTunnelLogo():
    print (f"{_fy}┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐{_reset}")
    print (f"{_fy}│ ──{_fb}╔═══╦═══╦╗{_fy}─{_fb}╔╗╔════╗{_fy}────{_fb}╔╗{_fy}─────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╔═╗║╔═╗║║{_fy}─{_fb}║║║╔╗╔╗║{_fy}────{_fb}║║{_fy}─────────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╚══╣╚══╣╚═╝║╚╝║║╠╩═╦══╣║╔══╗{_fy}─────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}╚══╗╠══╗║╔═╗║{_fy}──{_fb}║║║╔╗║╔╗║║║══╣{_fy}─────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}║╚═╝║╚═╝║║{_fy}─{_fb}║║{_fy}──{_fb}║║║╚╝║╚╝║╚╬══║{_fy}─────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}│ ──{_fb}╚═══╩═══╩╝{_fy}─{_fb}╚╝{_fy}──{_fb}╚╝╚══╩══╩═╩══╝{_fy}─────────────────────────────────────────────────────────────────────────────── │{_reset}")
    print (f"{_fy}└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘{_reset}")


#def TunnleProgress(SourceAddr,DestPort,Mode):
    

def ScpProgress(SourceLst,destinationLst,SourcePath,DestPath,mode):
    _clearClr = f'{_fbl}{_bw}'
    _SrcClr = f'{_fbl}{_bg}'
    _DstClr = f'{_fbl}{_bc}'
    _BColor = f'{_fy}'
    _SourceIP = lib.BaseFunction.GetValue(SourceLst,"IP",verbus=False,ReturnValueForNone='')
    _DestIP = lib.BaseFunction.GetValue(destinationLst,"IP",verbus=False,ReturnValueForNone='')

    _SourceIP_Label = f'{_clearClr}{lib.AsciArt.FnAlignmentStr(originalString="From",target_length=20)}{_reset}'
    _DestIP_Label = f'{_clearClr}{lib.AsciArt.FnAlignmentStr(originalString="To",target_length=20)}{_reset}'
    _SourceFile_Label = f'{_clearClr}{lib.AsciArt.FnAlignmentStr(originalString="File Name",target_length=46)}{_reset}'
    _DestFile_Label = f'{_clearClr}{lib.AsciArt.FnAlignmentStr(originalString=" Destination Path",target_length=46)}{_reset}'
        
    if _SourceIP != '':        
        _SourceIP_Label = f'{_SrcClr}{lib.AsciArt.FnAlignmentStr(originalString=_SourceIP,target_length=20)}{_reset}'         
    if SourcePath != '':
        _SourceFile_Label = f'{_SrcClr}{lib.AsciArt.FnAlignmentStr(originalString=SourcePath,target_length=46)}{_reset}'
        
    if _DestIP != '':        
        _DestIP_Label = f'{_DstClr}{lib.AsciArt.FnAlignmentStr(originalString=_DestIP,target_length=20)}{_reset}'
    if DestPath != '':
        _DestFile_Label = f'{_DstClr}{lib.AsciArt.FnAlignmentStr(originalString=DestPath,target_length=46)}{_reset}'
    
    LableStr = f'{_SourceIP_Label} / {_SourceFile_Label} --> {_DestIP_Label} / {_DestFile_Label}'
    
    _SourceIP_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString=" ",target_length=20)}{_reset}'
    _DestIP_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString=" ",target_length=20)}{_reset}'
    _SourceFile_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString=" ",target_length=46)}{_reset}'
    _DestFile_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString=" ",target_length=46)}{_reset}'
    

    if mode == 'from':
        _SourceIP_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString="⬇️  ⬇️  ⬇️",target_length=20)}{_reset}'
    elif mode == 'sfile':
        _SourceFile_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString="⬇️  ⬇️  ⬇️",target_length=46)}{_reset}'
    elif mode == 'to':
        _DestIP_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString="⬇️  ⬇️  ⬇️",target_length=20)}{_reset}'
    elif mode == 'dfile':
        _DestFile_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString="⬇️  ⬇️  ⬇️",target_length=46)}{_reset}'
    elif mode == 'both':
        _SourceIP_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString="⬇️  ⬇️  ⬇️",target_length=21)}{_reset}'
        _SourceFile_GUID = f'{_reset}{lib.AsciArt.FnAlignmentStr(originalString="⬇️  ⬇️  ⬇️",target_length=48)}{_reset}'    
        
    Guideline = f'{_SourceIP_GUID}   {_SourceFile_GUID}      {_DestIP_GUID}     {_DestFile_GUID}'
    if mode == 'confirm':
        Guideline = f"{_B}{_by}{_fbl}{lib.AsciArt.FnAlignmentStr(originalString='are you sure ?',target_length=143)}{_reset}"
        
    spaceline = lib.AsciArt.FnAlignmentStr(originalString=" ",target_length=145)
    #lib.AsciArt.BorderIt(Text=LableStr,WidthBorder=150)
    LineUp = '┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'
    LineDown = '└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘'
    print(f'{_BColor}{LineUp}{_reset}')
    if mode != '':
        print(f'{_BColor}│ {Guideline} {_BColor}│{_reset}')
        print(f'{_BColor}│{spaceline}{_BColor}│{_reset}')
    print(f'{_BColor}│{_reset} {LableStr} {_BColor}│{_reset}')
    print(f'{_BColor}{LineDown}{_reset}')

#def TunnelProgress()
#
#SourceLst,destinationLst,SourcePath,DestPath,mode


def sshTunnel(Mode=1):
    if Mode == 1:
        print(f'{_D}{_fc} _____ _____ _____    _____                 _ {_reset}')
        print(f'{_D}{_fc}|   __|   __|  |  |  |_   _|_ _ ___ ___ ___| |{_reset}')
        print(f'{_N}{_fc}|__   |__   |     |    | | | | |   |   | -_| |{_reset}')
        print(f'{_B}{_fc}|_____|_____|__|__|    |_| |___|_|_|_|_|___|_|{_reset}')

def ArtText(Text = "",Font = "",color = _fw):
    if Font == "":
        Font = 'stampate'
    TText = art.text2art(text=Text,font=Font)
    print(f'{color}{TText}{_reset}')
    
    

if __name__ == "__main__":   
    print(f"{_B}{_fy}You should not run this file directly")


