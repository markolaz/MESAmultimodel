import numpy as np
import os
import subprocess
import fileinput
import datetime

start = datetime.datetime.now()

masses = np.linspace(1, 4, 16)

#for mass in masses:
#	os.system('rm -rf '+str(mass)+'Msun')				#clear all existing directories - careful!

for mass in masses:
	os.system('cp -r $MESA_DIR/star/work '+str(mass)+'Msun')
	os.chdir(str(mass)+'Msun')
	os.system('pwd') #testing
	os.system('./mk')
	try:
		while subprocess.check_output(["pidof",'make']).strip():
			pass
	except subprocess.CalledProcessError, e:
		os.system('cp ../default_inlist inlist_project')
		for line in fileinput.input('inlist_project', inplace=True):
			print line.replace('TEMP_MASS', str(mass)).rstrip()
		os.system('./rn')
		try:
			while subprocess.check_output(["pidof",'star']).strip():
				pass
		except subprocess.CalledProcessError, e:
			print '~~~~~ FINISHED WITH '+str(mass)+' MSUN MODEL ~~~~~'
			os.chdir('..')

print datetime.datetime.now() - start