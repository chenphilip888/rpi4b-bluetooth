#!/usr/bin/python3

import bluetooth
import time

bd_addr = "DC:A6:32:D4:DE:E0"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

for i in range( 5 ):
    sock.send("1")
    print(sock.recv(1024))
    time.sleep( 1 )
    sock.send("0")
    print(sock.recv(1024))
    time.sleep( 1 )

sock.close()
