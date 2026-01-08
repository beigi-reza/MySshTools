from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import tunnel as TunnelManagment
from tunnel import current_directory,TUNNEL_LIST,LOG_PATH,TunnelJsonFilePath
import lib.BaseFunction
import os
import zipfile
# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

##################
ServerListPath = os.path.join(current_directory, "conf/UserConfig.json")
UserJson= lib.BaseFunction.LoadJsonFile(JsonFile=ServerListPath,Verbus=False,ReternValueForFileNotFound={}) 
USER_DICT = UserJson.get("users", {})


# Initialize FastAPI
app = FastAPI(
    title="🦑 SSH Tunnel Managment API",
    description="🦨 ",
    version="1.1.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


####################################
#########   Models
####################################

class UserLogin(BaseModel):
    user: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    user: str
    full_name: str
    is_active: bool

class UserCreate(BaseModel):
    user: str
    password: str
    full_name: str
    Group: Optional[str] = "Myuser"

class RunMode(BaseModel):
    DebugMode: bool = False

class TunnelStatus(BaseModel):
    code: str
    detail: Optional[str] = None
    status: bool

class TunnelEnableorDisable(BaseModel):
    message: str
    status: bool

class StatusResponse(BaseModel):
    detail: Optional[str] = None
    status: bool

class CloneTunnelRequest(BaseModel):
    TunnelCode: str

class TunnelLogsLineNumber(BaseModel):
    LogNumber: int = 50

class TunnelTemplate(BaseModel):
    Code: str
    Name: Optional[str] = "NewTunnel"
    Type: Optional[str] = "local"
    ssh_ip: str
    ssh_port: Optional[int] = 22
    ssh_user: Optional[str] = "root"
    Source_Server_IP: Optional[str] = "127.0.0.1"
    Source_Server_Port: int
    is_active: Optional[bool] = False
    Keep_Alive: Optional[bool] = False
    Authentication_method: Optional[str] = None
    password: Optional[str] = None
    private_key_path: Optional[str] = None
    Highly_Restricted_Networks_Status: Optional[bool] = False
    ExitOnForwardFailure: Optional[str] = 'no'
    ServerAliveInterval: Optional[int] = 1
    ServerAliveCountMax: Optional[int] = 3
    MonitorPort: Optional[int] = 0

class TunnelUpdate(BaseModel):    
    Name: Optional[str] = None
    Type: Optional[str] = None
    ssh_ip: Optional[str] = None
    ssh_port: Optional[int] = None
    ssh_user: Optional[str] = None
    Source_Server: Optional[str] = None
    Source_port: Optional[int] = None
    FinalPort: Optional[int] = None
    is_active: Optional[bool] = None
    Keep_Alive: Optional[bool] = None
    authentication: Optional[str] = None
    password: Optional[str] = None
    key_path: Optional[str] = None
    #
    Highly_Restricted_Networks_Enable : Optional[bool] = None    
    ExitOnForwardFailure: Optional[str] = None
    ServerAliveInterval: Optional[int] = None
    ServerAliveCountMax: Optional[int] = None
    MonitorPort: Optional[int] = None
    
class AuthenticationMode(BaseModel):
    authentication : str
    password: Optional[str] = None
    key_path: Optional[str] = None
####################################
#########   Helper functions
####################################

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    
    except Exception:
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    User = payload.get("sub")
    if User is None or User not in USER_DICT:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return USER_DICT[User]

####################################
#########   Routes
####################################

@app.get("/", tags=["Root"])
async def info():
    """Welcome endpoint"""
    return {"message": "SSH Tunnel Managment API", "Swagger": "/Swager", "Redoc": "/redoc"}


@app.post("/login", response_model=Token, tags=["Authentication"])
async def login(user_credentials: UserLogin):
    """Login and receive JWT token"""    
    user = USER_DICT.get(user_credentials.user)
    UserPassword = user_credentials.password
    HashedPassword = user.get("password") if user else None
    if not user or not verify_password(plain_password=UserPassword, hashed_password=HashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user_credentials.user})
    return {"access_token": access_token, "token_type": "bearer"}

