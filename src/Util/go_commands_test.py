from gocommand import gocommand_helper
from time import sleep

gocmd_helper = gocommand_helper('lgaswartz', 'local_dir', 'target_dir')
gocmd_helper.cyverse_pwd()
gocmd_helper.cyverse_ls_dir()
sleep(1)

gocmd_helper.sync_cyverse_dir('~/Desktop/test_exp', '/iplant/home/lgaswartz/target_dir_mkdir')

sleep(1)
print('Finished')
