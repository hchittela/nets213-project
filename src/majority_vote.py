import sys
import csv
import json

# idCol = 19
# labelCol = 15
# workerIDCol = 9

idCol = 19
labelCol = 12
workerIDCol = 7

def getLabels(filename):
  f = open(filename)
  csv_f = csv.reader(f)

  img_1VoteCount = {}
  img_2VoteCount = {}
  labels = {}

  for row in csv_f:
    img_1VoteCount.setdefault(row[idCol], 0)
    img_2VoteCount.setdefault(row[idCol], 0)

    if row[labelCol] == "img_1":
      if row[idCol] in img_1VoteCount:
        img_1VoteCount[row[idCol]] += 1
      else:
        img_1VoteCount[row[idCol]] = 1
    elif row[labelCol] == "img_2":
      if row[idCol] in img_2VoteCount:
        img_2VoteCount[row[idCol]] += 1
      else:
        img_2VoteCount[row[idCol]] = 1

  for ids in img_1VoteCount.iterkeys():
    img_1Count = img_1VoteCount.get(ids, 0)
    img_2Count = img_2VoteCount.get(ids, 0)

    if (img_1Count > img_2Count):
      labels[ids] = "img_1"
    else:
      labels[ids] = "img_2"

  f.close()
  return labels



def getQualities(filename, labels):
  f = open(filename)
  csv_f = csv.reader(f)

  imgs = {}
  qualities = {}

  for row in csv_f:
    key = row[workerIDCol]
    imgs.setdefault(key, [])
    imgs[key].append((row[idCol], row[labelCol]))

  for worker in imgs.iterkeys():
    sum = 0

    for tup in imgs[worker]:
      if (tup[0] in labels):
        if (tup[1] == labels[tup[0]]):
          sum += 1

    qualities.setdefault(worker, [])
    qualities[worker] = float(1.0/len(imgs[worker])) * sum

  f.close()
  return qualities


def writeToFile(dict, filename):
  # target = open(filename, 'w')
  #
  # for k in sorted(dict):
  #   target.write(k.strip() + '\t' + str(dict[k]).strip() + '\n')
  #
  # target.close()

  with open(filename, 'w') as fp:
    json.dump(dict, fp)

  fp.close()

if __name__ == '__main__':
  idLabels = getLabels('../data/f904543.csv')
  writeToFile(idLabels, '../data/904543_majority_data.txt')

  workerQualities = getQualities('../data/f904543.csv', idLabels)
  writeToFile(workerQualities, '../data/904543_majority_workers.json')
