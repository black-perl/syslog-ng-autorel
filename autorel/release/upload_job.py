import datetime
import sys
import os

#configure deps
deps_path = os.path.abspath("/home/ank/test/syslog-ng-autorel/autorel/deps/")
sys.path.append(deps_path)

from obs import OBS

obs_client = OBS()
current_files = obs_client.list_files()
# delete the current set of files
obs_client.remove_files(current_files)
# add the new set of files
new_files = sys.argv[1:]
obs_client.add_files(new_files)
# commit the new files
obs_client.commit()