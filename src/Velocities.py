import sys; sys.dont_write_bytecode = True
from sage.all import *
import os
import errno
import subprocess
import re
import platform
import Message
import ast
class Velocities:
	def __init__(self,sd):
		self.velocities = []
		self.name =""
		self.sd=sd
	

	#The user has decided to choose a velocity set associated with this space decomposition. This method will guide the user while they do so,
	#and return the chosen velocity set.			
	def chooseVelocities(self):
		os.chdir(os.path.expanduser('~/Documents/ElvisFiles/Situations/'+self.sd.name+'/Velocities/'))
		#Show the user the chosen velocity sets.
		print "\nYour saved velocity sets:"
		subprocess.call("ls")

		#Let the user choose a velocity file. Keep asking until it works. This code works whether
		#the user types the file extension or not.
		while(True):
			chosenVelFile = Message.getResponse("\nSelect a velocity file (case sensitive): ")
			try:
				with open(chosenVelFile,"r") as file:
					content = file.readlines()
			except:
				try:
					with open(chosenVelFile+'.txt',"r") as file:
						content = file.readlines()
				except:
					if OSError.errno == errno.ENOENT:
						print "---That velocity file does not exist, retry---"
					else:
						Message.errorMessage()
				break
			break
		content = [x.strip() for x in content]
		self.name = content[0]
		self.velocities = ast.literal_eval(content[1])


	#This method will create and return a new velocity set for this space decomposition.
	def createVelocities(self):
		#There will be exactly one velocity set associated to each region in the space decomposition.
		for i in range(self.sd.n):
			while True:
				#The user will be prompted to enter a valid velocity set.
				rawNumber = Message.getResponse('\nEnter a positive real number to indicate the velocity associated with region ' +str(i+1) +'. \n')
				try:
					#For now, velocity sets are just spheres, defined by a real number. This method will have to be rewritten to accept 
					#any function in hyperspherical coordinates.
					speed = (float)(rawNumber)
				except:
					Message.errorMessage()
					continue
				#Check that the number is positive before breaking the loop.	
				if speed > 0:
					break
				else:
					print('This number is not positive. ')
			self.velocities.append(speed)

		if self.sd.name != "":
			self.saveVelocitySet()


	#Save a velocity set as a text file in the folder associated to the relevant space decomposition.
	def saveVelocitySet(self):
		save = Message.getResponse("Save this velocity set(y/n): ")
		while save != "y" and save != "n":
			save = Message.getResponse("Error, type either y or n, retry: ")
		if save == "y":
			currDir = os.getcwd()
			os.chdir(os.path.expanduser('~/Documents/ElvisFiles/Situations/' + self.sd.name +'/Velocities/'))
			saveDir = os.getcwd()
			while True:
				self.name = Message.getResponse("Name your velocity set. Do not use 'q': ")
				try:
					velFile = open(self.name+'.txt',"w+")
				except:
					if OSError.errno != errno.EEXIST:
						Message.errorMessage()
					else:	
						print "ERROR... Already a saved velocity set. \n"
					continue
				break
			velFile.write(self.name + "\n")
			velFile.write(str(self.velocities))
			velFile.close()
			os.chdir(os.path.expanduser(currDir))
			print  self.name + " saved to " + saveDir
