import color.Back as Back
import color.Fore as Fore
import color.Style as Style
import art
from color.Style import _B,_D,_N,_reset
from color.Back import _bw,_by,_bb,_bbl,_br,_bc,_bg,_bm,_brst,_bEx_w,_bEx_y,_bEx_b,_bEx_bl,_bEx_r ,_bEx_c ,_bEx_g ,_bEx_m ,_b_rest
from color.Fore import _fw,_fy,_fb,_fbl,_fr,_fc,_fg,_fm,_fEx_w,_fEx_y,_fEx_b,_fEx_bl,_fEx_r,_fEx_c,_fEx_g,_fEx_m,_f_reset

LIST_OF_EMOJI = ['🇮🇷','🇬🇧','🇷🇺','🇩🇪','🇺🇸','🏁','🇨🇳','🕛','🟦','🟩','🟨','🟧','🟥','⬜',
                '😤','❌','✅','🚫','♻️','✏️','🙁','🔌','📍','⚙️','🚀','⏹️','🔰','➕',
                '🗑️','💡','🔒','🔐','🔑','↗️','🔄','👤','🌐','🏠','🖥️','⚠️','🛰️','⚡']


ClockIconList = ['🕛','🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚']
def FnAlignmentStr(originalString: str, target_length: int, padding_char: str = " ",AlignmentMode = "center") -> str:
    """اضافه کردن و بزرگ کردن رشته دریافتی و برگشت آن به طول درخواستی

    Args:
        originalString (str): متن اصلی
        target_length (int): طول رشته نهایی
        padding_char (str, optional): عبارتی که افزایش طول عبارت با آن صورت پذیرد
        AlignmentMode (str, optional): مارجین متن در عبارت

    Returns:
        str: _description_
    """
    if len(originalString) >= target_length:
        return originalString 
        
    total_padding = target_length - len(originalString)
    if AlignmentMode not in ['center','left','right']:
        Aligment = 'left'
    if AlignmentMode.lower() == 'center':        
        left_padding = total_padding // 2
        right_padding = total_padding - left_padding
        _str =  padding_char * left_padding + originalString + padding_char * right_padding
    elif AlignmentMode.lower() == 'left':
        total_padding = total_padding - 1
        _str = padding_char + originalString + padding_char * total_padding
    elif AlignmentMode.lower() == 'right':
        total_padding = total_padding - 1
        _tr = padding_char * total_padding + originalString + padding_char
    return _str

def wrap_text(text, max_width=100):
    """
    Wraps the given text to a specified maximum width.

    Args:
        text: The input text to be wrapped.
        max_width: The maximum width of each line.

    Returns:
        A list of lines, where each line has a maximum width of max_width.
    """

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > max_width:  # Add 1 for the space
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line += word + " "
    
    if current_line.strip():
        lines.append(current_line.strip())
    return lines



def BorderIt(Text:str,BorderColor = '',TextColor = '', WidthBorder = 100):
    """ Create a Border in Text
    Args:
        Text (str): Input text
        BorderColor (str, optional): Border Color_. Defaults to 'WHITE'.
        TextColor (str, optional): TextColor. Defaults to 'WHITE'.
        WidthBorder (int, optional): Width of Box. Defaults to 100.
    """
    if TextColor == '':
        TextColor = Fore.WHITE
    if BorderColor == '':
        BorderColor = Fore.WHITE

    LenStr = len(Text) + 2
    if LenStr > WidthBorder:
        LenStr = WidthBorder         
    RowLine = '─' * LenStr
    Upline = BorderColor + f'┌{RowLine}┐' + Style.RESET_ALL
    Dwonline = BorderColor + f'└{RowLine}┘' + Style.RESET_ALL
    ClmnChar = f'{BorderColor}│{Style.RESET_ALL}'
    lines = wrap_text(text=Text,max_width=WidthBorder - 1)
    print("")
    print(Upline)
    for line in lines:
        if LenStr == WidthBorder:
            aa = len(line)
            a = WidthBorder - len(line) - 1
            space_al = ' ' * a
        else:
            space_al = ' '    
        print(f'{ClmnChar} {TextColor}{line}{space_al}{ClmnChar}')
    print(Dwonline)
    print("")

