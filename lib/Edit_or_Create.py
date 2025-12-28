import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    MessageHandler,    
)
from tunnel import TUNNEL_LIST,SSHKEYDir,RefreshTunnelList,LOG_PATH
import TelegramBotFunction as BotFunc
import tempfile
import json
import lib.BaseFunction


def ConfirmationMenu(YesCallbackData='yes',NoCallbackData='no',YesText='✅ Yes',NoText='❌ No'):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(YesText, callback_data=YesCallbackData),InlineKeyboardButton(NoText, callback_data=NoCallbackData)],
    ])

def GetNumberMenu(TunnelCode,CallbackPrefix= ""):
    MenuList=[]
    MenuList.append([   InlineKeyboardButton("1️⃣", callback_data=f"{CallbackPrefix}_1|{TunnelCode}"),
                        InlineKeyboardButton("2️⃣", callback_data=f"{CallbackPrefix}_2|{TunnelCode}"),
                        InlineKeyboardButton("3️⃣", callback_data=f"{CallbackPrefix}_3|{TunnelCode}")]) 
    MenuList.append([   InlineKeyboardButton("4️⃣", callback_data=f"{CallbackPrefix}_4|{TunnelCode}"),
                        InlineKeyboardButton("5️⃣", callback_data=f"{CallbackPrefix}_5|{TunnelCode}"),
                        InlineKeyboardButton("6️⃣", callback_data=f"{CallbackPrefix}_6|{TunnelCode}")]) 
    MenuList.append([   InlineKeyboardButton("7️⃣", callback_data=f"{CallbackPrefix}_7|{TunnelCode}"),
                        InlineKeyboardButton("8️⃣", callback_data=f"{CallbackPrefix}_8|{TunnelCode}"),
                        InlineKeyboardButton("9️⃣", callback_data=f"{CallbackPrefix}_9|{TunnelCode}")]) 
    
    MenuList.append([InlineKeyboardButton("❌ Disable", callback_data=f"{CallbackPrefix}_0|{TunnelCode}")])
    MenuList.append([InlineKeyboardButton("⬅️ Back to Edit Menu", callback_data=f"AdvancedMenu|{TunnelCode}")])    
    return InlineKeyboardMarkup(MenuList)

