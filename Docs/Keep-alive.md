# Keep Alibe Mode

## Run as Service

### 1 - Create a service file:

create `keep-alive.service` on `/etc/systemd/system/`

```bash
vim /etc/systemd/system/keep-alive.service
```


### 2 - Add the following content to the file:

```
[Unit]
Description=Keep Alive Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/MySshTools
ExecStart=/usr/bin/python3 /root/MySshTools/keep-alive.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3 - Enable and start the service:


```bash
sudo systemctl daemon-reload
sudo systemctl enable keep-alive.service
sudo systemctl start keep-alive.service
sudo systemctl status keep-alive.service
```