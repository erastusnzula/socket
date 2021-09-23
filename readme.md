Socket
======

Description
===========
```
* Allows users to send cmd commands to  connected clients.

```

Packages
========
```
* import os.
* import socket.
* import threading.
* import subprocess.
* from queue import Queue.
```

How it works
============
```
* Run the server and client file on separate computers.
* On server side:
    - Type connections to list all connected clients.
    - Type connect + index number of client to connect.

* Once connected send cmd commands like dir, mkdir, etc.

* Type exit to disconnect from the client.
```