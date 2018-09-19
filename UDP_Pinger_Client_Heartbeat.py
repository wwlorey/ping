#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from socket import *
import datetime

# Initialize constants
NUM_HEARTBEATS = 10
UDP_IP = ''
UDP_PORT = 12000

SKIP_HEARTBEATS = True
HEARTBEAT_SKIP_PROB = 0.3

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Simulate a "dying" client by sending a finite number of heartbeats
for beat_num in range(1, NUM_HEARTBEATS + 1):
    if SKIP_HEARTBEATS:
        # Simulate dropping packets by skipping heartbeats
        if random.random() <= HEARTBEAT_SKIP_PROB:
            # Skip sending this packet
            continue

    # Create a heartbeat message
    beatMessage = str(beat_num) + ' ' + str(datetime.datetime.now().time())
    print(beatMessage)

    # Send the message
    clientSocket.sendto(beatMessage.encode(), (UDP_IP, UDP_PORT))
