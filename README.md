# FLAME - FLask Auto Miko Engine

Throwing CLI commands at Cisco IOS devices from your browser!

As the backronym suggets, this uses the Flask web framework for the front-end and Netmiko to interact with devices on the back-end.

![Screenshot](/screenshot.png?raw=true)

Usage
----
- Devices - Contains the IPs to interact with (these are stored in devices.txt)
- Commands - Contains the commands to be sent (these are stored in commands.txt)
- ChangePass - Utilises devices.txt to change SSH into each device and change the current user and enable passwords
- ConfigThrow - Utilises devices.txt and commands.txt to SSH into each device and carry out the commands listed and save the output


License
----
MIT