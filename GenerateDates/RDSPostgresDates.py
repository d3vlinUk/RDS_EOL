import requests
import json
from bs4 import BeautifulSoup

AWS_DATES = "https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html"
JSON_FILE_NAME = "../Dates/RDSPostgres.json"

def stripName(string):
    strings = ['version','date']
    string = string.text.strip().lower().split(" ")
    flag=0
    for i in string:
        for j in strings:
            if i==j:
                return j.title()
    return ""        

def removeCharacters(string):
    sub_list = ["*", "-"]
    for sub in sub_list:
        string = string.replace(sub, '')
    return string

def parseHTML():
    page = requests.get(AWS_DATES)
    return BeautifulSoup(page.content,"html.parser")

def parseTable(soup,params={}):
    tables = soup.find_all("table")
    return BeautifulSoup(str(tables[params['TableId']]),"html.parser")

def addMissingDay(input):
    if input and input.lstrip()[0].isalpha(): 
        return "01 "+input
    return input

def get_data(params = {}):

    soup = parseTable(parseHTML(),params)    
    rows = soup.find_all("tr")
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = soup.find_all("th")
        for i in range(len(thead)):
            headers[i] = stripName(thead[i])
            
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            if len(cells) > 3:
                for index in headers:
                    if index in (0,3): 
                        string = removeCharacters(cells[index].text.strip())
                        if index == 3:
                            string = addMissingDay(string)
                        items[headers[index]] = string
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        if items:
            data.append(items)
    return json.dumps(data, indent=2)

if __name__ == "__main__":
    params = {
    'TableId':1
    }
    results = get_data(params)
    print(results,file=open(JSON_FILE_NAME, 'w'))