def TunnelTypeMenu(TunnelCode=''):
    Menulist = []
    Menulist.append([InlineKeyboardButton("🏠 Local Port Forwarding", callback_data=f"TypeMode_local|{TunnelCode}")])    
    Menulist.append([InlineKeyboardButton("🛰️ Remote Port Forwarding", callback_data=f"TypeMode_Remote|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("⚡ Dynamic Port Forwarding", callback_data=f"TypeMode_Dynamic|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("⬅️ Back to Edit Menu", callback_data=f"EditTunnel|{TunnelCode}")])
    return InlineKeyboardMarkup(Menulist)

###################################
## NEMU
####################################


def DetectUserTunnelChanges(TunnelCode='',Fileds2Edit='',New_Value = ''):
    oldValue = TUNNEL_LIST[TunnelCode].get(Fileds2Edit,None)
    if oldValue is None:
        return True
    if oldValue.strip() != New_Value.strip():
        return True
    return False

def DetectTunnelChangeds(TunnelDict={},UserDataTunnel={}):
    for key in UserDataTunnel:
        oldValue = TunnelDict.get(key,None)
        newValue = UserDataTunnel.get(key,None)
        if oldValue is None or newValue is None:
            continue
        if str(oldValue).strip() != str(newValue).strip():
            return True



###################################
## Authenticate User Change Handler
####################################

async def AuthenticateUserChange(user_id: int,context,DataInput,query):
    tunnelCode= DataInput.split('|')[1]
    Action = DataInput.split('_')[2].split('|')[0]    
#    context.user_data["awaiting_value"] = True
#    context.user_data["TunnelInEdit"] = tunnelCode
    if Action == 'SetAuthPass':
        FieldToEdit = 'password'
        Msg = f"🔒 Please Enter New Password :"
    elif Action == 'SetAuthKeyfile':
        FieldToEdit = 'key_path'
        MsgList = []
        MsgList.append("🗝️ تغیر مسیر کلید احراز هویت\n\n")
        MsgList.append("📁 لطفا مسیر کامل کلید جدید را وارد نمایید. \n\n ")
        MsgList.append("نکته: در بعضی از نگارش های تلگرام هر ورودی با / دستور در نظر گرفته می شود، می توانید / اول را وارد نکید در زمان پردازش به آدرس اضافه خواهد شد.  \n\n ")
        MsgList.append("مثال: home/user/.ssh/id_rsa \n")
        Msg = ''.join(MsgList)
    elif Action == 'SetAuthPrivateKey':
        FieldToEdit = 'private_key'
        MsgList = []
        MsgList.append("🗝️ ارسال محتویات کلید در قالب پیام.\n\n")
        MsgList.append("📁 محتوای کلید خود را در در قالب پیام ارسال کنید..\n\n")
        MsgList.append("⚠️ نکات مهم: بازشدن فایل کلید با یک وبرایش گر غیر استاندارد می تواند باعث ایجاد مشکلاتی در ساختار کلید شود\n\n")
        MsgList.append("⚠️ نکات امنیتی:\nکلید ارسالی در قالب یک فال در سرور ذخیره خواهد شد.\n لطفا پس از ارسال پیام، آن را حذف نمایید تا امنیت کلید حفظ شود.\n\n")
        Msg = ''.join(MsgList)
    elif Action == 'UploadKey':
        MsgList = []
        MsgList.append("🗝️ ارسال فایل کلید\n\n")
        MsgList.append("📤 لطفا فایل کلید را در قالب یک Documents  ارسال کنید.\n\n")
        MsgList.append("⚠️ نکات امنیتی:\nکلید ارسالی در قالب یک فال در سرور ذخیره خواهد شد.\n لطفا پس از ارسال پیام، آن را حذف نمایید تا امنیت کلید حفظ شود.\n\n")
        Msg = ''.join(MsgList)        
        FieldToEdit = 'UploadKey'
    
    context.user_data["FieldToEdit"] = FieldToEdit
    
        
    keyboard = [
        [InlineKeyboardButton("❌ Cancel", callback_data=f"EditTunnel|{tunnelCode}")]        
    ]
    await query.message.reply_text(
        Msg,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
async def HandleAuthValueInput(update: Update, context: ContextTypes.DEFAULT_TYPE,TunnelInEdit,FileldToEdit,value):    
    AlertMessage = "⚠️ Security Note ⚠️\nTelegram does not allow you to delete your messages in private chats.\nIt is best to delete your messages that contain sensitive information."
    if FileldToEdit == 'password':
        if value.strip() == '':
            await update.message.reply_text("Password cannot be empty. Please send a valid password.")
            return False
        context.user_data['tunnel_list'][TunnelInEdit]['authentication'] = 'password'
        context.user_data['tunnel_list'][TunnelInEdit]['password'] = value
        await update.message.reply_text(f"✅ Password updated successfully for tunnel {TunnelInEdit}.\n")
    elif FileldToEdit == 'key_path':
        if value.strip() == '':
            await update.message.reply_text("Key file path cannot be empty. Please send a valid path.")
            return False
        if value.strip().startswith('/'):
            KeyFileRealPath = value.strip()
        else:
            KeyFileRealPath = '/' + value.strip()    
        if not os.path.isfile(KeyFileRealPath):
            await update.message.reply_text(f"❌ The specified key file does not exist: {KeyFileRealPath}\nPlease check the path and try again.")
            return False
        context.user_data['tunnel_list'][TunnelInEdit]['authentication'] = 'key_path'
        context.user_data['tunnel_list'][TunnelInEdit]['key_path'] = value 
        await update.message.reply_text(f"✅ authentication Tunnel ( {TunnelInEdit} ) change to Custom KeyFile.\n")
    elif FileldToEdit == 'private_key':
        if value.strip() == '':
            await update.message.reply_text("Private key content cannot be empty. Please send valid key content.")
            return False
        # Save the private key to a temporary file
        KeyFilePath = f"{SSHKEYDir}/{TunnelInEdit}_private_key.pem"        
        try:
            with open(KeyFilePath, 'w') as key_file:
                key_file.write(value.strip())
            os.chmod(KeyFilePath, 0o600)  # Set file permissions to read/write for owner only
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to save private key file: {str(e)}\nPlease try again.")
            return False
        context.user_data['tunnel_list'][TunnelInEdit]['authentication'] = 'key_path'
        context.user_data['tunnel_list'][TunnelInEdit]['key_path'] = KeyFilePath 
        await update.message.reply_text(f"✅ authentication Tunnel ( {TunnelInEdit} ) change to Private Key.\n\n Key Saved to:\n {KeyFilePath}\n")        

    elif FileldToEdit == 'UploadKey':
        pass
    else:
        context.user_data['tunnel_list'][TunnelInEdit]['authentication'] = ''
        context.user_data['tunnel_list'][TunnelInEdit]['password'] = ''
        await update.message.reply_text(f"Tunnel ({TunnelInEdit}) Use Defualt authentication.\n")
        return True
    
    await update.message.reply_text(AlertMessage)
    return True


###################################
## END Authenticate User Change Handler
####################################
async def CloneTunnelHandler(user_id: int,context,query,tunnelCode):
    keyboard = [
        [InlineKeyboardButton("❌ Cancel", callback_data=f"tunnel|{tunnelCode}")]        
    ]
    _msg = f"🖊️ Please Enter New Tunnel Code for the Cloned Tunnel:\n*Note:* This Code Must be Uniq 🦄\n\n"
    StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_Tunnel_Clone')
    if StikerID != None:
        await context.bot.send_sticker(
            chat_id=user_id,
            sticker=StikerID)
    await query.message.reply_text(
        _msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
        

async def StandardFieldUserChange(user_id: int,context,DataInput,query,tunnelCode):
    keyboard = [
        [InlineKeyboardButton("❌ Cancel", callback_data=f"EditTunnel|{tunnelCode}")]        
    ]
    if DataInput.split('|')[0].split('_')[1] == "Name":
        Msg = f"✏️ Enter Name for the Tunnel:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('Name','')}"
    elif DataInput.split('|')[0].split('_')[1] == "sship":
        Msg = f"✏️ Enter SSH Server 📍 Ip Adress for the Tunnel {tunnelCode}:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('ssh_ip','N/A')}"
    elif DataInput.split('|')[0].split('_')[1] == "sshport":
        Msg = f"✏️ Enter SSH Server 🔌 port for the Tunnel {tunnelCode}:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('ssh_port','N/A')}"
    elif DataInput.split('|')[0].split('_')[1] == "sshuser":
        Msg = f"✏️ Enter SSH Server 👤 User for the Tunnel {tunnelCode}:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('ssh_user','N/A')}"
    elif DataInput.split('|')[0].split('_')[1] == "SourceServer":
        Msg = f"✏️ Enter 📍 Source Server address for the Tunnel {tunnelCode}:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('Source_Server','N/A')}"
    elif DataInput.split('|')[0].split('_')[1] == "Sourceport":
        Msg = f"✏️ Enter 🔌 Source port for the Tunnel {tunnelCode}:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('Source_port','N/A')}"
    elif DataInput.split('|')[0].split('_')[1] == "FinalPort":
        Msg = f"✏️ Enter 🏁 Final Port for the Tunnel {tunnelCode}:\n\n old Value is: {context.user_data['tunnel_list'][tunnelCode].get('FinalPort','N/A')}"
        StikerID = BotFunc.GetTelegramStickerID(StikerName='change_FinalPort_config')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=user_id,
                sticker=StikerID)            
    elif DataInput.split('|')[0].split('_')[1].split('.')[0] == "MonitorPort":
        Highly_Restricted_Networks = context.user_data['tunnel_list'][tunnelCode].get('Highly_Restricted_Networks')
        MonitorPort = Highly_Restricted_Networks.get('MonitorPort',0)        
        try:
            MonitorPortInt = int(MonitorPort)
        except:
            MonitorPortInt = 0        
        MsgLine = []
        if MonitorPortInt == 0:
            MsgLine.append(f"❌ شما پورت مانیتورینگ 🛟 مستقل از تونل رابرای تونل [ {MonitorPort} ] غیر فعال کرده اید.\n\n")            
            MsgLine.append("⚠️ *نکته:* اگر در یک شبکه با محدودیت شدید هستید، توصیه می‌شود این گزینه را فعال کنید تا پایداری تونل افزایش یابد.\n\n")                    
        else:
            MsgLine.append(f"پورت مانیتورینگ 🛟 مستقل از تونل بر روی 44 تنظیم شده است \n\n")

        MsgLine.append(f"ℹ️ این پورت به صورت مستقل از تونل برای بررسی وضعیت اتصال استفاده می‌شود و در صورت عدم پاسخگویی، تونل را مجدداً راه‌اندازی می‌کند.\n\n")            
        MsgLine.append(f"ℹ️ این روش مستقل از خود SSH keepalive است و واقعاً سلامت مسیر تونل را می‌سنجد.")       
        MsgLine.append(f"ℹ️ مقدار 0 برای غیر فعال سازی *پورت مانیتورینگ را وارد نمایید*")
        MsgLine.append(f"⚠️ این پورت باید در هر دو سرور مبدا و مقصد آزاد و در دسترس باشد.\n\n")                
        MsgLine.append(f"⚠️ این سرویس در سرور لوکال از دو پورت پشت سرهم استفاده می کند\n")        
        MsgLine.append(f"یه طور مثال اگر پورت را 2000 وارد کنید دو پورت 2000 و 2001 استفاده خواهند شد\n\n")        

        Msg = ''.join(MsgLine)       
        StikerID = BotFunc.GetTelegramStickerID(StikerName='MonitorPort')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=user_id,
                sticker=StikerID)


#        await query.message.reply_text(
#            Msg,
#            reply_markup=ConfirmationMenu(
#                YesCallbackData=f"MonitorPort_disable|{tunnelCode}",
#                NoCallbackData=f"AdvancedMenu|{tunnelCode}",
#                YesText='✅ Yes, Disable',
#                NoText='❌ No, Cancel'),
#            parse_mode="Markdown")

    await query.message.reply_text(
        Msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    

async def EditStandardField(update: Update, context: ContextTypes.DEFAULT_TYPE,TunnelInEdit,FileldToEdit,value):
    if value.strip() == '':
        return await update.message.reply_text(f"{FileldToEdit} cannot be empty. Please send a valid value.")    
    if FileldToEdit == 'Name':
        FileldToEdit = 'Name'
        SuccessMsg = f"✅ Name for Tunnel ( {TunnelInEdit} ) updated to {value.strip()}.\n"
    elif FileldToEdit == 'sship':
        FileldToEdit = 'ssh_ip'
        SuccessMsg = f"✅ SSH IP for Tunnel ( {TunnelInEdit} ) updated to {value.strip()}.\n"
    elif FileldToEdit == 'sshport':
        try:
            port = int(value.strip())
            if port < 1 or port > 65535:
                await update.message.reply_text("❌ Invalid port number. Please enter a value between 1 and 65535.")
                return  False
        except ValueError:
            await update.message.reply_text("❌ Invalid port number. Please enter a numeric value.")
            return False
        FileldToEdit = 'ssh_port'
        SuccessMsg = f"✅ SSH Port for Tunnel ( {TunnelInEdit} ) updated to {port}.\n"
    elif FileldToEdit == 'sshuser':
        FileldToEdit = 'ssh_user'        
        SuccessMsg = f"✅ SSH User for Tunnel ( {TunnelInEdit} ) updated to {value.strip()}.\n"
    elif FileldToEdit == 'SourceServer':
        FileldToEdit = 'Source_Server'        
        SuccessMsg = f"✅ Source Server for Tunnel ( {TunnelInEdit} ) updated to {value.strip()}.\n"
    elif FileldToEdit == 'Sourceport':
        try:
            port = int(value.strip())
            if port < 1 or port > 65535:
                await update.message.reply_text("❌ Invalid port number. Please enter a value between 1 and 65535.")
                return  False
        except ValueError:
            await update.message.reply_text("❌ Invalid port number. Please enter a numeric value.")
            return False
        FileldToEdit = 'Source_port'        
        SuccessMsg = f"✅ Source Port for Tunnel ( {TunnelInEdit} ) updated to {port}.\n"
    elif FileldToEdit == 'FinalPort':
        try:
            port = int(value.strip())
            if port < 1 or port > 65535:
                await update.message.reply_text("❌ Invalid port number. Please enter a value between 1 and 65535.")
                return  False
        except ValueError:
            await update.message.reply_text("❌ Invalid port number. Please enter a numeric value.")
            return False
        FileldToEdit = 'FinalPort'        
        SuccessMsg = f"✅ Final Port for Tunnel ( {TunnelInEdit} ) updated to {port}.\n"
    elif FileldToEdit == 'MonitorPort':
        try:
            port = int(value.strip())
            if port < 0 or port > 65535:
                await update.message.reply_text("❌ Invalid port number. Please enter a value between 0 and 65535.")
                return  False
        except ValueError:
            await update.message.reply_text("❌ Invalid port number. Please enter a numeric value.")
            return False
        Highly_Restricted_Networks = context.user_data['tunnel_list'][TunnelInEdit].get('Highly_Restricted_Networks',{})
        Highly_Restricted_Networks['MonitorPort'] = port
        context.user_data['tunnel_list'][TunnelInEdit]['Highly_Restricted_Networks'] = Highly_Restricted_Networks
        if port == 0:
            SuccessMsg = f"✅ Monitor Port for Tunnel ( {TunnelInEdit} ) has been disabled.\n"
        else:
            port1 = port + 1 
            SuccessMsg = f"✅ Monitor Port for Tunnel ( {TunnelInEdit} ) updated to {port}.\n Open port {port},{port1} on Servers\n\n"
    await update.message.reply_text(SuccessMsg)

    context.user_data['tunnel_list'][TunnelInEdit][FileldToEdit] = value.strip()    
    return True

### Upload File

##async def HabdeleUploadKeyFile(update: Update, context: ContextTypes.DEFAULT_TYPE,TunnelInEdit):
##    if not update.message.document:
##        await update.message.reply_text("❌ No document found in the message. Please upload a valid key file.")
##        return False
##
##    document = update.message.document
##    if document.mime_type not in ['application/x-pem-file', 'application/octet-stream', 'text/plain']:
##        await update.message.reply_text("❌ Invalid file type. Please upload a valid key file.")
##        return False
##
##    # Download the file
##    KeyFilePath = f"{SSHKEYDir}/{TunnelInEdit}_uploaded_key.pem"
##    try:
##        await document.get_file().download_to_drive(custom_path=KeyFilePath)
##        os.chmod(KeyFilePath, 0o600)  # Set file permissions to read/write for owner only
##    except Exception as e:
##        await update.message.reply_text(f"❌ Failed to download and save key file: {str(e)}\nPlease try again.")
##        return False
##
##    context.user_data['tunnel_list'][TunnelInEdit]['authentication'] = 'key_path'
##    context.user_data['tunnel_list'][TunnelInEdit]['key_path'] = KeyFilePath 
##    await update.message.reply_text(f"✅ authentication Tunnel ( {TunnelInEdit} ) change to Uploaded Key File.\n\n Key Saved to:\n {KeyFilePath}\n")        
##    AlertMessage = "⚠️ Security Note ⚠️\nTelegram does not allow you to delete your messages in private chats.\nIt is best to delete your messages that contain sensitive information."
##    await update.message.reply_text(AlertMessage)
##    return True

async def RestrictedModeConfirm(user_id: int,context,query,TunnelCode):
    RestrictedModeStatus = context.user_data['tunnel_list'][TunnelCode].get('Highly_Restricted_Networks',{}).get('Enable',False)
    if RestrictedModeStatus:
        MsgList = []
        MsgList.append(f"⚠️شما در حال غیر فعال کردن حالت پایداری در شبکه با محدودیت شدید برای تونل [ {TunnelCode} ] هستید.\n\n")
        MsgList.append("\n*برای غیر فعال کردن این گزینه مطمين هستید ؟*")
        Msg = ''.join(MsgList)
        #Msg = f"❗ You are about to ⚠️ disable Highly Restricted Networks mode for tunnel .\n\n*Are you sure?*"
        await query.message.reply_text(
            Msg,
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"RestrictedMode_disable|{TunnelCode}",
                NoCallbackData=f"AdvancedMenu|{TunnelCode}",
                YesText='✅ Yes, Disable',
                NoText='❌ No, Cancel'),
            parse_mode="Markdown")
        
    else:
        MsgList = []
        MsgList.append(f"❕شما در حال فعال کردن حالت پایداری در شبکه با محدودیت شدید برای تونل {TunnelCode} هستید.\n\n")
        MsgList.append("⚠️ *توجه:* در این حالت تونل در برابر محدودیت های شبکه مقاومت می کند و در صورت اختلال به سرعت بازسازی می شود، اما برای فعال سازی این حالت، باید نرم افزار ( autossh ) روی سرور نصب باشد.\n\n")
        #Msg = f"❕ You are about to ✔️ Enable Highly Restricted Networks mode for tunnel [ {TunnelCode} ].\n\n⚠️ *Note:* In this mode, tunnel resists network restrictions, but to activate this mode, ( autossh ) must be installed on the server\n\n*Are you sure?*"
        Msg = ''.join(MsgList)
        await query.message.reply_text(
            Msg,
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"RestrictedMode_enable|{TunnelCode}",
                NoCallbackData=f"AdvancedMenu|{TunnelCode}",
                YesText='✅ Yes, Enable',
                NoText='❌ No, Disable'),
            parse_mode="Markdown")

