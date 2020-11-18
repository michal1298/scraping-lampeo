from bs4 import BeautifulSoup
from requests import get

URL_wiszace_do_kuchni = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'

page = get(URL_wiszace_do_kuchni)

bs = BeautifulSoup(page.content, 'html.parser')

for offers in bs.find('ul', class_='products-grid'):
    #print(offers)
    product_info = offers.find('p', class_='product-name').get_text()
    print(product_info)
    manufacturer = offers.find('p', class_='product-manufacturer').get_text()
    print(manufacturer)

    price_box = offers.find('div', class_='price-box-entities').get_text()
    print(price_box)

    #todo modify:
    #price_old = offers.find('span', class_='price').get_text()
    #print(price_old)
    #price = offers.find('span', class_='price').get_text()  #TODO zmienić
    #print(price)


    date_available = offers.find('p', class_='availability in-stock date-available').get_text()
    print(date_available)

    url_auction = offers.find('a')
    url_auction = (url_auction['href'])
    print(url_auction)
    url_auction = get(url_auction)


    # in auction:
    bs_auction = BeautifulSoup(url_auction.content, 'html.parser')
    for auction in bs_auction.find_all('div', class_='wrapper'):
        delivery = auction.find('span', class_='shipping').get_text()
        print(delivery)
        for product_collateral in auction.find_all('div', class_='product-collateral'):
            #print(product_collateral)
            description = product_collateral.find('div', class_='toggle-content std').get_text()
            print(description)

        #todo darmowa dostawa:
        #for cart_benefits in auction.find_all('strong', class_='span'):
            #print(cart_benefits)
        #for shipping in auction.find('span', class_='shipping').get_text():
            #print(shipping)

    print('\n')
    break