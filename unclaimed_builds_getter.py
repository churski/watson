#!bin/python
from unclaimed_builds_finder import jenkins_unclaimed_builds_finder
from datetime import datetime
import config

if not (config.username and config.token and config.jenkins_url and config.jobs):
	print "Please, fill config.py file"
	exit(1)

class unclaimed_builds_getter:
	
	jobs = config.jobs
	
	def __init__(self):
		self.builds_finder = jenkins_unclaimed_builds_finder(config.username, config.token, config.jenkins_url)
		self.not_claimed = {}
	
	def update(self):		
		for job in config.jobs:
			try:
				builds = self.builds_finder.get_not_claimed_builds(job, 10)
				self.not_claimed[job] = []
				for build in builds:
					self.not_claimed[job].append(build)
			except Exception, e:
				print "Exception while getting builds of job %s" % job
				print e	

	def get(self):
		return self.not_claimed
