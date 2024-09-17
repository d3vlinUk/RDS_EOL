import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
from dateutil import parser as date_parser
from datetime import datetime

LAMBDA_DATES = "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html"
RDS_PG_DATES = "https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html"
JSON_FILE_NAME = "../Dates/AWS_Eol_Dates.json"


def removeCharacters(string):
    sub_list = ["*", "-",".x"]
    for sub in sub_list:
        string = string.replace(sub, '')
    return string

def parseHTML(DatesUrl):
    page = requests.get(DatesUrl)
    return BeautifulSoup(page.content,"html.parser")

def parseTable(params={}):
    soup = parseHTML(params['DatesUrl'])
    tables = soup.find_all("table")
    return BeautifulSoup(str(tables[params['TableId']]),"html.parser")

def is_date_parsing(date_str):
    try:
        return bool(date_parser.parse(date_str))
    except ValueError:
        return False

def is_date_matching(date_str):
    try:
        return bool(datetime.strptime(date_str, '%b %d, %Y'))
    except ValueError:
        return False

def convertDate(input):
    if (is_date_matching(input)):
        return input
    else:
        if (is_date_parsing(input)):
            date = date_parser.parse(input).date()
            return date.strftime('%b %d, %Y')
    return input

def isStringEmpty(string):
    if(len(string) == 0):
        return True
    return False

def getDates(params = {}):
    soup = parseTable(params)    
    rows = soup.find_all("tr")

    data = []
    for row in rows:
        cells = row.find_all("td")
        items = {}
        if len(cells) > 3:
            for index in params['TableIndex']:
                # Ignore the data if it's empty/not present
                if isStringEmpty(cells[3].text.strip()) == False:
                    string = removeCharacters(cells[index].text.strip())
                    match index:
                        case value if value == params['TableIndex'][0]:
                            headerIndex = 'Version'
                        case value if value == params['TableIndex'][1]:
                            headerIndex = 'Date'
                            string = convertDate(string)
                    items[headerIndex] = string
        if items:
            data.append(items)

    return data

if __name__ == "__main__":
    
    jsondata = {}
    jsondata['lambda'] = getDates({'DatesUrl':LAMBDA_DATES,'TableId':0,'TableIndex':[1,3]})
    jsondata['RDS_PG'] = getDates({'DatesUrl':RDS_PG_DATES,'TableId':1,'TableIndex':[0,3]})
    
    print(json.dumps(jsondata, indent=2))
    print(json.dumps(jsondata, indent=2),file=open(JSON_FILE_NAME, 'w'))
