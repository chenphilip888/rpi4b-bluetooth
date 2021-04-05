#!/usr/bin/python3

import bluetooth
import sys
import time

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = bluetooth.find_service( uuid = uuid )

if len(service_matches) == 0:
    print("couldn't find the FooBar service")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((host, port))

for i in range( 5 ):
    sock.send("middle")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("right")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("left")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("middle")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("left")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("right")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("middle")
    print(sock.recv(1024))
    time.sleep( 0.8 )
    sock.send("left")
    print(sock.recv(1024))
    time.sleep( 0.8 )

sock.send("stop")
print(sock.recv(1024))
sock.close()
