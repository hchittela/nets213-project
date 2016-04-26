import urllib2
import urllib
import json
import requests
import MySQLdb
import csv

api_key = '-zk9FCZu_J6kWND991eQ'

def main():
    j = json.loads(create_job('CCB Round 1'))
    data = get_challenges_db()
    csv_path = create_csv(data, str(j['id']))
    upload_csv(csv_path, str(j['id']))


def create_job(title):
    # creates a new job on CrowdFlower with the given title
    data = {'job[title]' : title }
    data = urllib.urlencode(data)

    url = 'https://api.crowdflower.com/v1/jobs.json?key=' + api_key
    req = urllib2.Request(url, data, { 'Content-Type':'application/x-www-form-urlencoded'})

    js = ''
    f = urllib2.urlopen(req)

    for x in f:
        job_info = x
    f.close()

    print "Job " + str(json.loads(job_info)['id']) + " created succesfully"

    return job_info


def get_challenges_db():
    username = 'bf195be856ac10'
    password = 'fc75324d'
    db = MySQLdb.connect("us-cdbr-iron-east-03.cleardb.net", username, password, "heroku_8020c01508c5dac" )
    cursor = db.cursor()

    cursor.execute("SELECT url_1, url_2 FROM challenges")
    data = cursor.fetchall()

    return data


def create_csv(data, job_id):
    csv_path = 'data/' + job_id + '_input.csv'
    c = csv.writer(open(csv_path, 'wb'))
    # write headers
    c.writerow(('id', '_golden', 'url_img1', 'url_img2', 'answer_golden'))


    c.writerow((1, 'TRUE', 'http://i.imgur.com/AD3DgWB.jpg', 'http://i.imgur.com/lYoObRX.jpg', 'img_1'))

    # counter var used for id numbers in csv
    counter = 2
    for (url1, url2) in data:
        c.writerow((counter, '', url1, url2, ''))
        counter += 1

    return csv_path


def upload_csv(csv_path, job_id):
    # uploads a csv file to an existing CrowdFlower job
    csv_file = open(csv_path, 'rb')

    request_url = "https://api.crowdflower.com/v1/jobs/{}/upload".format(job_id)
    headers = {'content-type': 'text/csv'}
    payload = { 'key': api_key }

    r = requests.put(request_url, data=csv_file, params=payload, headers=headers)

    if (r.status_code == 200):
        print "Job " + job_id + " CSV upload successful"


if __name__ == "__main__":
    main()
