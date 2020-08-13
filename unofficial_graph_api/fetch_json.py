from bs4 import BeautifulSoup as scrapper
import json

def auto_troubleshoot(response_):
    valid_iterator = 0
    soup = scrapper(response_, 'html.parser')
    scripts = soup.find_all('script')
    while True:
        if 's.handle(' in str(scripts[valid_iterator]):
            return valid_iterator
            break
        else:
            pass
        valid_iterator += 1

def get_json(response_, index_id):
    soup = scrapper(response_, 'html.parser')
    name = soup.find_all('script')
    json_data = str(name[index_id]).split('s.handle(')[1].split(');')[0]
    data = json.loads(json_data)
    return data
