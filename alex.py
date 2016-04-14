import urllib2
import json
import MySQLdb

# Open database connection
db = MySQLdb.connect("us-cdbr-iron-east-03.cleardb.net","bf195be856ac10","fc75324d","heroku_8020c01508c5dac" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT * FROM CHALLENGES WHERE task_completed = 0")

# Fetch a single row using fetchone() method.
results = cursor.fetchall()
print results


api_key = 'K5t1gBHpy98KosE7zNsG'

def is_completed(job_id):
  url = "https://api.crowdflower.com/v1/jobs/" + job_id + "/ping.json?key=" + api_key
  results = urllib2.urlopen(url).read()
  json_data = json.loads(results)
  return json_data['ordered_units'] == json_data['completed_units_estimate']


job_id = '889596'
print is_completed(job_id)

# curl -X GET https://api.crowdflower.com/v1/jobs/{job_id}/ping.json?key={api_key}

# disconnect from server
db.close()