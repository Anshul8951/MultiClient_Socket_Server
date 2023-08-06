import socket
import threading
import time
import json
import uuid
from datetime import datetime
import sys
import os
import tkinter as tk

if getattr(sys, 'frozen', False):  # Check if running as executable
    # Get the base directory where the executable is located
    base_dir = os.path.dirname(sys.executable)
else:
    # If running as a script, use the script's directory
    base_dir = os.path.dirname(__file__)

config_file_path = os.path.join(base_dir, "config.txt")


# Read the configuration file
def read_config_file():
    # Read the configuration file and return its contents as a dictionary
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
    return config_data

config = read_config_file()

# Set up the network connection
HOST_IP = config['host_ip']
HOST_PORT = config['host_port']
SIZE = config['size']
FORMAT = config["format"]
EVENT = config["event"]
PING = config["ping"]
CHECK_INTERVAL = config["check_interval"]
PC1_IP = config['pc1_ip']
PC2_IP = config['pc2_ip']
ADDR = (HOST_IP, HOST_PORT)
URL = config["url"]
alive_connections = {PC1_IP : False, PC2_IP : False} #To get the status of each connection based on IP address
client_sockets = dict() #To get the client connection details to interact with it based on the IP address
server_on = dict() #To get the server connection details to close it when required
connection_status = {True: "Connected", False: "Disconnected"} #Display the right message based on connection status
status_label = dict() #To get the UI label element of the corresponding IP address 

def on_closing(root):
    #Retrieving the server connection details to close it
    server = server_on['status']
    server.close()
    root.destroy()

# Method to check if the connection is alive
def is_connection_alive(conn):
    try:
        conn.send(PING.encode(FORMAT))
        return True
    except:
        return False

#Method to continuously monitor the connection to the client
def monitor_client_connection(conn, addr):
    print(f"[MONITOR CONNECTION] {addr} Connection being monitored every {CHECK_INTERVAL} secs")
    
    while is_connection_alive(conn):
        time.sleep(CHECK_INTERVAL)

    #Updating the connection status and the UI labels based on the IP address
    alive_connections[addr[0]] = False
    txt_label = status_label[addr[0]]
    txt_label.config(text = connection_status[False])

    print(f"[MONITOR CONNECTION] {addr} disconnected.")

#Method to verify if the PC is connected to host before sending event and then send event
def verify_and_send(addr):
    if(alive_connections[addr]):
        print(f"[SEND EVENT] Sending Event to {addr}")
        conn = client_sockets[addr]
        try:
            conn.send(EVENT.encode(FORMAT))
            print(f"[SEND EVENT] Sending Event to {addr} successful")
        except Exception as e:
            print(f"[SEND EVENT] Error occurred while sending/receiving: {e}")
    else:
        print(f"[SEND EVENT] Unable to send event as PC is disconnected")

#Start server and accept new connections from client and then monitor them
def start_server():

    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST_IP}:{HOST_PORT}")
    server_on['status'] = server

    while True:
        conn, addr = server.accept()
        print(f"{conn} Connected to the server")
        alive_connections[addr[0]] = True
        txt_label = status_label[addr[0]]
        txt_label.config(text = connection_status[True])
        client_sockets[addr[0]] = conn
        thread1 = threading.Thread(target=monitor_client_connection, args=(conn, addr))
        thread1.start()
        
    server.close()


def main():

    # Create the main application window
    root = tk.Tk()
    root.title("Host PC")

    # Set the window size (width x height)
    window_width = 400
    window_height = 300
    root.geometry(f"{window_width}x{window_height}")

    #Creating a thread to continuously accept new connections from client and then monitor them
    thread = threading.Thread(target=start_server)
    thread.start()

    # Create the buttons
    txt_label_1 = tk.Label(root, text=connection_status[False], font=("Arial", 16))
    button1 = tk.Button(root, text="Send event to PC 1", command=lambda: verify_and_send(PC1_IP))
    txt_label_2 = tk.Label(root, text=connection_status[False], font=("Arial", 16))
    button2 = tk.Button(root, text="Send event to PC 2", command=lambda: verify_and_send(PC2_IP))
    #button3 = tk.Button(root, text="POST", command=button3_clicked)
    #button4 = tk.Button(root, text="Exit", command=button3_clicked)

    #Creating a map to update status labels of each connection
    status_label[PC1_IP] = txt_label_1
    status_label[PC2_IP] = txt_label_2

    # Pack the buttons to place them in the window
    txt_label_1.pack(pady=10)
    button1.pack(pady=10)
    txt_label_2.pack(pady=10)
    button2.pack(pady=10)
    #button3.pack(pady=10)

    # Bind the on_closing() function to the window close event
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()



