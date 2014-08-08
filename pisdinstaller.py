#!/usr/bin/env python
#
# PI SD Installer
# Author: Danny Lin
#
# Quit on error(except) or choose 'No'
# Github:https://github.com/danny-source
# Website:http://cms.35g.tw/coding
import os, sys, re, subprocess

def printLogo():
	printClearScreen()
	print ""
	print "(  ____ )\__   __/"
	print "| (    )|   ) (   "
	print "| (____)|   | |   "
	print "|  _____)   | |   "
	print "| (         | |   "
	print "| )      ___) (___"
	print "|/       \_______/"
	print ""
	print '/ __)(  _ \   (_  _)( \( )/ __)(_  _) /__\  (  )  (  )  ( ___)(  _ \\'
	print '\__ \ )(_) )   _)(_  )  ( \__ \  )(  /(__)\  )(__  )(__  )__)  )   /'
	print '(___/(____/   (____)(_)\_)(___/ (__)(__)(__)(____)(____)(____)(_)\_)'
	print ''
             
def printLine():
	print '\033[00;32m+---------------------------------------------------------------------------+\033[00;00m'

def printClearScreen():
	print "\033[2J"

def getDiskList():
	# Pull up the list of connected disks
	disks = []
	dev = ''
	unit = ''
	size = ''
	num = 0
	diskutil_raw = subprocess.Popen(['diskutil', 'list'], stdout=subprocess.PIPE).stdout.readlines()
	mounts = subprocess.Popen(['mount'], stdout=subprocess.PIPE).stdout.readlines()
	for diskutil_line in diskutil_raw:
		line = diskutil_line.split()
		idx =0
		if line[0] != ('0:'):
			continue		
		for line1 in line:
			match = re.search('disk', line1)
			if match:
				break
			else:
				idx = idx +1
		try:					
			dev = line[idx]
			unit = line[idx-1]			
			size = line[idx-2].lstrip('*')			
		except IndexError:
			print 'list disk error'
			break;				

		if unit == 'GB' and float(size) <= 2.0:
			continue
		elif unit == 'MB' and float(size) <= 2048.0:
			continue				
		for mount in mounts:
			if '/dev/'+dev in mount.split()[0] and mount.split()[2] == '/':
				#skip system disk
				break
		else:
			num = num + 1
			disks.append([num, dev, size, unit])
	return disks,num


def writeToImg(dev,size,unit, path):
	disk_dev = dev

	print 'It will:'
	printLine()
	print '\033[00;32m|\033[00;00m\033[00;00m','\033[00;00mImage File:\033[00;31m',path 
	print '\033[00;32m|\033[00;00m\033[00;00m','\033[00;00mWrite to  :\033[00;31m',str(disk_dev) ,str(size) + str(unit)
	printLine()
	
	choose = raw_input('Are you sure? [Y]es or [N]:')
	
	if choose in 'Yy':
		print ''
	else:
		print 'exit!'
		return False
		
	disk_dev = '/dev/r' + disk_dev
	ddcommand = ['sudo', 'dd', 'bs=1024', 'of=' + str(disk_dev),'if=' + str(path)]
	print 'Generate DD command:'
	printLine()
	print '[',ddcommand[1],ddcommand[2],ddcommand[3],ddcommand[4],']'
	printLine()
	#
	unmountcommand = ['diskutil', 'unmountDisk', str(disk_dev)]
	#	
	try:
		unmount_raw = subprocess.call(unmountcommand)
	except subprocess.CalledProcessError:
		print 'The drive could not be unmounted. '
		'Make sure it is not in use before continuing.'
		return
	printLine()
	print 'Wait for disk to finish writing. \r\nYou can check the write progress with Ctrl+T or Ctrl-C to Break'
	printLine()
	dd_raw = subprocess.call(ddcommand)
	
	if '0' in str(dd_raw) is False:
		print 'dd command is except '
		sys.exit()
	printLine()
	print "Unmount Disk"
	printLine()
	unmount_raw = subprocess.call(unmountcommand)
	printLine()
	print "All Done!"
	return True

	

if __name__ == "__main__":
#check file and parmeter
	printLogo()
	imagefile =''
	try:
		imagefile = sys.argv[1]
		if (os.path.isfile(imagefile)) == False:
			printLine()
			print ' Image file paht is not exit'
			printLine()
			sys.exit()
	except IndexError:
		printLine()
		print ' Usage:pisdinstaller.py [image file]'
		printLine()
		sys.exit()
#get Devies ,and it is size upto 2GB
	devices,num = getDiskList()
	if devices == False:
		sys.exit()
#List Devies
	print '\033[00;32m+------------------------+\033[00;00m'
	print '\033[00;32m|\033[00;00m\033[00;00mNo    disk       size   \033[00;32m|\033[00;00m'
	print '\033[00;32m+------------------------+\033[00;00m'
	disknumber = ''
	for device in devices:
		#print str(device[0]) + '    ' + str(device[1]) +'    ' + str(device[2]) + '' + str(device[3])
		print('\033[00;32m|\033[00;00m %s   %s %10.2f %s\033[00;32m|\033[00;00m' % (device[0], device[1], float(device[2]), device[3]))
		disknumber = disknumber + str(device[0])
		if int(device[0]) != num:
			disknumber = disknumber + ','
			print '\033[00;32m+------------------------+\033[00;00m'
	print '\033[00;32m--------------------------\033[00;00m'	

	
	
	iChoose = 0
	loop = True
	deviceDisk = ''
	deviceUnit = ''
	deviceSize = ''
	while loop:
		print 'Select the disk to use by enetering the number.'
		print '\033[00;31m!!! MAKE SURE YOU SELECT THE CORRECT NUMBER FOR DISK !!!\033[00;00m'
		print '\r\n'
		
		choose = raw_input('\033[00;00menter number:[ \033[00;31m' + str(disknumber) +'\033[00;00m ] or [Q]uit:')
		if choose in 'Qq':
			print 'exit!\n\r'
			sys.exit()
		try:
			iChoose = int(choose)
			#
			for device in devices:
				if iChoose == int(device[0]):
					deviceDisk = device[1]
					deviceSize = device[2]
					deviceUnit = device[3]
					break;
			else:
				print 'it can\'t get Disk Number!\n\r'
				sys.exit()				
			#
			break;
		except:
			print 'You must key a Number\r\n'
	
	writeToImg(deviceDisk,deviceSize,deviceUnit,imagefile)