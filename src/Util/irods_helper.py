import os
import logging
import subprocess #for making sub process of command

#getting log
log = logging.getLogger('open_controller_log.log')


class irod_helper():
    def __init__(self, username, target_dir):
        log.debug('Initializing irod helper')
        self.Cyverse_Username = username
        self.Cyverse_Dir = target_dir

    # to initialize irods for first time (if needed)
    #def iinit(self, username, password):
        #subprocess.call(['iinit'], shell=True)

    # to make directory on cyverse account
    def make_cyverse_dir(self, dir):
        subprocess.call(['imkdir /iplant/home/{}/{}'.format(self.Cyverse_Username, dir)], shell=True)

    # to downlaod cyverse directory
    def downlaod_cyverse_dir(self, target_dir, local_dest):
        subprocess.call(['iget -PT /iplant/home/{}/{} /{}'.format(self.Cyverse_Username, target_dir, local_dest)])

   # to upload cyverse directory
    def upload_cyverse_dir(self, target_dir, local_dest):
        subprocess.call(['iput -rPT /iplant/home/{}/{} /{}'.format(self.Cyverse_Username, target_dir, local_dest)])

    # syncs local directory with irod directory in Cyverse
    def sync_cyverse_dir(self, local_dir):
        subprocess.call(['irsync -r {} /iplant/home/{}/{}'.format(local_dir, self.Cyverse_Username, self.Cyverse_Dir)])