def ArtText(Text = "",Font = "",color = Fore.WHITE,PrintIt = True):
    FontList = ['straight',
                'stop',
                'standard',
                'stampate',
                'shimrod',
                'santaclara',
                'rounded',
                'rectangles',
                'rammstein',
                'ogre',
                ]
    if Font == "":
        Font = 'standard'
    TText = art.text2art(text=Text,font=Font)        
    if PrintIt:    
        print(f'{color}{TText}{Style.RESET_ALL}')
    else:
        return TText
    


def TestFont(Text = '',color = Fore.WHITE):
    FontList = ['straight',
                'stop',
                'standard',
                'stampate',
                'shimrod',
                'santaclara',
                'rounded',
                'rectangles',
                'rammstein',
                'ogre',
                'smisome1',
                'cyberlarge',
                'cybermedium',
                'larry3d',
                'merlin1',
                ]
    for Font in FontList:        
        TText = art.text2art(text=Text,font=Font)
        print("")
        print(f'{color}{TText}{Style.RESET_ALL}')
        print("")

def GenerateBarGraph(length = 10,UsedPercent = 20,UseEmoji = True):
    if isinstance(UsedPercent,str):
        if UsedPercent.endswith('%'):
            UsedPercent = UsedPercent[:-1]
        try:
            UsedPercent = float(UsedPercent)
        except:
            UsedPercent = 0

    if UseEmoji:
        if UsedPercent <= 30:
            if length >= 10:
                if UsedPercent < 10:
                    #UsedPercent = 10
                    Used_char = '🟦'
                else:
                    Used_char = '🟩'                        
            else:    
                Used_char = '🟩'
        elif UsedPercent <=60:
            Used_char = '🟨'
        elif UsedPercent <= 80:
            Used_char = '🟧'
        else:
            Used_char = '🟥'

        Unused_char = '⬜'
    else:
        Used_char = '█'
        Unused_char = '░'    
    filled = int(length * UsedPercent / 100)
    RamBar = Used_char * filled + Unused_char * (length - filled)
    return RamBar


