from sys import argv
from struct import *

import os
import sys
import getopt
import shutil
import filecmp
import binascii

original_file = ''
patched_file = ''
export_file = ''

def GetParams(argv):	
	global original_file
	global patched_file
	global export_file
	
	try:
		opts, args = getopt.getopt(argv,'ho:p:e:',['help', 'original=','patched=','export='])
	
		for opt, arg in opts:
			if opt == '-h':
				sys.exit()
			elif opt in ('-o', '--original'):
				original_file = arg
			elif opt in ('-p', '--patched'):
				patched_file = arg
			elif opt in ('-e', '--export'):
				export_file = arg
	except getopt.GetoptError:
		sys.exit(2)

def ValidInput():
	if os.path.isfile(original_file) and os.path.isfile(patched_file):
		if filecmp.cmp(original_file, patched_file) == False:
			return True
		else:
			print('\r\n[Warning] > The chosen eFile are identical!')
			return False
	else:
		if os.path.isfile(original_file) == False:
			print('\r\n[Warning] > {0} not found!'.format(os.path.basename(original_file)))
		if os.path.isfile(patched_file) == False:
			print('\r\n[Warning] > {0} not found!'.format(os.path.basename(patched_file)))
		return False
			
def CreatePatch():
	if (ValidInput()):
		position = 0x1
		offset = 0x1
		patchcode = ''

		#Generate PatchCode
		with open(original_file, 'rb') as oFile:
			with open(patched_file, 'rb') as pFile:
				byteO = oFile.read(1)
				byteP = pFile.read(1)
				while byteO: # != b'':
					byteO = oFile.read(1)
					byteP = pFile.read(1)
					if byteO != byteP:
						if int(offset) == int(position):
							patchcode += ';{0}:{1}'.format(hex(offset), str(byteP))
						else:
							patchcode += str(byteP)
					else:
						offset = position + 0x1
					position += 0x1
		
		#Merge PatchCode
		patchcode = patchcode.replace('\'b\'\\', '\\')
		
		#Export PatchCode
		with open(export_file, 'w') as eFile:
			eFile.write(patchcode)
	
		return True
	else:
		return False

def UnPackData(*args):
	return struct.pack('%df' % len(args), *args)
		
def PrintDone():
	os.system('cls')
	print('\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('Done...\r\n')
	print('{0} was successfull created! Enjoy it!\r\n'.format(os.path.basename(export_file)))
	print('-=] PatchMaker v1.0 # by scopolamin 2013 [=-')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n')
	
if __name__ == "__main__":
	try:
		GetParams(sys.argv[1:])
		if CreatePatch():
			PrintDone()
		else:
			print('\r\n[Warning] > PatchMaker was aborted')
	except IOError as io_err:
		print('\r\nI/O error: {0}\r\n'.format(io_err))
	except SystemExit as se_err:
		print('\r\nusage: C:\> python PatchMaker.py -o <original> -p <patched> -e <export>\r\n')
	except:
		print('\r\nUnknown Error: {0}\r\n'.format(sys.exc_info()[0]))

		

	

