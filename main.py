from bs4 import BeautifulSoup
from requests import get

URL_wiszace_do_kuchni = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'

page = get(URL_wiszace_do_kuchni)

# strona kategorii:
bs = BeautifulSoup(page.content, 'html.parser')
for offers in bs.find_all('li', class_='item'):
    #print(offers)
    for product_info in offers.find_all('div', class_='product-info'):
        #print('druga pętla:')
        #print(product_info)
        manufacturer = offers.find('p', class_='product-manufacturer').get_text()
        #print('producent:')
        print(manufacturer)
        price_box = offers.find('div', class_='price-box-entities').get_text()
        #print('koszt:')
        print(price_box)

    #todo modify:
    #price_old = offers.find('span', class_='price').get_text()
    #print(price_old)
    #price = offers.find('span', class_='price').get_text()  #TODO zmienić
    #print(price)

    #date_available = offers.find('p', class_='availability in-stock date-available' or 'availability in-stock date-available').get_text()
    #print('data:')
    #print(date_available)

    url_auction = offers.find('a')
    url_auction = (url_auction['href'])
    print(url_auction)
    url_auction = get(url_auction)

    # ---------------------------------------------------------------------------------------------------
    # in auction:
    #print('aukcja:\n')
    bs_auction = BeautifulSoup(url_auction.content, 'html.parser')
    for auction in bs_auction.find_all('div', class_='wrapper'):
        delivery = auction.find('span', class_='shipping').get_text()
        print(delivery)
        for product_collateral in auction.find_all('div', class_='product-collateral'):
            #print(product_collateral)

            #todo do dopracowania - pokazuje się niepotrzebne 'pobierz':
            description = product_collateral.find('div', class_='toggle-content std').get_text()
            print(description)

            product_specify = product_collateral.find('table', class_='toggle-content zebra-table').get_text()
            print(product_specify)

        #todo darmowa dostawa:
        #for cart_benefits in auction.find_all('strong', class_='span'):
            #print(cart_benefits)
        #for shipping in auction.find('span', class_='shipping').get_text():
            #print(shipping)

    print('\n')
    #break