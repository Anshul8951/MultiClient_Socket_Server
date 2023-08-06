import socket
import json
import tkinter as tk
import queue
import threading
import time
import sys
import os

CONNECTED = 'Connected to server'
DISCONNECTED = 'Disconnected from server'
connection = {'connected': False}
client_conn = dict() #To get the client connection details to close it when required
PING = 'ping'
FORMAT = 'utf-8'

if getattr(sys, 'frozen', False):  # Check if running as executable
    # Get the base directory where the executable is located
    base_dir = os.path.dirname(sys.executable)
else:
    # If running as a script, use the script's directory
    base_dir = os.path.dirname(__file__)

config_file_path = os.path.join(base_dir, "config.txt")

def read_config_file():
    # Read the configuration file and return its contents as a dictionary
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

# Read the configuration file
config = read_config_file()

# Set up the network connection
HOST_IP = config['host_ip']
HOST_PORT = config['host_port']
SIZE = config['size']
FORMAT = config["format"]
EVENT = config["event"]
ADDR = (HOST_IP, HOST_PORT)
PING = config['ping']
FORMAT = config['format']
CHECK_INTERVAL = config['check_interval']

CONNECTED = 'Connected to server'
DISCONNECTED = 'Disconnected from server'
connection = {'connected': False}

def on_closing(root, text_label, connection_status_label):
    disconnect_from_server(text_label, connection_status_label)
    root.destroy()

# Method to check if the connection is alive
def is_connection_alive():
    client = client_conn['conn']
    try:
        client.send(PING.encode(FORMAT))
        return True
    except:
        return False

#Method to continuously monitor the connection to the client
def monitor_client_connection(text_label, connection_status_label):
    
    while is_connection_alive():
        time.sleep(CHECK_INTERVAL)

    disconnect_from_server(text_label, connection_status_label)


#Receive events from Host PC
def recv_event(text_label):

    #Waiting to receive an event from the host
    connection['connected'] = True
    count = 0
    client = client_conn['conn']
    while connection['connected']:
        msg = client.recv(SIZE).decode(FORMAT)
        if(msg == EVENT):
            count = count + 1
            text_label.config(text=f"Event Received from Host {count} times")
            print("Event received from host")
    
def connect_to_server(text_label, connection_status_label):

    if(connection['connected'] == True):
        return
    
    #Connecting to Host
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {HOST_IP}:{HOST_PORT}")
    client_conn['conn'] = client

    text_label.config(text=f"Event Received from Host 0 times")
    connection_status_label.config(text = CONNECTED)

    #Creating a thread to monitor the connection status regularly
    thread = threading.Thread(target=monitor_client_connection, args = (text_label, connection_status_label))
    thread.start()

    #Creating a thread to handle any receive event from server
    thread1 = threading.Thread(target=recv_event, args = (text_label,))
    thread1.start()

def disconnect_from_server(text_label, connection_status_label):
    if(connection['connected'] == False):
        return
    client = client_conn['conn']
    client.close()
    text_label.config(text=f"Event Received from Host 0 times")
    connection_status_label.config(text = DISCONNECTED)
    connection['connected'] = False

def main():

    # Create the main application window
    root = tk.Tk()
    root.title("PC 1")

    # Set the window size (width x height)
    window_width = 400
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    connection_status_label = tk.Label(root, text=DISCONNECTED, font=("Arial", 16))

    # Create a label to display text
    text_label = tk.Label(root, text=f"Event Received from Host 0 times", font=("Arial", 16))

    #Connect to server
    connect = tk.Button(root, text="Connect to Server", command=lambda: connect_to_server(text_label, connection_status_label))

    #Disconnect from Server
    disconnect = tk.Button(root, text="Disconnect to Server", command=lambda: disconnect_from_server(text_label, connection_status_label))

    # Pack the label to place it in the window
    connection_status_label.pack(pady=50)
    connect.pack(pady=50)
    disconnect.pack(pady=50)
    text_label.pack(pady=50)    

    # Bind the on_closing() function to the window close event
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, text_label, connection_status_label))
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
