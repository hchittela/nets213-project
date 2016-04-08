import csv

votes = {}
comments = {}

with open('../data/qc1_output.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['img_id'] in votes:
			votes[row['img_id']][row['vote']] = votes[row['img_id']][row['vote']] + 1
		else:
			votes[row['img_id']] = {'A': 0, 'B': 0}

with open('../data/aggregation_output.csv', 'wb') as writefile:
	agg_output = csv.writer(writefile)
	agg_output.writerow(['id', 'vote_img1', 'vote_img2'])
	for vote in votes:
		agg_output.writerow([vote, votes[vote]['A'], votes[vote]['B']])