async def RestrictedModeChange(data,context):
        TunnelCode = data.split('|')[1]
        Status_RestrictedMode = data.split('|')[0].split('_')[1]

        if Status_RestrictedMode == 'enable':
            Status_RestrictedMode = True
        elif Status_RestrictedMode == 'disable':            
            Status_RestrictedMode = False
        context.user_data["tunnel_list"][TunnelCode]["Highly_Restricted_Networks"]["Enable"] = Status_RestrictedMode


async def ExitOnForwardFailureConfirm(context,query,data):
    TunnelCode = data.split('|')[1]
    RestrictedModeStatus = context.user_data['tunnel_list'][TunnelCode].get('Highly_Restricted_Networks',{})
    ExitOnForwardFailure = RestrictedModeStatus.get('ExitOnForwardFailure','yes')
    if ExitOnForwardFailure == 'yes':
        MsgList = []
#        MsgList.append(f"❗ You are about to ✔️ Enable kill tunnel on Forward port Failure for tunnel [ {TunnelCode} ].\n\n")
#        MsgList.append("⚠️ *Note:* When this option is disabled, the tunnel will attempt to reconnect automatically if the forward port fails, instead of terminating the tunnel.\n\n")
#        MsgList.append("⚠️ *Note:* Turned off this option to prevent tunnels from being killed He takes the lost.\n\n")
#        MsgList.append("⚠️ *Note:* The activation of this option along with the correct setting of other parameters can make the tunnel more stable.")
#        MsgList.append("\n*Are you sure?*")
        MsgList.append(f"❗شما در حال غیر فعال کردن گزینه  قطع شدن تونل در صورت اختلال در پورت مقصد برای تونل  [ {TunnelCode} ] هستید\n\n")
        MsgList.append("⚠️ *توجه:* وقتی این گزینه غیرفعال باشد، برنامه سعی می کند به جای پایان دادن به تونل، در صورت ایراد در اتصال ، دوباره اتصال را برقرار کند.\n\n")
        MsgList.append("⚠️ *نکته:* خاموش کردن این گزینه می تواند باعث زنده نگه داشتن اتصال های خراب گردد.\n\n")
        MsgList.append("⚠️ *نکته:* فعال بودن این گزینه به همراه تنظیم صحیح سایر پارامترها می‌تواند تونل را پایدارتر کند.")
        MsgList.append("\n\n*برای غیر فعال کردن این گزینه مطمين هستید ؟*")

        Msg = ''.join(MsgList)
        await query.message.reply_text(
            Msg,
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"ExitOnForwardFailure_disable|{TunnelCode}",
                NoCallbackData=f"AdvancedMenu|{TunnelCode}",
                YesText='✅ Yes, Disable',
                NoText='❌ No, Enable'),
            parse_mode="Markdown")
    else:
        MsgList = []        
        MsgList.append(f"❕شما در حال فعال کردن قطع شدن تونل در صورت اختلال در پورت مقصد برای تونل [ {TunnelCode} ] هستید.\n\n")
        MsgList.append("⚠️ *توجه:* وقتی این گزینه فعال باشد، در صورت در دسترس نبودن پورت مقصد به هر دلیلی تونل بسته خواهد شد و نرم افزار متوجه اختلال در تونل می گردد. \n\n")        
        MsgList.append("⚠️ *نکته:* فعال بودن این گزینه به همراه تنظیم صحیح سایر پارامترها می‌تواند تونل را پایدارتر کند.")
        MsgList.append("\n\n*برای غیر فعال کردن این گزینه مطمين هستید ؟*")
        Msg = ''.join(MsgList)
        await query.message.reply_text(
            Msg,
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"ExitOnForwardFailure_enable|{TunnelCode}",
                NoCallbackData=f"AdvancedMenu|{TunnelCode}",
                YesText='✅ Yes, Enable',
                NoText='❌ No, Disable'),
            parse_mode="Markdown")

