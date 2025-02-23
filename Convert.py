import lib.BaseFunction
import os
import json

current_directory = os.path.dirname(os.path.realpath(__file__))

OldJsonListFile = os.path.join(current_directory,'conf/old.json')
OldJsonList = lib.BaseFunction.LoadJsonFile(OldJsonListFile)



SERVERS = OldJsonList['servers']

def CreateNewFormatJson(Servers):
    NewServerLIst = []
    for _ in Servers:
        _serverDict = {}
        _serverDict["ServerName"] = _["server_name"]
        _serverDict["IP"] = _["IP"]
        _serverDict["Port"] = _["ssh_port"]
        _serverDict["User"] = _["ssh_user"]
        _serverDict["Tags"] = [_["alias"]]
        _serverDict["Code"] = _["code"]
        _serverDict["Group"] = _["Group"]
        _serverDict["Icon"] = ""
        NewServerLIst.append(_serverDict)
    return NewServerLIst
    

def SaveNewJson(FileName,JsonVar):
    try:
        with open(FileName, 'w') as json_file:
            json.dump(JsonVar, json_file, indent=4)
    except Exception as e:
            print(f"Error saving dictionary to {FileName}: {e}")



NewServerLIst = CreateNewFormatJson(SERVERS)
NewServerDict = {}
NewServerDict.update({"servers":NewServerLIst})
PathFile = os.path.join(current_directory,'conf/ServerList.json')

SaveNewJson(FileName=PathFile,JsonVar=NewServerDict)

