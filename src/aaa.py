#!/usr/bin/python
# -*- coding: utf-8 -*-

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSSwitch, Controller, RemoteController
import time
import os
import json
import time
import timeit

def emptyNet():

	net = Mininet(controller=Controller)

	info('*** Adding hosts ***\n')
	net.addHost('h1')
	net.addHost('h2')

	s1 = net.addSwitch('s1')

	net.addHost('r1')

	s2 = net.addSwitch('s2')

	net.addHost('h3')
	net.addHost('h4')

	ctrl = net.addController( 'c0', port=6633)


	info('*** Creating links ***\n')
	net.addLink('h1','s1')
	net.addLink('h2','s1')

	net.addLink('s1', 'r1')        
	net.addLink('r1', 's2')

	net.addLink('h3','s2')
	net.addLink('h4','s2')


	info('*** Configuring hosts ***\n')
	host = net.getNodeByName('h1')
	host.cmd('ifconfig h1-eth0 192.168.0.2')
	host.cmd('ifconfig netmask 255.255.255.0')
	host.cmd('route add default gw 192.168.0.1')

	host = net.getNodeByName('h2')
	host.cmd('ifconfig h2-eth0 192.168.0.3')
	host.cmd('ifconfig netmask 255.255.255.0')
	host.cmd('route add default gw 192.168.0.1')

	router = net.getNodeByName('r1')
	router.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
	router.cmd('ifconfig r1-eth0 192.168.0.1')
	router.cmd('ifconfig r1-eth0 netmask 255.255.255.0')
	router.cmd('route add default gw 0.0.0.0')
	router.cmd('ifconfig r1-eth1 10.0.0.1')
	router.cmd('ifconfig r1-eth1 netmask 255.255.255.0')
	router.cmd('')


	host = net.getNodeByName('h3')
	host.cmd('ifconfig h3-eth0 10.0.0.2')
	host.cmd('ifconfig netmask 255.255.255.0')
	host.cmd('route add default gw 10.0.0.1')

	host = net.getNodeByName('h4')
	host.cmd('ifconfig h4-eth0 10.0.0.3')
	host.cmd('ifconfig netmask 255.255.255.0')
	host.cmd('route add default gw 10.0.0.1')

	ctrl.start()
	s1.start([ctrl])
	s2.start([ctrl])

	info('*** Starting CLI ***\n')
	CLI(net)

	info('*** Stopping newtwork ***\n')
	net.stop()
	exit()


setLogLevel('info')
emptyNet()
