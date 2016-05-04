import urllib
import json
import requests

api_key = '-zk9FCZu_J6kWND991eQ'

def main():
    regenerate_results('full', '896688')
    download_results('full', '896688')

def regenerate_results(report_type, job_id):
    # regenerates the results of type report_type for job job_id to ensure we're downloading latest

    request_url = 'https://api.crowdflower.com/v1/jobs/{}/regenerate?'.format(job_id)
    payload = { 'type': report_type, 'key': api_key }

    r = requests.post(request_url, params=payload)

    if (r.status_code == 200):
        print 'Job ' + job_id + ' results regenerate successful'

def download_results(report_type, job_id):
    # downloads results of type report_type for job job_id from CrowdFlower

    request_url = 'https://api.crowdflower.com/v1/jobs/{}.csv?'.format(job_id)
    payload = { 'type': report_type, 'key': api_key }

    r = requests.get(request_url, params=payload)

    print r.status_code
    if (r.status_code == 200):
        print 'Job ' + job_id + ' results download successful'

if __name__ == "__main__":
    main()
