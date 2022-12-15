import os
import logging
import subprocess #for making sub process of command
from time import sleep

#getting log
log = logging.getLogger('open_controller_log.log')


class gocommand_helper():
	
	# Initializing without specifying target or local dirs
	#@classmethod
	def __init__(self,	username):
		log.debug('Initializing gocommand helper')
		self.Cyverse_Username	= username #removed username with config file, may readd
		#self.Cyverse_Dir = target_dir
		#self.Local_Exp_Dir = local_dir
		self.config_gocommands() #configure gocommands using config file
	
	# Initializing with specifying target or local dirs
	'''@classmethod
	def init_with_params(cls, username, target_dir, local_dir):
		#log.debug('Initializing irod	helper')
		log.debug('Initializing gocommand helper')
		self.Cyverse_Username	= username #removed username with config file, may readd
		self.Cyverse_Dir = target_dir
		self.Local_Exp_Dir = local_dir'''
	
	# Configure using config.yaml
	def config_gocommands(self):
			cmd = './gocmd -c src/Util/config.yaml env'
			self.execute_command(cmd)
			log.debug('Configured GoCommands')

	# Execute a command
	def execute_command(self, cmd):
		#os.system(cmd)
		log.debug('Executing the cmd {} in gocmd helper'.format(cmd))
		p = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		# may have to put this in separate thread to not block executation of program
		#while p.poll() is None:
			#print('Waiting...')
			#sleep(1)
			#pass
		out, err = p.communicate() # This is a blocking function, stops program until finished
		log.info(out.decode('UTF-8'))
		log.info(err.decode('UTF-8'))
		
	# Make	directory in Cyverse Account
	def cyverse_mkdir(self, dir):
		cmd = './gocmd mkdir {}'.format(dir)
		self.execute_command(cmd)
		log.debug('Folder Created')  
	
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
		cmd = './gocmd get {} {}'.format(target_dir, local_dest)
		self.execute_command(cmd)

   # to	upload cyverse directory
	def upload_cyverse_dir(self, local_dir, target_dest):
		cmd = './gocmd put {} {}'.format(local_dir, target_dest)
		self.execute_command(cmd)
		
	# syncs local directory with irod directory in	Cyverse, not given
	#def sync_cyverse_dir(self):
		#cmd = './gocmd sync --progress {} i:{}'.format(self.Local_Exp_Dir, self.CyVerse_Dir)
		#self.execute_command(cmd)

	# syncs local directory with irod directory in	Cyverse given parameters
	def sync_cyverse_dir(self,	local_dir, target_dir):
		cmd = './gocmd sync {} i:/iplant/home/{}/{}'.format(local_dir, self.Cyverse_Username, target_dir)
		self.execute_command(cmd)
