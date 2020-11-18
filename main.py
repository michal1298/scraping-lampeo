from bs4 import BeautifulSoup
from requests import get

URL_wiszace_do_kuchni = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'

page = get(URL_wiszace_do_kuchni)

bs = BeautifulSoup(page.content, 'html.parser')

for offers in bs.find('ul', class_='products-grid'):
    #print(offers)
    product_info = offers.find('p', class_='product-name').get_text()
    print(product_info)

    #break