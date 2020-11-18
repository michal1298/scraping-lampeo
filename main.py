from bs4 import BeautifulSoup
from requests import get

URL_wiszace_do_kuchni = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'

page = get(URL_wiszace_do_kuchni)

bs = BeautifulSoup(page.content, 'html.parser')

for offers in bs.find_all('div', class_='category-products'):
    print(offers)