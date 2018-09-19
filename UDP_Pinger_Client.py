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

# Initialize variables
rtt_list = [None] * NUM_PINGS

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set a timeout for the socket in seconds
clientSocket.settimeout(TIMEOUT)

for ping_num in range(1, NUM_PINGS + 1):
    oldNow = datetime.datetime.now()

    # Create a ping message
    pingMessage = 'Ping ' + str(ping_num) + ' ' + str(oldNow.time())

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

        # Save off the RTT
        rtt_list[ping_num - 1] = rtt
        
    except:
        print('Request timed out')

    print()

# Calculate and print RTT stats
num_dropped_packets = rtt_list.count(None)
rtt_list = [f for f in rtt_list if f]

min_rtt = min(rtt_list)
max_rtt = max(rtt_list)
avg_rtt = sum(rtt_list) / len(rtt_list)
packet_loss = (num_dropped_packets / NUM_PINGS) * 100

print('RTT Statistics')
print('min RTT:\t' + str(min_rtt))
print('max RTT:\t' + str(max_rtt))
print('average RTT:\t' + str(avg_rtt))
print('packet loss:\t' + str(packet_loss) + '%')
