#!/usr/bin/python

import bluetooth
import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)

pwm = GPIO.PWM(33, 50)
pwm.start(2.5)              # min 2.5, max 11.5 180 degrees

host = ""
# Creaitng Socket Bluetooth RFCOMM communication
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
		
		if data == "stop":
			pwm.start(0)
			send_data = "Stop "
		elif data == "middle":
			pwm.ChangeDutyCycle(7.0)
			send_data = "Middle "
		elif data == "right":
			pwm.ChangeDutyCycle(2.5)
			send_data = "Right "
		elif data == "left":
			pwm.ChangeDutyCycle(11.5)
			send_data = "Left "
		else:
			send_data = "Error "
		# Sending the data.
		client.send(send_data) 
except:
	# Closing the client and server connection
	client.close()
	server.close()