async def ExitOnForwardFailureChange(data,context):
        TunnelCode = data.split('|')[1]
        Status_ExitOnForwardFailure = data.split('|')[0].split('_')[1]
        if Status_ExitOnForwardFailure == 'enable':
            Status_ExitOnForwardFailure = 'yes'
        elif Status_ExitOnForwardFailure == 'disable':            
            Status_ExitOnForwardFailure = 'no'
        context.user_data["tunnel_list"][TunnelCode]["Highly_Restricted_Networks"]["ExitOnForwardFailure"] = Status_ExitOnForwardFailure        
        return True

async def SendAlivePacketMenuHandler(context,query,data,UserId):
    TunnelCode = data.split('|')[1]
    Highly_Restricted_Networks = context.user_data['tunnel_list'][TunnelCode].get("Highly_Restricted_Networks",{})
    ServerAliveInterval = Highly_Restricted_Networks.get('ServerAliveInterval',0)
    if ServerAliveInterval <= 0:
        MsgList = []
        MsgList.append(f"⚠️ ارسال پکت برای زنده نگه داشتن تونل برای تونل {TunnelCode} غیر فعال شده است.\n\n")
        MsgList.append("⚠️ *توجه:* با غیر فعال کردن این گزینه، تونل ممکن است در صورت عدم فعالیت برای مدت طولانی قطع شود.\n\n")
        MsgList.append("⚠️ *نکته:* غیرفعال کردن این گزینه باعث کاهش پایداری تونل در شبکه‌های با محدودیت شدید شود.\n\n")
        MsgList.append("\n*برای غیر فعال کردن این گزینه مطمين هستید ؟*")
        Msg = ''.join(MsgList)
    else:
        MsgList = []
        MsgList.append(f"⏲️ هر [ {ServerAliveInterval} ] ثانیه یک پکت برای زنده نگهداشتن تونل {TunnelCode} ارسال خواهد شد.\n\n")
        MsgList.append("با فعال بودن این امکان تونل در صورت عدم فعالیت برای مدت طولانی، با ارسال پکت‌های زنده نگه داشته می‌شود.\n\n")
        MsgList.append("⚠️ *نکته:* غیرفعال کردن این گزینه باعث کاهش پایداری تونل در شبکه‌های با محدودیت شدید شود.\n\n")
        MsgList.append("\n*مقدار دلخواه خود را انتخاب کنید ؟*")
        Msg = ''.join(MsgList)        

    
        StikerID = BotFunc.GetTelegramStickerID(StikerName='ServerAliveInterval')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)

    await query.message.reply_text(
        Msg,            
        reply_markup=GetNumberMenu(TunnelCode=TunnelCode,CallbackPrefix="SetExitOnForwardFailure"),
        parse_mode="Markdown")

