
data = open('../data/majority_workers.txt', 'r')

arr = []

for record in data:
	worker_arr = record.split( )
	if (worker_arr[0] != '_worker_id'):
		arr.append([worker_arr[0], float(worker_arr[1])])

print arr
