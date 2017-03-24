from datetime import date
from datetime import datetime
from datetime import timedelta

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import lxml


homes = ['ORD', 'MDW']
destinations = ['PUQ', 'LAS', 'PDX', 'ANC', 'MSY', 'YYZ', 'OPO', 'LIS', 'RAK',
                'GVA', 'PRG', 'AMS', 'KRK', 'BUD', 'OSL', 'TRD', 'BMA', 'LED',
                'SVO', 'VKO', 'DME', 'MEL', 'SYD', 'WLG', 'AKL']

vacation_days = 7
travellers = 2


def get_date_range():
    start_date = date.today()
    depart_date = start_date + timedelta(days=30)
    return_date = depart_date + timedelta(days=vacation_days)

    return([depart_date, return_date])


def get_search_link(home, destination):
    depart_date = get_date_range()[0]
    return_date = get_date_range()[1]
    url = 'https://www.kayak.com/flights/%s-%s/%s/%s/%sadults' % (home, destination,
                                                                 depart_date, return_date,
                                                                 travellers)

    return(url)


def run_flight_search():
    page = urlopen(get_search_link('ORD', 'PUQ'))
    soup = BeautifulSoup(page.read(), 'lxml')   
    price = soup.find('div', {'class': 'bigPrice'})
    print(price)
    print(soup)

    # for link in soup.find_all('a id'):
    #     print(link.get('href'))
    



run_flight_search()




# htmlfile = urllib.urlopen(html)
# htmltext = htmlfile.read()

# re1 = '<div class="GHOFUQ5BGJC">(.+?)</div>'
# pattern1 = re.compile(re1)
# price = re.findall(pattern1, htmltext)
# re2 ='<div class="GHOFUQ5BMFC">(.+?)</div>'
# pattern2 = re.compile(re2)
# airline = re.findall(pattern2, htmltext)

# print(price)
# print(airline)
