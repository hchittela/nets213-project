import csv

bad_response_workers = []

# not sure why, but none of the results have golden = TRUE, so this is pointless, hence I commented it
# with open('../data/f901004.csv') as csvfile:
# 	reader = csv.DictReader(csvfile)
# 	for row in reader:
# 		if row['_golden'].upper() == 'TRUE' and row['select_the_most_visually_appealing_design'] != row['select_the_most_visually_appealing_design']:
# 			bad_response_workers.append(row['_worker_id'])


with open('../data/qc1_output.csv', 'wb') as writefile:
	qc1_output = csv.writer(writefile)
	qc1_output.writerow(['img_id','vote'])
	with open('../data/f901004.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['_golden'].upper() == 'FALSE' and row['_worker_id'] not in bad_response_workers:
				data = []
				data.append(row['_unit_id'])
				data.append(row['select_the_most_visually_appealing_design'])
				qc1_output.writerow(data)