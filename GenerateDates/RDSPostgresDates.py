import requests
import json
from bs4 import BeautifulSoup

AWS_DATES = "https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html"
JSON_FILE_NAME = "../Dates/RDSPostgres.json"


def get_html(Url):
    page = requests.get(Url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("table")
    return results.prettify()

def get_postgresl_rds_data(indent):

    content = get_html(AWS_DATES)
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")
    
    headers = {}
    thead = soup.find("thead")
    if thead:
        thead = soup.find_all("th")
        for i in range(len(thead)):
            headers[i] = thead[i].text.strip().lower().replace(' ', '_')
            
    data = []
    for row in rows:
        cells = row.find_all("td")
        if thead:
            items = {}
            if len(cells) > 3:
                for index in headers:
                    if index in (0,3):
                        items[headers[index]] = cells[index].text.strip()
        else:
            items = []
            for index in cells:
                items.append(index.text.strip())
        if items:
            data.append(items)
    return json.dumps(data, indent=indent)

if __name__ == "__main__":
    results = get_postgresl_rds_data(2)
    print(results,file=open(JSON_FILE_NAME, 'w'))