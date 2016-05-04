import csv

url_comments = {}

with open('../data/f901004.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print row
		if row['_golden'].upper() == 'FALSE':
			if row['url_img1'] in url_comments:
				url_comments[row['url_img1']].append(row['enter_the_reasoning_for_your_decision'])
			else:
				url_comments[row['url_img1']] = []
				url_comments[row['url_img1']].append(row['_unit_id'])
				url_comments[row['url_img1']].append(row['enter_the_reasoning_for_your_decision'])
			# if row['url_img2'] in url_comments:
			# 	url_comments[row['url_img2']].append(row['comment_img2'])
			# else:
			# 	url_comments[row['url_img2']] = []
			# 	url_comments[row['url_img2']].append(row['_unit_id'])
			# 	url_comments[row['url_img2']].append(row['comment_img2'])

print url_comments


with open('../data/qc2_input.csv', 'wb') as writefile:
	qc2_input = csv.writer(writefile)
	qc2_input.writerow(['img_id','img_url','img_comment1','img_comment2','img_comment3','img_comment4','img_comment5'])
	for key, value in url_comments.iteritems():
		for i in range(0,len(value)/5):
			data = []
			data.append(value[0])
			data.append(key)
			data.append(value[i*5 + 1])
			data.append(value[i*5 + 2])
			data.append(value[i*5 + 3])
			data.append(value[i*5 + 4])
			data.append(value[i*5 + 5])
			qc2_input.writerow(data)


