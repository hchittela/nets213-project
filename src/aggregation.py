import csv

votes = {}
comments = {}

with open('../data/qc1_output.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['img_id'] in votes:
			votes[row['img_id']][row['vote']] = votes[row['img_id']][row['vote']] + 1
		else:
			votes[row['img_id']] = {'img_1': 0, 'img_2': 0}
			votes[row['img_id']][row['vote']] = votes[row['img_id']][row['vote']] + 1

with open('../data/f901096.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['img_id'] not in comments:
			comments[row['img_id']] = {}
		comments[row['img_id']][row['img_comment1']] = []
		comments[row['img_id']][row['img_comment2']] = []
		comments[row['img_id']][row['img_comment3']] = []
		comments[row['img_id']][row['img_comment4']] = []
		comments[row['img_id']][row['img_comment5']] = []
		comments[row['img_id']][row['img_comment1']].append(int(row['how_useful_is_comment_1_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment1']].append(int(row['how_useful_is_comment_2_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment1']].append(int(row['how_useful_is_comment_3_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment1']].append(int(row['how_useful_is_comment_4_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment1']].append(int(row['how_useful_is_comment_5_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))

with open('../data/f901096.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		comments[row['img_id']][row['img_comment1']].append(int(row['how_useful_is_comment_1_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment2']].append(int(row['how_useful_is_comment_2_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment3']].append(int(row['how_useful_is_comment_3_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment4']].append(int(row['how_useful_is_comment_4_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))
		comments[row['img_id']][row['img_comment5']].append(int(row['how_useful_is_comment_5_for_this_picture_eg_1_is_blankgibberish_and_5_is_the_font_is_better']))

averages={}
top = {}
for img_id in comments:
	averages[img_id] = []
	for comment in comments[img_id]:
		avg = float(sum(comments[img_id][comment]))/len(comments[img_id][comment])
		averages[img_id].append((comment,avg))
	sort = sorted(averages[img_id], key=lambda tup: tup[1], reverse=True)
	top_5 = []
	top_5.append(sort[0])
	top_5.append(sort[1])
	top_5.append(sort[2])
	top_5.append(sort[3])
	top_5.append(sort[4])
	top[img_id] = top_5
print top


with open('../data/aggregation_output.csv', 'wb') as writefile:
	agg_output = csv.writer(writefile)
	agg_output.writerow(['id', 'vote_img1', 'vote_img2', 'top_comment_1', 'top_comment_2', 'top_comment_3', 'top_comment_4', 'top_comment_5'])
	for vote in votes:
		data=[]
		data.append(vote)
		data.append(votes[vote]['img_1'])
		data.append(votes[vote]['img_2'])
		data.append(top[vote][0][0])
		data.append(top[vote][1][0])
		data.append(top[vote][2][0])
		data.append(top[vote][3][0])
		data.append(top[vote][4][0])
		agg_output.writerow(data)

