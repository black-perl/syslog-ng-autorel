import sys,os
import logging
autorel_path = os.path.abspath('autorel/')
sys.path.append(autorel_path)
deps_path = os.path.abspath('autorel/deps')
sys.path.append(deps_path)

from autorel.settings import (VERSION,
							  RELEASE_TAG,
							  RELEASE_NAME
							  )
from release import SyslogNgRelease

s = SyslogNgRelease("master",RELEASE_NAME,RELEASE_TAG,VERSION)
s.release()