#@app.post("/register", response_model=User, tags=["Authentication"])
#async def register(user: UserCreate):
#    """Register a new user"""
#    #if user.user in fake_users_db:
#    #    raise HTTPException(status_code=400, detail="Email already registered")
#    
#    hashed_password = get_password_hash(user.password)
##    fake_users_db = {}
##    fake_users_db[user.user] = {
##        "email": user.email,
##        "hashed_password": hashed_password,
##        "full_name": user.full_name,
##        "is_active": True,
##        "Group": user.Group
##    }
#    return User(email=user.user, full_name=user.full_name, is_active=True)

@app.get("/GetAllTunnels", tags=["Tunnels"])
async def get_all_tunnels(current_user: dict = Depends(get_current_user)):    
    """Get all SSH tunnels"""    
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    return _TUNNEL_LIST

@app.get("/GetTunnelbyCode/{code}", tags=["Tunnels"])
async def get_tunnel_by_code(code: str, current_user: dict = Depends(get_current_user)):    
    """Get SSH tunnel by code"""
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()    
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            return tunnel
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.get("/GetStatusAllTunnels", tags=["Tunnels"])
async def get_status_all_tunnels(current_user: dict = Depends(get_current_user)):
    """Get status of all SSH tunnels"""        
    status_list = TunnelManagment.GetStatusAllTunnel()
    return status_list
    
@app.get("/GetStatusTunnelbyCode/{code}", tags=["Tunnels"])
async def get_status_tunnel_by_code(code: str, current_user: dict = Depends(get_current_user)):
    """Get status of SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            status = TunnelManagment.GetTunnelStatusByDict(tunnel)
            return status
    raise HTTPException(status_code=404, detail="Tunnel not found")


@app.post("/StartTunnelbyCode/{code}",response_model=TunnelStatus, tags=["Tunnels"])
async def start_tunnel_by_code(code: str,run_mode:RunMode, current_user: dict = Depends(get_current_user)):
    """Start SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    DebugMode = run_mode.DebugMode    
    for _t in _TUNNEL_LIST:
        _tunnel = _TUNNEL_LIST[_t]
        Code = _tunnel.get('Code','')
        if Code.strip().lower() == code.strip().lower():            
            if TunnelManagment.CheckStatusTunnel(_tunnel)[0]:            
                msg = f"❕ Tunnel {_tunnel['Name']} is already running."                
                TnlStatus = (True,msg)
                break
            TnlStatus = TunnelManagment.FnStartTunnel(TunnleDict=_tunnel,DebugMode=DebugMode)
            break
    else:
        raise HTTPException(status_code=404, detail="Tunnel not found")
        
    return {"code": _tunnel.get("Code",""),            
            "status": TnlStatus[0],
            "msg": TnlStatus[1]
            }

@app.post("/StartAllTunnels", tags=["Tunnels"])
async def start_all_tunnels(current_user: dict = Depends(get_current_user)):
    """Start all SSH tunnels"""            
    status_list = TunnelManagment.StartAllTunnel(ReturnResualt=True)
    return status_list

