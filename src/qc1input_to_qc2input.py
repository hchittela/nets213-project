import csv

url_comments = {}

with open('../data/qc1_input.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['_golden'] == 'FALSE':
			if row['url_img1'] in url_comments:
				url_comments[row['url_img1']].append(row['comment_img1'])
			else:
				url_comments[row['url_img1']] = []
				url_comments[row['url_img1']].append(row['img_id'])
				url_comments[row['url_img1']].append(row['comment_img1'])
			if row['url_img2'] in url_comments:
				url_comments[row['url_img2']].append(row['comment_img2'])
			else:
				url_comments[row['url_img2']] = []
				url_comments[row['url_img2']].append(row['img_id'])
				url_comments[row['url_img2']].append(row['comment_img2'])

print url_comments


with open('../data/qc2_input.csv', 'wb') as writefile:
	qc2_input = csv.writer(writefile)
	qc2_input.writerow(['id','img_id','img_url','img_comment1','img_comment2','img_comment3','img_comment4','img_comment5'])
	for key, value in url_comments.iteritems():
		data = []
		data.append('1')
		data.append(value[0])
		data.append(key)
		data.append(value[1])
		data.append(value[2])
		data.append(value[3])
		data.append(value[4])
		data.append(value[5])
		qc2_input.writerow(data)