def GetCountryNameFromCode(CountryCode:str = ''):
    CountryDict = {
        'RNX': {
            'name':'🏢 Ronix Company 🏢',
            'emoji':'🏁'
        },
        'Invalid': {
            'name':'Invalid Country',
            'emoji':'🏴'
        },
        'US': {
            'name':'United States',
            'emoji':'🇺🇸'
        },
        'IR': {
            'name':'Iran',
            'emoji':'🇮🇷'
        },
        'IN': {
            'name':'India',
            'emoji':'🇮🇳'
        },
        'CN': {
            'name':'China',
            'emoji':'🇨🇳'
        },
        'RU': {
            'name':'Russia',
            'emoji':'🇷🇺'
        }, 
        'DE': {
            'name':'Germany',
            'emoji':'🇩🇪'
        },
        'FR': {
            'name':'France',
            'emoji':'🇫🇷'
        },
        'GB': {
            'name':'United Kingdom',
            'emoji':'🇬🇧'
        },
        'JP': {
            'name':'Japan',
            'emoji':'🇯🇵'
        },
        'CA': {
            'name':'Canada',
            'emoji':'🇨🇦'
        },
        'UA': {
            'name':'Ukraine',
            'emoji':'🇺🇦'
        },
        'BD': {
            'name':'Bangladesh',
            'emoji':'🇧🇩'
        },
        'PK': {
            'name':'Pakistan',
            'emoji':'🇵🇰'
        },
        'NK': {
            'name':'North Korea',
            'emoji':'🇰🇵'
        },
        'NL': {
            'name':'Netherlands',
            'emoji':'🇳🇱'
        },
        'CY': {
            'name':'Cyprus',
            'emoji':'🇨🇾'
        },
        'IT': {
            'name':'Italy',
            'emoji':'🇮🇹'
        },
        'SG': {
            'name':'Singapore',
            'emoji':'🇸🇬'
        },
        'AU': {
            'name':'Australia',
            'emoji':'🇦🇺'
        },
        'GE': {
            'name':'Georgia',
            'emoji':'🇬🇪'
        },
        'ZA': {
            'name':'South Africa',
            'emoji':'🇿🇦'
        },
        'ID': {
            'name':'Indonesia',
            'emoji':'🇮🇩'
        },
        'TR': {
            'name':'Turkey',
            'emoji':'🇹🇷'
        },
        'IE': {
            'name':'Ireland',
            'emoji':'🇮🇪'
        },
        'KR': {
            'name':'South Korea',
            'emoji':'🇰🇷'
        },
        'MM': {
            'name':'Myanmar',
            'emoji':'🇲🇲'
        },
        'ES': {
            'name':'Spain',
            'emoji':'🇪🇸'
        },
        'PH': {
            'name':'Philippines',
            'emoji':'🇵🇭'
        },
        'SA': {
            'name':'Saudi Arabia',
            'emoji':'🇸🇦'
        },
        'OM': {
            'name':'Oman',
            'emoji':'🇴🇲'
        },
        'AE': {
            'name':'United Arab Emirates',
            'emoji':'🇦🇪'
        },
        'MU': {
            'name':'Mauritius',
            'emoji':'🇲🇺'
        },
        'QA': {
            'name':'Qatar',
            'emoji':'🇶🇦'
        },
        'HK': {
            'name':'Hong Kong',
            'emoji':'🇭🇰'
        },
        'MG': {
            'name':'Madagascar',
            'emoji':'🇲🇬'
        },
        'CH': {
            'name':'Switzerland',
            'emoji':'🇨🇭'
        },
        'KZ': {
            'name':'Kazakhstan',
            'emoji':'🇰🇿'
        },
        'LB': {
            'name':'Lebanon',
            'emoji':'🇱🇧'
        },
        'EG': {
            'name':'Egypt',
            'emoji':'🇪🇬'
        },
        'CL': {
            'name':'Chile',
            'emoji':'🇨🇱'
        },
        'LY': {
            'name':'Libya',
            'emoji':'🇱🇾'
        },
        'CG': {
            'name':'Congo',
            'emoji':'🇨🇬'
        },
        'BY': {
            'name':'Belarus',
            'emoji':'🇧🇾'
        },
        'LK': {
            'name':'Sri Lanka',
            'emoji':'🇱🇰'
        },
        'BR': {
            'name':'Brazil',
            'emoji':'🇧🇷'
        },
        'RS': {
            'name':'Serbia',
            'emoji':'🇷🇸'
        },
        'IQ': {
            'name':'Iraq',
            'emoji':'🇮🇶'
        },
        'JQ': {
            'name':'Jordan',
            'emoji':'🇯🇴'
        },
        'PT': {
            'name':'Portugal',
            'emoji':'🇵🇹'
        },
        'TH': {
            'name':'Thailand',
            'emoji':'🇹🇭'
        },
        'AZ': {
            'name':'Azerbaijan',
            'emoji':'🇦🇿'
        },
        'CZ': {
            'name':'Czech Republic',
            'emoji':'🇨🇿'
        },
        'PL': {
            'name':'Poland',
            'emoji':'🇵🇱'
        },
        'SE': {
            'name':'Sweden',
            'emoji':'🇸🇪'
        },
        'NO': {
            'name':'Norway',
            'emoji':'🇳🇴'
        },
        'FI': {
            'name':'Finland',
            'emoji':'🇫🇮'
        },
        'DK': {
            'name':'Denmark',
            'emoji':'🇩🇰'
        },
        'GR': {
            'name':'Greece',
            'emoji':'🇬🇷'
        },
        'HU': {
            'name':'Hungary',
            'emoji':'🇭🇺'
        },
        'RO': {
            'name':'Romania',
            'emoji':'🇷🇴'
        },
        'BG': {
            'name':'Bulgaria',
            'emoji':'🇧🇬'
        },
        'HR': {
            'name':'Croatia',
            'emoji':'🇭🇷'
        },
        'SK': {
            'name':'Slovakia',
            'emoji':'🇸🇰'
        },
        'SI': {
            'name':'Slovenia',
            'emoji':'🇸🇮'
        },
        'LT': {
            'name':'Lithuania',
            'emoji':'🇱🇹'
        },
        'LV': {
            'name':'Latvia',
            'emoji':'🇱🇻'
        },
        'EE': {
            'name':'Estonia',
            'emoji':'🇪🇪'
        },
        'VN': {
            'name':'Vietnam',
            'emoji':'🇻🇳'
        },
        'AM': {
            'name':'Armenia',
            'emoji':'🇦🇲'
        },
        'TN': {
            'name':'Tunisia',
            'emoji':'🇹🇳'
        },
        'DZ': {
            'name':'Algeria',
            'emoji':'🇩🇿'
        },
        'MA': {
            'name':'Morocco',
            'emoji':'🇲🇦'
        },
        'GH': {
            'name':'Ghana',
            'emoji':'🇬🇭'
        },
        'KE': {
            'name':'Kenya',
            'emoji':'🇰🇪'
        },
        'NG': {
            'name':'Nigeria',
            'emoji':'🇳🇬'
        },
        'TZ': {
            'name':'Tanzania',
            'emoji':'🇹🇿'
        },
        'UG': {
            'name':'Uganda',
            'emoji':'🇺🇬'
        },
        'SN': {
            'name':'Senegal',
            'emoji':'🇸🇳'
        },
        'CI': {
            'name':'Côte d’Ivoire',
            'emoji':'🇨🇮'
        },
        'CM': {
            'name':'Cameroon',
            'emoji':'🇨🇲'
        },
        'ZW': {
            'name':'Zimbabwe',
            'emoji':'🇿🇼'
        },
        'NZ': {
            'name':'New Zealand',
            'emoji':'🇳🇿'
        },
        'MX': {
            'name':'Mexico',
            'emoji':'🇲🇽'
        },
        'AR': {
            'name':'Argentina',
            'emoji':'🇦🇷'
        },
        'CO': {
            'name':'Colombia',
            'emoji':'🇨🇴'
        },
        'PE': {
            'name':'Peru',
            'emoji':'🇵🇪'
        },
        'VE': {
            'name':'Venezuela',
            'emoji':'🇻🇪'
        },
        'EC': {
            'name':'Ecuador',
            'emoji':'🇪🇨'
        },
        'UY': {
            'name':'Uruguay',
            'emoji':'🇺🇾'
        },
        'PY': {
            'name':'Paraguay',
            'emoji':'🇵🇾'
        },
        'BO': {
            'name':'Bolivia',
            'emoji':'🇧🇴'
        },
        'XK': {
            'name':'Kosovo',
            'emoji':'🇽🇰'
        },
        'ET': {
            'name':'Ethiopia',
            'emoji':'🇪🇹'
        },
        'SD': {
            'name':'Sudan',
            'emoji':'🇸🇩'
        },
        'ML': {
            'name':'Mali',
            'emoji':'🇲🇱'
        },
        'BF': {
            'name':'Burkina Faso',
            'emoji':'🇧🇫'
        },
        'NE': {
            'name':'Niger',
            'emoji':'🇳🇪'
        },
        'TD': {
            'name':'Chad',
            'emoji':'🇹🇩'
        },
        'RW': {
            'name':'Rwanda',
            'emoji':'🇷🇼'
        },
        'BI': {
            'name':'Burundi',
            'emoji':'🇧🇮'
        },
        'MW': {
            'name':'Malawi',
            'emoji':'🇲🇼'
        },
        'LS': {
            'name':'Lesotho',
            'emoji':'🇱🇸'
        },
        'SZ': {
            'name':'Eswatini',
            'emoji':'🇸🇿'
        },
        'AO': {
            'name':'Angola',
            'emoji':'🇦🇴'
        },
        'CM': {
            'name':'Cameroon',
            'emoji':'🇨🇲'
        },
        'GA': {
            'name':'Gabon',
            'emoji':'🇬🇦'
        },
        'CG': {
            'name':'Congo',
            'emoji':'🇨🇬'
        },
        'CD': {
            'name':'Democratic Republic of the Congo',
            'emoji':'🇨🇩'
        },
        'BJ': {
            'name':'Benin',
            'emoji':'🇧🇯'
        },
        'TG': {
            'name':'Togo',
            'emoji':'🇹🇬'
        },
        'CV': {
            'name':'Cape Verde',
            'emoji':'🇨🇻'
        },
        'GM': {
            'name':'Gambia',
            'emoji':'🇬🇲'
        },
        'SL': {
            'name':'Sierra Leone',
            'emoji':'🇸🇱'
        },
        'LR': {
            'name':'Liberia',
            'emoji':'🇱🇷'
        },
        'GW': {
            'name':'Guinea-Bissau',
            'emoji':'🇬🇼'
        },
        'ST': {
            'name':'São Tomé and Príncipe',
            'emoji':'🇸🇹'
        },
        'CV': {
            'name':'Cape Verde',
            'emoji':'🇨🇻'
        },
        'UZ': {
            'name':'Uzbekistan',
            'emoji':'🇺🇿'
        },
        'MK': {
            'name':'North Macedonia',
            'emoji':'🇲🇰'
        },
        'AL': {
            'name':'Albania',
            'emoji':'🇦🇱'
        },
        'MT': {
            'name':'Malta',
            'emoji':'🇲🇹'
        },
        'IS': {
            'name':'Iceland',
            'emoji':'🇮🇸'
        },
        'LV': {
            'name':'Latvia',
            'emoji':'🇱🇻'
        },
        'PR': {
            'name':'Puerto Rico',
            'emoji':'🇵🇷'
        },
        'MN': {
            'name':'Mongolia',
            'emoji':'🇲🇳'
        },
        'MY': {
            'name':'Malaysia',
            'emoji':'🇲🇾'
        },
        'JQ': {
            'name':'Jordan',
            'emoji':'🇯🇴'
        },
        'MV': {
            'name':'Maldives',
            'emoji':'🇲🇻'
        },
    }
    for code, info in CountryDict.items():
        if code == CountryCode:
            return info['name'], info['emoji']
    return 'Unknown', '🏳️'