@app.post("/StopTunnelbyCode/{code}",response_model=TunnelStatus, tags=["Tunnels"])
async def stop_tunnel_by_code(code: str, current_user: dict = Depends(get_current_user)):
    """Stop SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()    
    for _t in _TUNNEL_LIST:
        _tunnel = _TUNNEL_LIST[_t]
        Code = _tunnel.get('Code','')
        if Code.strip().lower() == code.strip().lower():            
            rst = TunnelManagment.CheckStatusTunnel(_tunnel)
            if rst[0] == False: 
                msg = f"❕ Tunnel {_tunnel['Name']} is not running."                
                TnlStatus = (True,msg)
                break
            TnlStatus = TunnelManagment.KillProcessByPID(pid=rst[2])
            break
    else:
        raise HTTPException(status_code=404, detail="Tunnel not found")
 
    return {"code": _tunnel.get("Code",""),            
            "status": TnlStatus[0],
            "msg": TnlStatus[1]
            }


@app.post("/StopAllTunnels", tags=["Tunnels"])
async def stop_all_tunnels(current_user: dict = Depends(get_current_user)):
    """Stop all SSH tunnels"""            
    rstDict = TunnelManagment.DropAllSShTunnel(ReturnResualt=True)    
    return rstDict

@app.post("/restartTunnelbyCode/{code}",response_model=StatusResponse, tags=["Tunnels"])
async def restart_tunnel_by_code(code: str,run_mode:RunMode, current_user: dict = Depends(get_current_user)):
    """Restart SSH tunnel by code"""            
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        _tunnel = _TUNNEL_LIST[_t]
        Code = _tunnel.get('Code','')
        if Code.strip().lower() == code.strip().lower():            
            Rst = TunnelManagment.RestartTunnel(TunnelDict=_tunnel)
            return {"detail": Rst[1],
                    "status": Rst[0]
                    }
    else:
        raise HTTPException(status_code=404, detail="Tunnel not found")
        

@app.post("/AddNewTunnel",response_model=StatusResponse, tags=["Tunnel Managment"])
async def add_new_tunnel(new_tunnel: TunnelTemplate, current_user: dict = Depends(get_current_user)):
    """Add a new SSH tunnel"""
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    NewCode = new_tunnel.Code.strip().lower()
    for _t in _TUNNEL_LIST:        
        if _t.strip().lower() == NewCode:
            return {"detail": f"Tunnel with code {new_tunnel.Code} already exists.",                    
                    "status": False}
        elif new_tunnel.ssh_ip.lower() == "string":
            return {"detail": f"Invalid SSH IP address.",                    
                    "status": False}
        elif new_tunnel.Source_Server_Port <=0 or new_tunnel.Source_Server_Port >65535:
            return {"detail": f"Invalid Source Server Port number.",                    
                    "status": False}
        elif new_tunnel.ssh_port <=0 or new_tunnel.ssh_port >65535:
            return {"detail": f"Invalid SSH Port number.",                    
                    "status": False}
        elif new_tunnel.Authentication_method not in ["password","private_key",None,""]:
            return {"detail": f"Invalid Authentication method. Choose 'password', 'private_key' or ...",
                    "status": False}
        
    _TUNNEL_LIST[NewCode] = {}
    _TUNNEL_LIST[NewCode]["Name"] = new_tunnel.Name
    _TUNNEL_LIST[NewCode]["Code"] = new_tunnel.Code
    _TUNNEL_LIST[NewCode]["Type"] = new_tunnel.Type
    _TUNNEL_LIST[NewCode]["ssh_ip"] = new_tunnel.ssh_ip
    _TUNNEL_LIST[NewCode]["ssh_port"] = new_tunnel.ssh_port
    _TUNNEL_LIST[NewCode]["ssh_user"] = new_tunnel.ssh_user
    _TUNNEL_LIST[NewCode]["Source_Server"] = new_tunnel.Source_Server_IP
    _TUNNEL_LIST[NewCode]["Source_port"] = new_tunnel.Source_Server_Port
    _TUNNEL_LIST[NewCode]["is_active"] = new_tunnel.is_active
    _TUNNEL_LIST[NewCode]["Keep_Alive"] = new_tunnel.Keep_Alive
    _TUNNEL_LIST[NewCode]["Authentication_method"] = new_tunnel.Authentication_method
    _TUNNEL_LIST[NewCode]["password"] = new_tunnel.password
    _TUNNEL_LIST[NewCode]["private_key_path"] = new_tunnel.private_key_path
    _TUNNEL_LIST[NewCode]["status"] = False        
    _TUNNEL_LIST[NewCode]["Highly_Restricted_Networks"] ={}
    _TUNNEL_LIST[NewCode]["Highly_Restricted_Networks"]["Enable"] = new_tunnel.Highly_Restricted_Networks_Status
    _TUNNEL_LIST[NewCode]["Highly_Restricted_Networks"]["ExitOnForwardFailure"] = new_tunnel.ExitOnForwardFailure
    _TUNNEL_LIST[NewCode]["Highly_Restricted_Networks"]["ServerAliveInterval"] = new_tunnel.ServerAliveInterval
    _TUNNEL_LIST[NewCode]["Highly_Restricted_Networks"]["ServerAliveCountMax"] = new_tunnel.ServerAliveCountMax
    _TUNNEL_LIST[NewCode]["Highly_Restricted_Networks"]["MonitorPort"] = new_tunnel.MonitorPort
    _TUNNEL_LIST
    _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=TunnelJsonFilePath,JsonData=_TUNNEL_LIST,Verbus=False)
    if _Rst[0]:
        return {"detail": f"Tunnel with code {NewCode} has been added. \n New Tunnel disable by default.",
                "status": True}
    else:
        return {"detail": f"Error in add new tunnel: {_Rst[1]}",
                "status": False}

@app.post("/DisableTunnelbyCode/{code}",response_model=TunnelEnableorDisable, tags=["Tunnel Managment"])
async def disable_tunnel_by_code(code: str, current_user: dict = Depends(get_current_user)):
    """Disable SSH tunnel by code"""        
    _Rst = TunnelManagment.EnableorDisableTunnelByCode(TunnelCode=code,Changeto=False)
    if _Rst:
        return {"message": f"Tunnel with code {code} has been disabled.",
                "status": True}
    else:
        return {"message": f"Error in disable tunnel{_Rst[1]}",
                "status": False}

@app.post("/EnableTunnelbyCode/{code}",response_model=TunnelEnableorDisable, tags=["Tunnel Managment"])
async def enable_tunnel_by_code(code: str, current_user: dict = Depends(get_current_user)):
    """Enable SSH tunnel by code"""        
    _Rst = TunnelManagment.EnableorDisableTunnelByCode(TunnelCode=code,Changeto=True)
    if _Rst:
        return {"message": f"Tunnel with code {code} has been enabled.",
                "status": True}
    else:
        return {"message": f"Error in enable tunnel{_Rst[1]}",
                "status": False}


@app.post("/CloneTunnelbyCode/{code}",response_model=StatusResponse, tags=["Tunnel Managment"])
async def clone_tunnel_by_code(code: str,NewTunnelCode = CloneTunnelRequest, current_user: dict = Depends(get_current_user)):
    """Clone SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:        
        if _t.strip().lower() == code.strip().lower():            
            _Rst = TunnelManagment.FnCloneTunnelbyCode(TunnelCode4Clone=code,NewTunnelCode=NewTunnelCode)
            if _Rst[0]:
                return {"detail": f"Tunnel with code {code} has been cloned to {NewTunnelCode}.",
                        "status": True}
            else:
                return {"detail": f"Error in clone tunnel: {_Rst[1]}",
                        "status": False}
    raise HTTPException(status_code=404, detail="Tunnel not found")
    

