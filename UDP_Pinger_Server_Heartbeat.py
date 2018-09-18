#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This server assumes that packet numbering starts at 1 and increases in increments of 1.

If the last N packets sent by a client are dropped, the server will not report lost packets
as the number of sent packets is not agreed upon beforehand.
"""

import random
from socket import *
import datetime

# Holds the sequence number and timestamp received in a UDP message
class UDPMessage:
    def __init__(self, message):
        """Initializes the UDPMessage class"""
        message = message.decode().split()
        self.seqNum = int(message[0])
        self.timestamp = datetime.datetime.strptime(message[1], '%H:%M:%S.%f')

# Initialize constants
HEARTBEAT_TIMEOUT = 3.0
TIME_DIFF = 1.0
UDP_IP = ''
UDP_PORT = 12000
BUFF_SIZE = 1024
MAX_NUM_UNRESPONSIVE_CLIENTS = 1

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Set a timeout for the socket in seconds
serverSocket.settimeout(HEARTBEAT_TIMEOUT)

# Assign IP address and port number to socket
serverSocket.bind((UDP_IP, UDP_PORT))

# Create a variable to store the previous message received
prevMessage = UDPMessage(('0 ' + str(datetime.datetime.now().time())).encode())

num_unresponsive_clients = 0

while True:
    # Attempt to receive the client packet along with the address it is coming from
    try:
        message, address = serverSocket.recvfrom(BUFF_SIZE)
        
        newMessage = UDPMessage(message)

        # The client is alive
        print('Received packet ' + str(newMessage.seqNum))

        # Calculate the time diff
        diff = (newMessage.timestamp - prevMessage.timestamp).total_seconds() 

        # Check for dropped packets
        if newMessage.seqNum - prevMessage.seqNum > 1:
            print('Dropped packet(s): ' + str(list(range(prevMessage.seqNum + 1, newMessage.seqNum)))[1:-1])
        
        # Print the time diff
        print('Time diff: ' + str(diff) + '\n')

        prevMessage = newMessage

        
    except:
        # The client is dead
        print('Unresponsive client\n')

        num_unresponsive_clients += 1

        if num_unresponsive_clients >= MAX_NUM_UNRESPONSIVE_CLIENTS:
            break
