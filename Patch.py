from sys import argv
from struct import *

import os
import sys
import getopt
import shutil
import filecmp
import binascii
import shutil

original_file = ''
patch_file = ''

def GetParams(argv):	
	global original_file
	global patch_file
	
	try:
		opts, args = getopt.getopt(argv,'ho:p:',['help', 'original=','patch='])
	
		for opt, arg in opts:
			if opt == '-h':
				sys.exit()
			elif opt in ('-o', '--original'):
				original_file = arg
			elif opt in ('-p', '--patch'):
				patch_file = arg
	except getopt.GetoptError:
		sys.exit(2)

def ValidInput():
	if os.path.isfile(original_file) and os.path.isfile(patch_file):
		return True
	else:
		if os.path.isfile(original_file) == False:
			print('\r\n[Warning] > {0} not found!'.format(os.path.basename(original_file)))
		if os.path.isfile(patch_file) == False:
			print('\r\n[Warning] > {0} not found!'.format(os.path.basename(patch_file)))
		return False
			
def PatchFile():
	if (ValidInput()):
		#Backup
		shutil.copy2(original_file, '{0}.bkp'.format(original_file))
			
		#Patch File
		with open(patch_file, 'r') as pFile:
			patch = pFile.read()
			arr = str(patch).split(";")

			if(len(arr) > 1):
				for code in arr[1:]:
					PatchBlock(code)
				return True
			else:
				print('\r\n[Warning] > {0} is invalid'.format(os.path.basename(patch_file)))
				return False
	else:
		return False
		
def PatchBlock(code):
	offset = int(code.split(':')[0], 16)
	bcd = code.split(':')[1];

	#Fix
	bcd = bcd.replace('\'b\'', '\\')
	bcd = bcd if bcd[2] == '\\' else bcd.replace('b\'', 'b\'\\')

	cnt = bcd.count('\\')
	frm = '{0}s'.format(cnt)
	#print('{0} [{1}]'.format(offset, bcd))
	
	try:
		cc = unpack('11s', str(bcd))[0]
		print('SUPER: {0} [{1}]'.format(offset, bcd))
	except:
		print('ERROR: {0} [{1}]'.format(offset, bcd))

	# with open(original_file, 'r+b') as fh:
		# fh.seek(offset)
		# fh.write(unpack('{0}s'.format(cnt), bcd))
		
def PrintDone():
	#os.system('cls')
	print('\r\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('Done...\r\n')
	print('{0} was successfull patched! Enjoy it!\r\n'.format(os.path.basename(original_file)))
	print('-=] PatchMaker v1.0 # by scopolamin 2013 [=-')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n')
	
if __name__ == "__main__":
	try:
		GetParams(sys.argv[1:])
		if PatchFile():
			PrintDone()
		else:
			print('\r\n[Warning] > Injection was aborted')
	except IOError as io_err:
		print('\r\nI/O error: {0}\r\n'.format(io_err))
	except SystemExit as se_err:
		print('\r\nusage: C:\> python Patch.py -o <original> -p <patch>\r\n')
	except:
		print('\r\nUnknown Error: {0}\r\n'.format(sys.exc_info()[0]))