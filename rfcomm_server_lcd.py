#!/usr/bin/python

import bluetooth
import time
import smbus

bus = smbus.SMBus(1)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# I2C LCD
# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)    
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)     
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count >= 16:
            count = 0
            row += 1
            if row >= 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

textCommand(0x01) # clear display
time.sleep(.05)
textCommand(0x08 | 0x04) # display on, no cursor
textCommand(0x28) # 2 lines
time.sleep(.05)

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
		
		if data == "red":
			setRGB( 255, 0, 0 )
			send_data = "Red "
		elif data == "green":
			setRGB( 0, 255, 0 )
			send_data = "Green "
		elif data == "blue":
			setRGB( 0, 0, 255 )
			send_data = "Blue "
		elif data == "yellow":
			setRGB( 255, 255, 0 )
			send_data = "Yellow "
		elif data == "cyan":
			setRGB( 0, 255, 255 )
			send_data = "Cyan "
		elif data == "purple":
			setRGB( 255, 0, 255 )
			send_data = "Purple "
		elif data == "black":
			setRGB( 0, 0, 0 )
			send_data = "Black "
		elif data == "white":
			setRGB( 255, 255, 255 )
			send_data = "White "
		else:
                        setRGB( 128, 255, 0 )
                        setText( data )
			send_data = "OK "
		# Sending the data.
		client.send(send_data) 
except:
	# Closing the client and server connection
	client.close()
	server.close()
