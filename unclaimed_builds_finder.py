#!bin/python
from jenkinsapi.jenkins import Jenkins

class jenkins_unclaimed_builds_finder:
	
	def __init__(
		self,
		username,
		password,
		url
	):
		print "Connecting..."
		self.jenkins = Jenkins(
			url,
			username,
			password,
			timeout=15
		)
		print "Connected"

	def is_claimed(self, build):
		try:
			return build.get_actions()['claimed']
		except KeyError:
			return False
			
	def get_last_n_failed_builds(self, job_name, n):
		job = self.jenkins[job_name]
		last = job.get_last_buildnumber()
		failed_builds = []
		for i in range(last - n, last + 1):
			build = job.get_build(i)
			if (build.get_status() == 'FAILURE'):
				failed_builds.append(build)
		return failed_builds

	# n is a number of last jobs that we want to check
	def get_not_claimed_builds(self, job_name, n):
		builds = self.get_last_n_failed_builds(job_name, n)
		not_claimed = []
		for build in builds:
			if not self.is_claimed(build):
				not_claimed.append(build)
		return not_claimed