async def ServerAliveCountMaxMenuHandler(context,query,data,UserId):
    TunnelCode = data.split('|')[1]
    Highly_Restricted_Networks = context.user_data['tunnel_list'][TunnelCode].get("Highly_Restricted_Networks",{})
    ServerAliveCountMax = Highly_Restricted_Networks.get('ServerAliveCountMax',0)
    if ServerAliveCountMax <= 0:
        MsgList = []
        MsgList.append(f"❕❗ مقدار خطای فابل تحمل تونل {TunnelCode} بر روی [ 0 ] تنظیم شده است \n\n")
        MsgList.append("⚠️ *نکته:* این مقدار یعنی هیچ خطایی قابل تحمل نیست و با اولین مشکل اتصال قطع خواهد شد.\n\n")
        MsgList.append("⚠️ اخطار :  این مقدار برای شبکه های ناپایدار ، تونل های دائمی و اتصالات VPN  مناسب نیست\n\n")
        MsgList.append("مناسب برای : اسکریپت‌های Fail-Fast، مانیتورینگ و ...")
        MsgList.append("\n*برای مقدار [ 0 ] این گزینه مطمين هستید ؟*")
        Msg = ''.join(MsgList)
    else:
        MsgList = []
        MsgList.append(f"مقدار خطای فابل تحمل تونل {TunnelCode} بر روی [ {ServerAliveCountMax} ] تنظیم شده است \n\n")
        MsgList.append(f"تونل {TunnelCode} بعد از {ServerAliveCountMax} عدم پاسخ پکت بررسی سلامت کشته خواهد شد.\n\n")        
        MsgList.append("\n*مقدار دلخواه خود را انتخاب کنید ؟*")
        Msg = ''.join(MsgList)        
    
        StikerID = BotFunc.GetTelegramStickerID(StikerName='ServerAliveCountMax')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)

    await query.message.reply_text(
        Msg,            
        reply_markup=GetNumberMenu(TunnelCode=TunnelCode,CallbackPrefix="SetServerAliveCountMax"),
        parse_mode="Markdown")


