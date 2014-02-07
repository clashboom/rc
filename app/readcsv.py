import csv

db = open('db.csv', 'rb')
reader = csv.reader(db, delimiter=";")

output = open('fdb.csv', 'wb')
writer = csv.writer(output)

for row in reader:
    writer.writerow(row[:-1])

db.close()
output.close()
