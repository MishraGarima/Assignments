Assignment: Do Network Analysis using Nmap (network mapper)

Install the network scanning tool Nmap 
$ sudo apt install nmap

Get the IP range/subnet mask of your network
$ ifconfig
or using UI

Scan Network for connected device using Nmap
$ nmap -sP 10.1.50.11/24
(IP of the current PC)

Scan port 80 on the target system
$ nmap -p 80 10.1.50.11

Scan all ports(1-65536) on the target system
$ nmap -p- 10.1.50.11

OS scanning using Nmap
$ nmap -O 10.1.50.11
