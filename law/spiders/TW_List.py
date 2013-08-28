import csv
def TW_list():
	with open('6a.csv','rb') as csvfile:
		read = csv.reader(csvfile, delimiter=',')
		for row in read:
			return row