def GenerateMenu(MenuList = [],defautl_color = _fw ,SeletedColor = _fb,Titel = 'Menu Title...',Desciption= '',InputMsg = 'Enter Command : >'):
    Maxlen = len(Titel)
    for _x in MenuList:
        if Maxlen < len(_x):
            Maxlen = len(_x)
    if Maxlen < 45:
        Maxlen = 45
    print("")
    print(defautl_color + '-' * Maxlen)
    print(defautl_color + '-' * 5 +  f'> {SeletedColor}{Titel}{_reset}')
    print(defautl_color + '-' * Maxlen + "\n")
    count = 1
    for item in MenuList:
        print(f'{defautl_color}( {SeletedColor}{count} {defautl_color}) {item}{_reset}')
        count = count +1
    print(f'{defautl_color}( {SeletedColor}b {defautl_color}) Back to ...{_reset}')
    print(f'{defautl_color}( {SeletedColor}q {defautl_color}) Quit {_reset}')
    UserInput = input(f"\n{_B}{defautl_color}{InputMsg}")
    return UserInput.lower().strip()



def FnConfirmChange(MsgStr = "Are You Sure ?",YesTxt = "YES", NoText = "NO"):    
    SaveInput = input(f'{_B}{_fw}{MsgStr} [ {_bg} {YesTxt.upper()} {_reset}{_B + _fw} / {_br} {NoText.upper()} {_reset}{_B + _fw} ] >{_reset}')
    if SaveInput.strip() == '':
        return None
    elif SaveInput.lower() in ['0','n','no']:
        return False
    elif SaveInput.lower() in ['y','yes']:
        return True

        







if __name__ == "__main__":    
    print(f"{Style.NORMAL + Fore.YELLOW}You should not run this file directly")
