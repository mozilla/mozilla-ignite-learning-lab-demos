# Mozilla Ignite Learning Lab 6: Software Defined Networking

Status: In-progress

So you want to get started with Software Defined Networking (SDN),
the future of networking?

This is a tutorial project you can use to get quickly up and running
with a homebrew SDN network at home.

Before you get started, check out our DIY video, where we build an OpenFlow
network in a suburban garage: http://example.com

## Pre-requisites

- 3-4 spare computers (desktops, laptops, Raspberry Pis)
- `ssh` on at least on of the computers (you'll want to use this computer for the 'setup' phase)
- Python 2.7 Installed on all computers: http://www.python.org/getit/
- A copy of this repository on all computers (may need a USB stick if you don't use git)
- This router, which this lab is designed for: http://www.amazon.com/TP-LINK-TL-WR1043ND-Ultimate-Wireless-Gigabit/dp/B002YLAUU8
- Pioneer spirit!

## Getting Set Up With the Right Firmware

The first part of our lab involves putting the right firmware
on our router. The firmware we're using is a special flavor
of OpenWRT, an open source operating system for routers. 
It has OpenFlow 1.0 preinstalled.

1. Power up your router
1. Connect a computer to it via ethernet to one of the router's LAN ports
1. Navigate to the router's admin panel: 192.168.0.1
1. Login in with username 'admin' and password 'admin'
1. Head to System Tools -> Firmware upgrade
1. For the firmware file upload, select misc/firmware/ofwrt-attitude-adj-pantou.bin in this repository
1. Upload, and wait a few minutes. There will no longer be a web interface
1. Telnet into your router: `telnet 192.168.1.1`
1. Set a password for the root account (follow the prompts): `passwd`
1. Exit: `exit`
1. Log in via SSH: `ssh root@192.168.1.1`
1. Enter the password that you set 3 steps ago
1. Are you in? Nice!

## Configuring the router

1. 

## Help!
"Let's get our computers and our router ready for our OpenFlow experiment. Part of this involves installing custom openflow-enabled firmware on our TP-link router. If you happen to be using a different openflow-enabled router, you can skip that part of the setup."
1. Get project files, Copy project files to all computers
    "The first thing we need to do is get a copy of this lab's files on each of our computers. You can head to https://github.com/mozilla/mozilla-ignite-learning-lab-demos/lab-6-7-openflow and download
    a zip file. Then extract those files onto each of the computers we'll be using."
1. Disconnect all from internet
    "Now we'll disconnect all of our computers from the internet. This means turning of wireless networking and unplugging any existing ethernet cables"
1. Plug in router
    "Now let's power up your router. You can do this by simple plugging it in!"
1. Pick one computer to use as a "controller", plug an ethernet cable into router LAN port
    "Pick on computer that you would like to use as your OpenFlow 'controller'. If possible, you'll want to use a Mac or Linux computer since you'll be using special utilities like SSH and SCP". Run an ethernet cable from a LAN port on your router to your laptop's ethernet port"
1. Navigate to the router's admin panel: 192.168.1.1
    "Once we're connected to our router's network, open a web browser and point it to: http://192.168.1.1"
1. Login in with username 'admin' and password 'admin'
    "When we're prompted to log in, use the username 'admin' and the password, 'admin'"
1. Head to System Tools -> Firmware upgrade
    "Once we're logged in, we'll want to head to system Tools in the sidebar, click on that, then head to Firmware upgrade"
1. "For the firmware file upload, select misc/firmware/ofwrt-attitude-adj-pantou.bin in this repository. Click Upload"
1. "Wait a few minutes for your router to install the new firmware. When the firmware is properly installed, you won't have access to a web interface any longer, but you will be able to get shell access"
1. Telnet into your router: `telnet 192.168.1.1`
    "Open your terminal application, like DOS or Terminal.app, and telnet into the TPLink router at 192.168.1.1"
1. Set a password for the root account (follow the prompts): `passwd`
    "Now let's set a password for the root account on our router. Type `passwd` and follow the prompts"
1. "Finally, let's exit out of telnet. Exit: `exit`"
1. Using Putty for Windows, or SSH for Mac or Linux, SSH into your router: `ssh root@192.168.1.1`
1. "Enter the password that you set earlier ... did you get in? Nice! Now you can move on to configure your switch."

1. Configure router
    "Now it's time to configure our router in a way that facilitates our OpenFlow experiments. We're going to designate the router's WAN port as a port where the controller will be connected, and the LAN ports as OpenFlow-controlled ports"
    - "In the files you downloaded earlier, copy misc/router-config/network to your router with this command: scp misc/router-config/network root@192.168.1.1:~/"
    - "Then log into the router, and run: sudo cp network /etc/config/""
1. "Now it's time to restart the network. Our connection is going to die, because now the only place we can connect to our switch on on the LAN port: /etc/init.d/network restart"
1. Unplug from LAN, plug comp into router's WAN port
    "Unplug your controller from the router's LAN port, and plug it into the WAN port. Wait a few seconds until your computer connects to the network"
1. Get your controller's IP address
    "Find out your controllers' IP address. You can do this by opening a terminal, and running `ifconfig`"
1. "Now let's jump back into our router and finish what we started. SSH back into the router like before:`ssh root@192.168.1.1`"
1. "Open a text editor and edit the openflow configuration:" `vi /etc/config/openflow'
1. "Use arrow keys to move to line that says 'ofctl': 
    If you're not familiar with the vi text editor, you'll want to type the letter 'i' once. then you'll be able to add and delete characters. Replace the existing ip address on that line with your router's. Finally, press colon, w, q, and enter." :wq [enter]
1. Restart openflow: /etc/init.d/openflow restart
    "Lastly, restart openflow on your switch. Congrats, now Openflow is enabled on your switch! All we have to do now is move on to our next project, where we'll get a controller up and running"

1. Example project (mozilla_flow)
"On the computer you're using as a controller, navigate to the controller folder"
1. Navigate to controller/ in the example code
1. Run: ./poy.py --verbose mozilla_load
    - Will redirect UDP packets from 10002 to 10003
1. Watch for openflow connection from switch
1. Plug in remaining computers to router LAN ports
1. Wait for IP addresses to be assigned
1. Obtain each computer's IP address: ipconfig (Windows) / ifconfig (Mac)
1. At a command, navigate to the exmaple code
1. Navigate to code/mozilla_flow/
1. On one computer, run: python receive.py 
    - It will listen on port 10003
1. On the other, navigate tot he example code.
   run: python send.py [IP address of receiving computer] Hello!
    - It will send on port 10002
1. Watch for message to appear on receiving computer

kenny@mozillafoundation.org