async def KeepAliveToggleHandler(context,query,data,UserId):
    TunnelCode = data.split('|')[1]
    KeepAliveMode = context.user_data['tunnel_list'][TunnelCode].get("Keep_Alive",False)
    if KeepAliveMode:
        MsgList = []
        MsgList.append(f"⚠️ شما در حال غیر فعال کردن گزینه Keep Alive برای تونل [ {TunnelCode} ] هستید.\n\n")
        MsgList.append("⚠️ با غیر فعال کردن این گزینه با راه اندازی مجدد سرور تونل قطع خواهد شد.\n\n")
        MsgList.append("\n*برای غیر فعال کردن این گزینه مطمين هستید ؟*")
        Msg = ''.join(MsgList)
        await query.message.reply_text(
            Msg,
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"KeepAliveServer_disable|{TunnelCode}",
                NoCallbackData=f"AdvancedMenu|{TunnelCode}",
                YesText='✅ Yes, Disable',
                NoText='❌ No, Enable'),
            parse_mode="Markdown")
    else:
        MsgList = []
        MsgList.append(f"❕شما در حال فعال کردن گزینه Keep Alive برای تونل [ {TunnelCode} ] هستید.\n\n")
        MsgList.append("⚠️  راه اندازی می شود و تونل را در هر شرایطی زنده نگه می دارد این امکان به کمک یک سرویس مستقل به نام KeepAlive.\n\n")
        MsgList.append("⚠️ با فعال کردن این گزینه تونل همیشه فعال خواهد ماند و امکان توقف آن حتی توسط کشتن اتصال در سیستم  عامل وجود نخواهد داشت.\n\n")
        MsgList.append("\n*برای فعال کردن این گزینه مطمين هستید ؟*")
        Msg = ''.join(MsgList)
        await query.message.reply_text(
            Msg,
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"KeepAliveServer_enable|{TunnelCode}",
                NoCallbackData=f"AdvancedMenu|{TunnelCode}",
                YesText='✅ Yes, Enable',
                NoText='❌ No, Disable'),
            parse_mode="Markdown")
    


async def ChangeTunnelType(data,context,UserId,query):
        TunnelCode = data.split('|')[1]
        StikerID = BotFunc.GetTelegramStickerID(StikerName='change_tunnel_type')
        CurrentType = ''
        for _t in TUNNEL_LIST:
            _tunnel = TUNNEL_LIST[_t]
            if _t == TunnelCode:
                CurrentType = _tunnel.get('Type','local')
                break
        if CurrentType == 'local':
            CurrentType = '🏠 Local Port Forwarding'
        elif CurrentType == 'remote':
            CurrentType = '🛰️ Remote Port Forwarding'
        elif CurrentType == 'dynamic':          
            CurrentType = '⚡ Dynamic Port Forwarding'

        SSHLink = "[GatewayPorts](https://linux.die.net/man/5/sshd_config#GatewayPorts)"
        MsgList= []
        MsgList.append(f"⚙️ شما در حال تغییر نوع تونل برای تونل [ {TunnelCode} ] هستید.\n\n")
        MsgList.append(f"*🏠 Local Port Forwarding :*\n\n")
        MsgList.append(f"- این نوع تونل برای انتقال اطاعات از سرور راه دور و یا همان مقصد به سرور محلی استفاده می‌شود.\n")        
        MsgList.append(f"- در این روش یک پورت سرور مقصد و یا پورت سرور دیگیری که در دسترس سرور مقصد می باشد به سرور محلی منتقل می شود.\n\n") 
        MsgList.append(f"*🛰️ Remote Port Forwarding :*\n\n")
        MsgList.append(f"- این نوع تونل برای انتقال اطلاعات از سرور محلی  به سرور مقصد استفاده می‌شود.\n")
        MsgList.append(f"- در این روش یک پورت سرور محلی و یا پورت سرور دیگری که در دسترس سرور محلی می باشد به سرور راه دور منتقل می شود.\n")                
        MsgList.append(f"- این توع تونل احتیاج به تنظبماتی اضافی در سرور مقصد دارد.\n")
        MsgList.append(f"- برای استفاده از این روش باید {SSHLink} در سرور مقصد در تنظیمات SSH انجام شده باشد.\n\n")        
        MsgList.append(f"*⚡ Dynamic Port Forwarding :*\n\n")
        MsgList.append(f"- نوع تونل به عنوان یک پروکسی پویا عمل می‌کند و به شما امکان می‌دهد تا ترافیک را از طریق تونل به مقصدهای مختلف هدایت کنید.\n")
        MsgList.append(f"- در این روش اطلاعات از سرور محلی به سرور مقصد و یا همان راه دور منتقل خواهد شد\n")
        MsgList.append(f"- ⚠️ *توجه:* تغییر نوع تونل ممکن است نیاز به تنظیمات اضافی داشته باشد و باید با نیازهای شما سازگار باشد.\n\n")
        
        MsgList.append(f"Current TunnelType: *" + CurrentType + "*\n\n")
        Msg = ''.join(MsgList)


        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
            
        await query.message.reply_text(                        
            Msg,
            reply_markup=TunnelTypeMenu(TunnelCode=TunnelCode),
            parse_mode="Markdown"
        )

