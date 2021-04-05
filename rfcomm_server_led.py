#!/usr/bin/python

import bluetooth
from bluetooth import *
import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
led = 18
GPIO.setup(led,GPIO.OUT)

host = ""
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
try:
	server.bind((host, bluetooth.PORT_ANY))
	print("Bluetooth Binding Completed")
except:
	print("Bluetooth Binding Failed")

server.listen(1) # One connection at a time
port = server.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)
# Server accepts the clients request and assigns a mac address. 
client, address = server.accept()
print("Connected To", address)
print("Client:", client)
try:
	while True:
		# Receivng the data. 
		data = client.recv(1024) # 1024 is the buffer size.
		# print(data)
		
		if data == "1":
			GPIO.output(led, GPIO.HIGH)
			send_data = "Light On "
		elif data == "0":
			GPIO.output(led, GPIO.LOW)
			send_data = "Light Off "
		else:
			send_data = "Type 1 or 0 "
		# Sending the data.
		client.send(send_data) 
except:
	# Closing the client and server connection
	client.close()
	server.close()
