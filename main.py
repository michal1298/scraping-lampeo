from bs4 import BeautifulSoup
from requests import get
#import time

def parse_price(price):  # zamiana stringa na liczbę zmiennoprzecinkową
    return price.replace(' ', '').replace('zł', '').replace(',', '.')

#URL = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'
URL = 'https://www.lampy.pl/oswietlenie-wewnetrzne/sypialnia-ra/'

page = get(URL)

# in category:
bs = BeautifulSoup(page.content, 'html.parser')
for offers in bs.find_all('li', class_='item'):
    #print(offers)
    for product_info in offers.find_all('div', class_='product-info'):
        #print('druga pętla:')
        #print(product_info)
        product_name = offers.find('p', class_='product-name').get_text().strip()      # nazwa produktu
        #print('product name:')
        print(product_name)
        manufacturer = offers.find('p', class_='product-manufacturer').get_text().strip()   # producent
        #print('producent:')
        print(manufacturer)
        #price_box = offers.find('div', class_='price-box-entities').get_text()      # cena
        #print('koszt:')
        #print(price_box)
        #for price_old_box in offers.find_all('p', class_='old-price'):
            #print(price_old_box)
            #price_old = parse_price(price_old_box.find('span', class_='price').get_text())
            #print(price_old)
        for price_special_box in offers.find_all('p', class_='special-price'):
            price_special = parse_price(price_special_box.find('span', class_='price').get_text().strip())
            print(price_special)
        #regular_price = offers.find('span', class_='price').get_text().strip()
        #print(regular_price)
        regular_price = parse_price(offers.find('span', class_='price').get_text().strip())
        print(regular_price)


    url_auction = offers.find('a')
    url_auction = (url_auction['href'])
    print(url_auction)                      # link do aukcji
    url_auction = get(url_auction)

    # ---------------------------------------------------------------------------------------------------
    # in auction:
    #print('aukcja:\n')
    bs_auction = BeautifulSoup(url_auction.content, 'html.parser')
    #time.sleep(2)
    for auction in bs_auction.find_all('div', class_='wrapper'):
        delivery = auction.find('span', class_='shipping').get_text().rstrip('\n').strip()
        print(delivery)

        #float (price_special)
        #float (regular_price)
        if(delivery) == 'Należy doliczyć koszty wysyłki':
            expensive_shipping = 100.0
            expensive_shipping_str = str(expensive_shipping)
            #delivery_cost = 32.0
            if(price_special or regular_price) < expensive_shipping_str:
                delivery_cost = 32.0        #todo nigdy nie ma 32
            #elif (price_special or regular_price) >= 100:
            elif(price_special or regular_price) >= expensive_shipping_str:
                delivery_cost = 20.0
        elif(delivery) == 'bezpłatna dostawa na terenie Polski , Dodatkowa opłata za dostawę artykułów o dużych gabarytach':        #todo nie działa
            delivery_cost = 35.0
        else:
            delivery_cost = 0.0

        print(delivery_cost)

        for product_collateral in auction.find_all('div', class_='product-collateral'):
            #print(product_collateral)

            #description = product_collateral.find('div', class_='toggle-content std').get_text()
            #print(description)

            date_available = offers.find('p', {"class": ["availability replenishment date-available", "availability in-stock date-available", "availability in-stock date-available replenishment", "availability replenishment date-available ", "availability currently-not-available"]}).getText().strip()
            # print('data:')
            print(date_available)   #todo Żarówka LED E27 ToLEDo RT A60 7W przezroczysta się wysypuje
                                    #todo ICONE Vera ST - designerska lampa stojąca LED
                                    #todo Lampa LED oświetlająca sufit Felicja z lampką
                                    #todo https://www.lampy.pl/foscarini-twiggy-be-colour-lampa-lukowa-led.html wysypuje się, bo na początku wyświetla się 'niedostępny', później zmienia się na 2-3 tygodnie

            for toggle_content in product_collateral.find_all("div", class_='toggle-content std'):
                #print(toggle_content)
                description_title = toggle_content.find('h2').get_text().strip()        # nagłówek opisu
                print(description_title)

                description = toggle_content.find('p').get_text().strip()       # opis
                print(description)






            #product_specify = product_collateral.find('table', class_='toggle-content zebra-table').get_text()
            #print(product_specify)

            headings = []   # for categories names
            for product_specify in product_collateral.find_all('th'):
                #print(product_specify_head)
                product_specify = (product_specify.text).rstrip('\n')       # delete \n
                headings.append(product_specify)
            print(headings)

            properties = []     # for specify
            for product_properties in product_collateral.find_all('td'):
                #print(product_properties_head)
                product_properties = (product_properties.text).rstrip('\n')
                properties.append(product_properties)
            print(properties)



        #todo darmowa dostawa - jest uzależniona od wartości kupionego przedmiotu
        #for cart_benefits in auction.find_all('strong', class_='span'):
            #print(cart_benefits)
        #for shipping in auction.find('span', class_='shipping').get_text():
            #print(shipping)

    print('\n')
    #break

    #todo wysypało się, kiedy produktu już nie było, a był jeszcze wyświetlany w liście w kategorii, np B-Leuchten Miami lampa LED oświetlająca sufit