#        await query.message.reply_text(                        
#            f"⚙️ Select Tunnel Mode  for Tunnel ( {TunnelCode} )\n\n Current Mode: {CurrentType}",
#            reply_markup=TunnelTypeMenu(TunnelCode=TunnelCode),
#            parse_mode="Markdown"
#        )
        return

async def SaveUserTunnelChangesConfim(context,query,update,UserId):
        ######### SAVE CHANGES ##############
        StikerID = BotFunc.GetTelegramStickerID(StikerName='Save_changes')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
        TUNNEL_LIST = RefreshTunnelList()
        TunnelChangesDict = BotFunc.compare_dicts(dict1=TUNNEL_LIST,dict2=context.user_data["tunnel_list"])
        FinalMsg = BotFunc.GenerateDiffReport(DiffResult=TunnelChangesDict)

        await query.message.reply_text(
            f"❓ Are you sure with the changes? \n{FinalMsg}",
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"YesSaveUserTunnelChanges",
                NoCallbackData=f"tunnel_list",
                YesText='✅ Yes, Save Changes',
                NoText='❌ No, Discard Changes'))
            

async def ExportTunnelAsJson(TunnelCode,context,UserId):    
    for _tunnel in TUNNEL_LIST:
        if _tunnel == TunnelCode:
            TunnelData = context.user_data['tunnel_list'][_tunnel]
            break
    
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8"
    ) as f:
        json.dump(TunnelData, f, ensure_ascii=False, indent=2)
        file_path = f.name

    await context.bot.send_document(
        chat_id=UserId,
        document=open(file_path, "rb"),
        filename=f"Tunnel-{TunnelCode}-Configuration.json",
        caption=f"📄 Download Json Configuration for Tunnel ({TunnelCode})"
    )

async def DownloadTunnelLogs(TunnelCode,context,UserId):
    LogFilePath = f"{LOG_PATH}/{TunnelCode}.log"
    if not os.path.isfile(LogFilePath):
        return False
    try:
        await context.bot.send_document(
            chat_id=UserId,
            document=open(LogFilePath, "rb"),
            filename=f"Tunnel-{TunnelCode}-Logs.log",
            caption=f"📄 Download Logs for Tunnel ({TunnelCode})")
        return True
    except Exception as e:
        print(f"Error sending log file: {str(e)}")
        return False

async def DownloadTemplateTunnelAsJson(context,UserId):    
    TunnelData = {
        "Code": "",
        "ssh_ip": "",
        "ssh_port": 22,
        "ssh_user": "root",
        "authentication": "password_or_key_path",
        "password": "your_ssh_password_if_using_password_authentication",
        "key_path": "/path/to/your/private/key_if_using_key_authentication",
        "Type": "local_or_remote_or_dynamic",
        "Source_Server": "localhost",
        "Source_port": 8080,
        "FinalPort": 9090,
        "Highly_Restricted_Networks": {
            "Enable": False,
            "MonitorPort": 0,
            "ExitOnForwardFailure": "yes",
            "ServerAliveInterval": 1,
            "ServerAliveCountMax": 3
        },
        "Keep_Alive": False,
    }    
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8"
    ) as f:
        json.dump(TunnelData, f, ensure_ascii=False, indent=2)
        file_path = f.name

    await context.bot.send_document(
        chat_id=UserId,
        document=open(file_path, "rb"),
        filename=f"Tunnel-Template-Configuration.json",
        caption=f"📄 Download Json Configuration Template"
    )

async def CLoneCodeTextHandler(update: Update, context: ContextTypes.DEFAULT_TYPE,UserId,Value,Tunnel4Cloned):
    TunnelCodeIsUniq = True
    TunnelData = {}
    for _t in TUNNEL_LIST:        
        if _t.strip().lower() == Value.strip().lower():
            TunnelCodeIsUniq = False
        if _t == Tunnel4Cloned: # For Cloning
            TunnelData = context.user_data['tunnel_list'][_t]

    if not TunnelCodeIsUniq:
        await update.message.reply_text(f"❌ The Clone Code you entered is already in use. Please choose a different code and try again.\n*Note:* Code must be unique.",
            parse_mode="Markdown")
        return False
    if TunnelData  == {}:
        await update.message.reply_text(f"❌ Unable to find the tunnel data to clone. Please try again.",
            parse_mode="Markdown")
        return False
    
    context.user_data['tunnel_list'][Value.strip()] = TunnelData.copy()
    context.user_data['tunnel_list'][Value.strip()]['pid'] = ""
    context.user_data['tunnel_list'][Value.strip()]['Code'] = Value.strip()
    context.user_data['tunnel_list'][Value.strip()]['status'] = False
    context.user_data['tunnel_list'][Value.strip()]['is_active'] = False    
    return True

