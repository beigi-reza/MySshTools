#! /usr/bin/python3

import lib.BaseFunction
import tunnel as tu
import concurrent.futures
from datetime import datetime, timedelta
from tunnel import ( 
    TUNNEL_LIST
)


def autostart(TUNNEL_LIST):
    with concurrent.futures.ProcessPoolExecutor() as executor:    
#        for tunnel in TUNNEL_LIST:
#            future_to_id = executor.submit(tu.FnAutorestartTunnel(tunnel))    
#            tu.FnStartTunnel(tunnel)
        
        future_to_id = {executor.submit(tu.FnAutoRestartTunnel, tunnel): tunnel for tunnel in TUNNEL_LIST}
        #future_to_id = {executor.submit(worker_process, i): i for i in range(num_processes)}

        for future in concurrent.futures.as_completed(future_to_id):
            process_id = future_to_id[future]
            try:
                result = future.result()
                print(f"Received: {result}")
            except Exception as e:
                print(f"Process {process_id} generated an exception: {e}")



if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _LineLog = f"### {timestamp},Trying Started Tunnel as Keep Alive Mode ..."
    print (f"{_LineLog}")
    tu.SaveLogWebsite(_LineLog)
    autostart(TUNNEL_LIST)