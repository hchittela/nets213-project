import urllib2
import urllib
import json
import requests

api_key = '-zk9FCZu_J6kWND991eQ'

def create_job(title):
	data = {'job[title]' : title }
	data = urllib.urlencode(data)

	url = 'https://api.crowdflower.com/v1/jobs.json?key=' + api_key
	req = urllib2.Request(url, data, { 'Content-Type':'application/x-www-form-urlencoded'})

	js = ''
	f = urllib2.urlopen(req)

	for x in f:
		js = x
	f.close()

	print "Job " + str(json.loads(js)['id']) + " created succesfully"

	return js


def upload_csv(csv_path, job_id):
	csv_file = open(csv_path, 'rb')

	request_url = "https://api.crowdflower.com/v1/jobs/{}/upload".format(job_id)
	headers = {'content-type': 'text/csv'}
	payload = { 'key': api_key }

	r = requests.put(request_url, data=csv_file, params=payload, headers=headers)

	if (r.status_code == 200):
		print "Job " + job_id + " CSV upload successful"

	# print r.content

if __name__ == "__main__":
	j = json.loads(create_job('job_4'))
	upload_csv('../data/qc2_input.csv', str(j['id']))
