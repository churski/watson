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
	i = 0
	for job in builds_getter.get():
		if builds_getter.get()[job]:
			unclaimed += "<h2>%s</h2>" % job
			for build in builds_getter.get()[job]:
				unclaimed += button(i, "%s/%s" % (build.job.url, build.get_number()), build)
				i += 1
	if unclaimed or not update_time:
		res = header + unclaimed
	else:
		res = header + no_unclaimed
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
%s
%s
<body>
%s
</body>
</html>
''' % (page_script, page_styles, body_content)

def button(id, build_url, build_name):
	return """
<button onclick="switchMarked(%s)"></button><a id=%s href='%s'>%s</a><br>
""" % (id, id, build_url, build_name)


no_unclaimed = '''
<h2 style="color:green;">It seems that there are no unclaimed builds.</h2>
'''

page_script = """
  <script>
	  marked = {}
	  
	  function switchMarked(id) {
		  marked[id] = !marked[id];
		  if (marked[id]) {
			document.getElementById(id).style = "color: lightgray";
		} else {
			document.getElementById(id).style = "";
		}
	  }
  </script>
"""

page_styles = """
<style>
button {
	border-radius: 5px;
	height: 15px;
	width: 15px;
	margin: 3px;
}
</style>
"""
