#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from socket import *
import datetime

# Initialize constants
TIMEOUT = 1.0
UDP_IP = ''
UDP_PORT = 12000
NUM_PINGS = 10
BUFF_SIZE = 1024

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set a 1sec timeout for the socket
clientSocket.settimeout(TIMEOUT)

for i in range(1, NUM_PINGS + 1):
    oldNow = datetime.datetime.now()

    # Create a ping message
    pingMessage = 'Ping ' + str(i) + ' ' + str(oldNow.time())

    # Send a message
    clientSocket.sendto(pingMessage.encode(), (UDP_IP, UDP_PORT))

    # Attempt to receive a message
    try:
        message, address = clientSocket.recvfrom(BUFF_SIZE)

        # Calculate the round trip time (RTT) in seconds
        newNow = datetime.datetime.now()
        rtt = (newNow - oldNow).total_seconds()

        # Print the response message and RTT
        print(message.decode())
        print(rtt)
    except:
        print('Response timed out')

    print()