@app.delete("/DeleteTunnelbyCode/{code}",response_model=StatusResponse, tags=["Tunnel Managment"])
async def delete_tunnel_by_code(code: str, current_user: dict = Depends(get_current_user)):
    """Delete SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        if _t == code:
            TunnelDict = _TUNNEL_LIST[_t]
            rst = TunnelManagment.CheckStatusTunnel(TunnelDict)
            if rst[0]:
                TunnelManagment.KillProcessByPID(pid=rst[2])            
            DeleteRst = TunnelManagment.DeleteTunnel(TunnelDict=TunnelDict,NoWait=True)
            if DeleteRst :
                return {"detail": f"Tunnel with code {code} has been deleted.",
                        "status": True}
            else:
                return {"detail": f"Error in delete tunnel: {_Rst[1]}",
                        "status": False}    
    raise HTTPException(status_code=404, detail="Tunnel not found")

###########################################
##########   Debug Mode routes
###########################################

@app.get("/debug/GetTunnelStatus/{code}", tags=["Debug"])
async def debug_get_tunnel_status(code: str, current_user: dict = Depends(get_current_user)):
    """Debug: Get SSH tunnel status by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            status = TunnelManagment.Fn_getTunnelStatus(TunnelDict=tunnel)
            return status
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.get("/StartTunnelInDebugMode/{code}", tags=["Debug"])
async def debug_run_tunnel_in_debug_mode(code: str, current_user: dict = Depends(get_current_user)):
    """Debug: Run SSH tunnel in debug mode by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            rst = TunnelManagment.CheckStatusTunnel(tunnel)
            if rst[0]: 
                TunnelManagment.KillProcessByPID(pid=rst[2])
            status = TunnelManagment.FnStartTunnel(TunnleDict=tunnel,DebugMode=True)
            RsrLog = TunnelManagment.GetTunnelLogDetails(TunnelDict=tunnel)
            if RsrLog[0]:
                Logs = RsrLog[1]
            else:
                Logs = f"Failed to get logs.\n {RsrLog[1]}"

            if status[1] == '':
                statusMsg = "Tunnel started in debug mode."
            else:
                statusMsg = status[1]
            return {"is_active": status[0], "TunnelMsg": statusMsg, "Logs": Logs}
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.get("/GetTunnelCommand/{code}", tags=["Debug"])
async def debug_get_tunnel_command(code: str, current_user: dict = Depends(get_current_user)):
    """Debug: Get SSH tunnel command by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            CommandLIST = TunnelManagment.CreateCommamd(TunnleDict=tunnel,TypeOfTunnel=tunnel["Type"].lower(),DebugMode=False)
            FullCommandLine = ''            
            for _ in CommandLIST:
                FullCommandLine += f' {_}'
    
            FullCommandLine = FullCommandLine.strip()    
            return {"CommandLine": FullCommandLine}
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.get("/GetTunnelJson/{code}", tags=["Debug"])
async def debug_get_tunnel_json(code: str, current_user: dict = Depends(get_current_user)):
    """Debug: Get SSH tunnel JSON by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            return tunnel
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.post("/GetTunnelLogs/{code}",tags=["Debug"])
async def debug_get_tunnel_logs(code: str, Log_Number:TunnelLogsLineNumber,current_user: dict = Depends(get_current_user)):
    _lNumber = Log_Number.LogNumber
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            RsrLog = TunnelManagment.GetTunnelLogDetails(TunnelDict=tunnel,NumLines=_lNumber)
            if RsrLog[0]:
                Logs = RsrLog[1]
            else:
                Logs = f"Failed to get logs.\n {RsrLog[1]}"
            return {"Logs": Logs}
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.post("/ClearTunnelLogs/{code}",tags=["Debug"])
async def debug_clear_tunnel_logs(code: str, current_user: dict = Depends(get_current_user)):
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            RsrLog = TunnelManagment.ClearTunnleLog(TunnelCode=code)
            if RsrLog[0]:
                return {"detail": "Logs cleared successfully.", "status": True}
            else:
                return {"detail": f"Failed to clear logs.\n {RsrLog[1]}", "status": False}
    raise HTTPException(status_code=404, detail="Tunnel not found")

@app.post("/DownloadTunnelLogs/{code}",tags=["Debug"])
async def debug_download_tunnel_logs(code: str, current_user: dict = Depends(get_current_user)):
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        tunnel = _TUNNEL_LIST[_t]
        if tunnel["Code"] == code:
            LogFilePath = f"{LOG_PATH}/{_t}.log"
            zip_path = f"/tmp/{code}_logs.zip"
            if not os.path.exists(LogFilePath):
                raise HTTPException(status_code=404, detail="Log Files not found")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(LogFilePath, arcname=os.path.basename(LogFilePath))
        
            return FileResponse(
                zip_path,
                media_type="application/zip",
                filename=zip_path.split("/")[-1]
            )                        
            #return {"zip_file_path": zip_path}
    raise HTTPException(status_code=404, detail="Tunnel not found")


@app.patch("/UpdateTunnelbyCode/{code}",response_model=StatusResponse, tags=["Tunnel Managment"])
async def update_tunnel_by_code(code: str, updated_tunnel: TunnelUpdate, current_user: dict = Depends(get_current_user)):
    """Update SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    ALLOWED_FIELDS = {"Name", 
                        "Type",
                        "ssh_ip",
                        "ssh_port",
                        "ssh_user",
                        "FinalPort",
                        "Source_Server",
                        "Source_port",
                        "Keep_Alive",
                        "is_active",
                        "authentication",
                        "password",
                        "key_path",
                        "Highly_Restricted_Networks_Enable",                        
                        "ExitOnForwardFailure",
                        "ServerAliveInterval",
                        "ServerAliveCountMax",
                        "MonitorPort"
                        }
    Updated = False
    for _t in _TUNNEL_LIST:
        if _t.strip().lower() == code.strip().lower():            
            TunnelDict = _TUNNEL_LIST[_t]
            
            update_data = updated_tunnel.model_dump(exclude_unset=True)            

            if not update_data:
                raise HTTPException(status_code=400, detail="No fields provided for update")

            for key, value in update_data.items():
                if type(value) == str:
                    if value.lower().strip() == "string":
                        continue                
                if key in ALLOWED_FIELDS:
                    ## Check for ssh_port and Source_port validity
                    if key in ["ssh_port","Source_port","FinalPort"]:
                        if value <=0 or value >65535:
                            return {"detail": f"Invalid port number for {key}.",
                                    "status": False}
                        elif type(value) != int:
                            try:
                                value = int(value)
                            except Exception:
                                return {"detail": f"Invalid port number for {key}.",
                                        "status": False}                            
                    elif key in ["is_active","Keep_Alive"]:
                        if type(value) != bool:
                            if str(value).strip().lower() in ["true","1","yes"]:
                                value = True
                            elif str(value).strip().lower() in ["false","0","no"]:
                                value = False
                            else:
                                return {"detail": f"Invalid boolean value for {key}.",
                                        "status": False}                        
                    elif key == "authentication":
                        if value not in ["password","private_key",None,""]:
                            return {"detail": f"Invalid Authentication method. Choose 'password' or 'private_key' or ...",
                                    "status": False}
                    elif key == "key_path":
                        if not os.path.isfile(value):
                            return {"detail": f"Private key file not found at ( {value} ).",
                                    "status": False}
                    elif key == "Type":
                        if value.lower().strip() not in ["local","remote","dynamic"]:
                            return {"detail": f"Invalid tunnel type. Choose 'local', 'remote' or 'dynamic'.",
                                    "status": False}
                        else:
                            value = value.lower().strip()

                    #TunnelDict[key] = value
                    if key == "Highly_Restricted_Networks_Enable":
                        key = "Enable"
                    if key in ["Enable","ExitOnForwardFailure","ServerAliveInterval","ServerAliveCountMax","MonitorPort"]:
                        if key == "ExitOnForwardFailure":                            
                            if value.lower().strip() not in ['yes','no','true','false','1','0']:
                                if type(value) == bool:
                                    if value:
                                        value = 'yes'
                                    else:
                                        value = 'no'
                                else:
                                    return {"detail": f"Invalid value for {key}. Choose 'yes' or 'no'.",
                                            "status": False}
                            else:
                                if str(value).strip().lower() in ['yes','true','1']:
                                    value = 'yes'
                                elif str(value).strip().lower() in ['no','false','0']:
                                    value = 'no'
                                else:
                                    return {"detail": f"Invalid value for {key}. Choose 'yes' or 'no'.",
                                            "status": False}
                            value = value.lower().strip()
                        if _TUNNEL_LIST[_t]["Highly_Restricted_Networks"][key] != value:
                            Updated = True
                            _TUNNEL_LIST[_t]["Highly_Restricted_Networks"][key] = value
                    else:
                        if _TUNNEL_LIST[_t][key] != value:
                            Updated = True
                            _TUNNEL_LIST[_t][key] = value
            if Updated:
                _Rst = lib.BaseFunction.SaveJsonFile(JsonFile=TunnelJsonFilePath,JsonData=_TUNNEL_LIST,Verbus=False)
            else:
                return {"detail": f"No changes detected for tunnel with code {code}.",
                        "status": False}
            if _Rst[0]:
                return {"detail": f"Tunnel with code {code} has been updated.",
                        "status": True}
            else:
                return {"detail": f"Error in update tunnel: {_Rst[1]}",
                        "status": False}    
    raise HTTPException(status_code=404, detail="Tunnel not found")


