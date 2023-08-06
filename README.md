# Software Description:
A Windows 10 (x64) compatible software that will be deployed on three computers, each with distinct roles:

Computer 1 (Host/Server): This computer will act as the central host/server for the software system.
Computer 2 and Computer 3 (Gamer PCs): These two computers are identical and connected to the local network with static IP addresses. They will run VR games for customers using the machines and receive instructions from the host computer to initiate or halt games.

## LAN Communication:
A seamless Local Area Network (LAN) communication between the host and the gamer PCs. 
A visible message on each computer's screen to indicate successful communication. 
The communication status is regularly monitored every second using pinging.

Configuration File/Setting Page:
A configuration file (config.exe) for both client and server. This will allow users to easily set essential connection details for the devices:

On the Gamer PCs: Users can specify the static IP address of the host computer.
On the Host/Server: Users can set the static IP addresses of both gamer PCs.

## UI Element Trigger:
A simple user interface on the host's exe. A button within this interface that, when pressed, triggers a command (or an event) to be sent to the gamer PCs. This command leada to a change in a specific UI element, simulating the initiation of a game.

# Implementation
Done using Multi Client Socket programming with Server using multithreading.
The UI is built using tkinter.