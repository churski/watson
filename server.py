#!bin/python

from jenkinsapi.jenkins import Jenkins
from unclaimed_builds_getter import unclaimed_builds_getter
from flask import Flask
from datetime import datetime
import time
import thread

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0')

def update():
	global builds_getter
	global update_time
	while True:
		print "UPDATING... %s" % datetime.now() 
		builds_getter.update()
		print "UPDATED %s" % datetime.now() 
		update_time = datetime.now().strftime('%H:%M')
		time.sleep(30 * 60)

@app.route("/")
def hello():
	header = "<h1>Not claimed Jenkins builds</h1>"
	global update_time
	if update_time:
		header += "Last update time: %s<br>" % update_time
	else:
		header += "Initial update did not finish yet.<br>"
	unclaimed = ""
	for job in builds_getter.get():
		if builds_getter.get()[job]:
			unclaimed += "<h2>%s</h2>" % job
			for build in builds_getter.get()[job]:
				unclaimed += "<input type=\"checkbox\"><a href=%s/%s>%s</a><br>" % (build.job.url, build.get_number(), build)
				unclaimed += button(i, "%s/%s" % (build.job.url, build.get_number()), build)
	if unclaimed or not update_time:
		res = header + unclaimed
	else:
		res = header + no_unclaimed()
	return html_builder(res)

update_time = ""

builds_getter = unclaimed_builds_getter()
thread.start_new_thread(update, ())

def html_builder(body_content):
	return'''
<!DOCTYPE html>
<html>
<head>
<title>Web Jenkins Claims</title>
</head>
<body>
%s
</body>
</html>
''' % body_content

def no_unclaimed():
	return '''
<br>It's a bug or
<h2 style="color:green;">there are no unclaimed builds!</h2>
'''

def page_script():
	return """
  <script>
	  marked = {}
	  
	  function switchMarked(id) {
		  marked[id] = !marked[id];
		  if (marked[id]) {
			document.getElementById(id).style = "color: lightgray";
		} else {
			document.getElementById(id).style = "color: blue";
		}
	  }
  </script>
"""


def button(id, build_url, build_name):
	return """
<button onclick="switchMarked(%s)" style="border-radius: 3px;">Marker</button><a id=%s href='%s'>%s</a><br>
""" % (id, id, build_url, build_name)
