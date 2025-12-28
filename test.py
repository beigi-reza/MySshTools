import lib.ServiceManagment as ServiceManagment
import os


current_directory = os.path.dirname(os.path.realpath(__file__))

ServiceName = 'keep-alive'
ServiceDiscription = 'Keep Alive Service'
ExecStart = '/usr/bin/python3 /path/to/your/script.py'
User = 'root'
WorkingDir = '/path/to/your'


