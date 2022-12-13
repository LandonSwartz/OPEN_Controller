import os
import logging
import subprocess #for making sub process of command
from time import sleep

#getting log
#log = logging.getLogger('open_controller_log.log')


class gocommand_helper():
	def __init__(self,	username, target_dir, local_dir):
		#log.debug('Initializing irod	helper')
		print('Initializing irod helper')
		self.Cyverse_Username	= username
		self.Cyverse_Dir = target_dir
		self.Local_Exp_Dir = local_dir

	# Execute a command
	def execute_command(self, cmd):
		#os.system(cmd)
		p = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		# may have to put this in separate thread to not block executation of program
		#while p.poll() is None:
			#print('Waiting...')
			#sleep(1)
			#pass
		out, err = p.communicate() # This is a blocking function, stops program until finished
		print(out.decode('UTF-8'))
		print(err.decode('UTF-8'))
		
	# Make	directory in Cyverse Account
	def cyverse_mkdir(self, dir):
		cmd = './gocmd mkdir {}'.format(dir)
		self.execute_command(cmd)
		print('Folder Created')  
	
	#Find current working directory
	def cyverse_pwd(self):
		cmd = './gocmd pwd'
		self.execute_command(cmd)
		
	#Find current working directory
	def cyverse_ls_dir(self):
		cmd = './gocmd ls'
		self.execute_command(cmd)

	# to download cyverse directory
	def download_cyverse_dir(self,	target_dir,	local_dest):
		cmd = './gocmd get --progress {} {}'.format(target_dir, local_dest)
		self.execute_command(cmd)

   # to	upload cyverse directory
	def upload_cyverse_dir(self, target_dir, local_dest):
		cmd = './gocmd put	--progress {} {}'.format(local_dest, target_dir)
		self.execute_command(cmd)
		
	# syncs local directory with irod directory in	Cyverse, not given
	def sync_cyverse_dir(self):
		cmd = './gocmd sync --progress {} i:{}'.format(self.Local_Exp_Dir, self.CyVerse_Dir)
		self.execute_command(cmd)

	# syncs local directory with irod directory in	Cyverse given
	def sync_cyverse_dir(self,	local_dir, target_dir):
		cmd = './gocmd sync --progress {} i:{}'.format(local_dir, target_dir)
		self.execute_command(cmd)