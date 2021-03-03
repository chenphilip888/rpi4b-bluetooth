#!/usr/bin/python3

import bluetooth
import time

bd_addr = "DC:A6:32:D4:DE:E0"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

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
