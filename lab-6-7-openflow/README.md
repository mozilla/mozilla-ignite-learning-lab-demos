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

1. Get project files
1. Copy project files to all computers
1. Disconnect all from itnernet
1. Plug in router
1. Pick one computer to use as a "controller", plug in ethernet cable into router LAN port
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

1. Configure router
    - It's best to use a mac or linux to configure your router
    - Copy misc/router-config/network to your router: scp misc/router-config/network root@192.168.1.1:~/
    - From within the router, run: sudo cp network /etc/config/
1. Restart network (cxn will die): /etc/init.d/network restart
1. Unplug from LAN, plug comp into router's WAN port
1. Get your controller's IP address
1. SSH back into router if the connection didn't come up:`ssh root@192.168.1.1`
1. Enter: `vi /etc/config/openflow'
1. Use arrow keys to move to line that says 'ofctl': Enter your controller's IP address
1. Restart openflow: /etc/init.d/openflow restart

1. Example project
1. Plug in your "host" computers to the router's LAN ports



kenny@mozillafoundation.org