@app.post("/SetAuthenticationMode/{code}",response_model=StatusResponse, tags=["Tunnel Authentication Managment"])
async def Set_authentication_method(code: str, authentication_mode: AuthenticationMode, current_user: dict = Depends(get_current_user)):    
    """Set authentication method for SSH tunnel by code"""        
    _TUNNEL_LIST = TunnelManagment.RefreshTunnelList()
    for _t in _TUNNEL_LIST:
        if _t.strip().lower() == code.strip().lower():            
            #TunnelDict = _TUNNEL_LIST[_t]
            _Rst = TunnelManagment.FnSetAuthenticationMode(_TempTunnelList = _TUNNEL_LIST,                                                    
                                                    TunnelCode=code.lower().strip(),
                                                    AuthenticationMode=authentication_mode.authentication,
                                                    Password=authentication_mode.password,
                                                    KeyPath=authentication_mode.key_path)
            if _Rst[0]:
                _TUNNEL_LIST = _Rst[2]
                if lib.BaseFunction.SaveJsonFile(JsonFile=TunnelJsonFilePath,JsonData=_TUNNEL_LIST,Verbus=False):
                    return {"detail": f"Authentication method for tunnel with code {code} has been updated.",
                            "status": True}
                else:
                    return {"detail": f"Error in update tunnel authentication method: {_Rst[1]}",
                            "status": False}
            else:
                return {"detail": f"Error in update tunnel authentication method: {_Rst[1]}",
                        "status": False}            
    raise HTTPException(status_code=404, detail="Tunnel not found")
    

####################################
#########   Run the app
####################################

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)