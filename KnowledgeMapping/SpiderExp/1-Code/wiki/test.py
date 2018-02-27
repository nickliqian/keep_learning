import csv


csvFile = open("./test.csv", 'a', newline='', encoding='utf-8')
try:
    writer = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
    writer.writerow(['number', 'number plus 2', 'number times 2'])
    for i in range(10):
        writer.writerow([i, i+2, i*2])
finally:
    csvFile.close()