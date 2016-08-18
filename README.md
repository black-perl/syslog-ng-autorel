# syslog-ng-autorel
https://github.com/balabit/syslog-ng/wiki/GSoC2016-Idea-&amp;-Project-list#project-automated-release-generation-for-syslog-ng

Testing Instructions
---------------------
- Configure `autorel/settings.py` 
	- PROJECT = "black-perl/syslog-ng" (fork against we are testing)
	- GITHUB_AUTH_TOKEN = <github-token-object>
- Configure `autorel/release/obs.py` for OBS settings
- `python3 release_test.py`

Dependencies
------------
- `docker-py`(Python 3.4)
- `pygit2` (Python 3.4)
- `pygithub` (Python 3.4)
- `python-osc` (Python 2.7)

Notes
=====
- Some things are required to be hardcoded because we are testing against a fork
- And, some refactoring is required.
- Commits to `test` branch are result of fast bug fixes. I will make separate commits
  to independent modules and finally merge them.