async def Edit_isActive(context: ContextTypes.DEFAULT_TYPE,TunnelInEdit,UserId,query):
    for _t in context.user_data['tunnel_list']:
        if _t == TunnelInEdit:
            TunnelDict = context.user_data['tunnel_list'][_t]

    StikerID = BotFunc.GetTelegramStickerID(StikerName='change_ssh_config')
    IsActive = TunnelDict.get('is_active',False)
    if StikerID != None:
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)
    if IsActive:
        await query.message.reply_text(
            f"❓ Are you sure to Disable Tunnel? \n",
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"IsActive_Change|{TunnelInEdit}",
                NoCallbackData=f"tunnel|{TunnelInEdit}",
                YesText='✅ Yes, Disable Tunnel',
                NoText='❌ No, Cancel'))
    else:
        await query.message.reply_text(
            f"❓ Are you sure to Enable Tunnel? \n",
            reply_markup=ConfirmationMenu(
                YesCallbackData=f"IsActive_Change|{TunnelInEdit}",
                NoCallbackData=f"tunnel_list",
                YesText='✅ Yes, Enable Tunnel',
                NoText='❌ No, Cancel'))
    pass
async def CreateNewTunnelHandler(context: ContextTypes.DEFAULT_TYPE,query,UserId):
    StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_Create_New_Tunnel')
    if StikerID != None:
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)
    MsgLine = []  
    MsgLine.append(f"⚙️ برای ایجاد تونل به یکی از دو روش زیر عمل کنید:\n\n")
    MsgLine.append(f"۱. فایل پیکربندی تونل را به صورت JSON آپلود کنید.\n\n")
    MsgLine.append(f"۲. تنظبمات تونل را با ساختار یک فابلjson به صورت دستی وارد کنید.\n\n")
    MsgLine.append(f"⚠️ *توجه:* در صورت انتخاب روش دوم، باید تمامی فیلدهای مورد نیاز را به درستی پر کنید تا تونل به درستی ایجاد شود.\n\n")    
    Msg = ''.join(MsgLine)

    keyboard = [
        [InlineKeyboardButton("📃 Download Template", callback_data=f"Download TunnelTemplate")],
        [InlineKeyboardButton("❌ Cancel", callback_data="tunnel_list")]
    ]

    await query.message.reply_text(
        Msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
async def HandleNewTunnelTemplateFileUpload(context: ContextTypes.DEFAULT_TYPE,update: Update,UserId,FilePath = "",LocadJsonFrom = 'file',UserInput = None):
    if LocadJsonFrom == 'file':
        JsonConfig = lib.BaseFunction.LoadJsonFile(JsonFile=FilePath,Verbus=False)
    else:
        JsonConfig = lib.BaseFunction.LoadJsonFromText(JsonText=UserInput,Verbus=False)
    if JsonConfig == None:
        Msg = "❌ Failed to load the JSON configuration file. Please ensure the file is correctly formatted and try again."
        await update.message.reply_text(Msg)
        return False,{}
        
    TunnelCode = JsonConfig.get('Code','').strip()
    if TunnelCode == '':
        Msg = "❌ The 'Code' field in the JSON configuration file is missing or empty. Please provide a unique tunnel code and try again."
        await update.message.reply_text(Msg)
        return False,{}
    else:
        TUNNEL_LIST = RefreshTunnelList()
        for _t in TUNNEL_LIST:
            if _t.strip().lower() == TunnelCode.strip().lower():
                Msg = f"❌ The Tunnel Code '{TunnelCode}' you provided is already in use. Please choose a different code and try again."
                await update.message.reply_text(Msg)
                return False,{}

    NewTunnel = {}
    NewTunnel["Name"] = JsonConfig.get('Name',"New Tunnel")
    NewTunnel["Code"] = TunnelCode
    NewTunnel["ssh_ip"] = JsonConfig.get('ssh_ip',"")
    NewTunnel["ssh_port"] = JsonConfig.get('ssh_port',22)
    NewTunnel["ssh_user"] = JsonConfig.get('ssh_user',"root")
    NewTunnel["authentication"] = JsonConfig.get('authentication',"")
    NewTunnel["password"] = JsonConfig.get('password',"")
    NewTunnel["key_path"] = JsonConfig.get('key_path',"")
    NewTunnel["Type"] = JsonConfig.get('Type',"")
    NewTunnel["Source_Server"] = JsonConfig.get('Source_Server',"localhost")
    NewTunnel["Source_port"] = JsonConfig.get('Source_port',0)
    NewTunnel["FinalPort"] = JsonConfig.get('FinalPort',0)
    NewTunnel["Highly_Restricted_Networks"] = {}
    NewTunnel["Highly_Restricted_Networks"]["Enable"] = JsonConfig.get('Highly_Restricted_Networks',{}).get('Enable',False)
    NewTunnel["Highly_Restricted_Networks"]["MonitorPort"] = JsonConfig.get('Highly_Restricted_Networks',{}).get('MonitorPort',0)
    NewTunnel["Highly_Restricted_Networks"]["ExitOnForwardFailure"] = JsonConfig.get('Highly_Restricted_Networks',{}).get('ExitOnForwardFailure','yes')
    NewTunnel["Highly_Restricted_Networks"]["ServerAliveInterval"] = JsonConfig.get('Highly_Restricted_Networks',{}).get('ServerAliveInterval',0)
    NewTunnel["Highly_Restricted_Networks"]["ServerAliveCountMax"] = JsonConfig.get('Highly_Restricted_Networks',{}).get('ServerAliveCountMax',0)
    context.user_data['tunnel_list'][TunnelCode] = NewTunnel
    context.user_data['tunnel_list'][TunnelCode]['pid'] = ""
    context.user_data['tunnel_list'][TunnelCode]['status'] = False
    context.user_data['tunnel_list'][TunnelCode]['is_active'] = False
    return True,NewTunnel
    



if __name__ == "__main__":           
    print(f"You should not run this file directly")
