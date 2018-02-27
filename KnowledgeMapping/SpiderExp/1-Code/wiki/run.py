import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "lxml")
table = bsObj.findAll("table",{"class":"wikitable"})[0]
rows = table.findAll("tr")
csvFile = open("./editors.csv", 'a', newline="", encoding='utf-8')
writer = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
            print(csvRow)
            writer.writerow(csvRow)
finally:
    csvFile.close()