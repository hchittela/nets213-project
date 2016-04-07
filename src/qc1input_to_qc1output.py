import csv

bad_response_workers = []

with open('../data/qc1_input.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['_golden'] == 'TRUE' and row['which_design_is_better'] != row['which_design_is_better_gold']:
			bad_response_workers.append(row['_worker_id'])


with open('../data/qc1_output.csv', 'wb') as writefile:
	qc1_output = csv.writer(writefile)
	qc1_output.writerow(['img_id','vote'])
	with open('../data/qc1_input.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['_golden'] == 'FALSE' and row['_worker_id'] not in bad_response_workers:
				data = []
				data.append(row['img_id'])
				data.append(row['which_design_is_better'])
				qc1_output.writerow(data)