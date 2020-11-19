from bs4 import BeautifulSoup
from requests import get
#import time

def parse_price(price):  # zamiana stringa na liczbę zmiennoprzecinkową
    return price.replace(' ', '').replace('zł', '').replace(',', '.')

URL = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'      # na tym linku początkowo robiłem
#URL = 'https://www.lampy.pl/oswietlenie-wewnetrzne/sypialnia-ra/'

page = get(URL)

# w kategorii:
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
    url_auction = (url_auction['href'])     # link do aukcji
    print(url_auction)
    url_auction = get(url_auction)

    # ---------------------------------------------------------------------------------------------------
    # w aukcji:
    #print('aukcja:\n')
    bs_auction = BeautifulSoup(url_auction.content, 'html.parser')
    #time.sleep(2)
    for auction in bs_auction.find_all('div', class_='wrapper'):
        delivery = auction.find('span', class_='shipping').get_text().rstrip('\n').strip()  # czy darmowa dostawa
        print(delivery)

        #float (price_special)
        #float (regular_price)
        if (delivery) == 'Należy doliczyć koszty wysyłki':
            expensive_shipping = 100.0
            expensive_shipping_str = str(expensive_shipping)
            #delivery_cost = 32.0
            if (price_special or regular_price) < expensive_shipping_str:
                delivery_cost = 32.0        #todo nigdy nie ma 32; ciągle jest 20
                break
            #elif (price_special or regular_price) >= 100:
            elif(price_special or regular_price > expensive_shipping_str):
                delivery_cost = 20.0
        elif(delivery) == 'bezpłatna dostawa na terenie Polski , Dodatkowa opłata za dostawę artykułów o dużych gabarytach':        #todo nie działa - jest tam znak nowej linii
            delivery_cost = 35.0
            #break
        else:
            delivery_cost = 0.0

        print(delivery_cost)

        for product_collateral in auction.find_all('div', class_='product-collateral'):
            #print(product_collateral)

            #description = product_collateral.find('div', class_='toggle-content std').get_text()
            #print(description)

            date_available = offers.find('p', {"class": ["availability replenishment date-available", "availability in-stock date-available", "availability in-stock date-available replenishment", "availability replenishment date-available ", "availability currently-not-available"]}).getText().strip()       # czas dostawy
            # print('data:')

            date_available = date_available.replace("Termin dostawy: ", "")#.replace(' dni', "").replace(' tygodni', '')
            print(date_available)
                                    #todo Żarówka LED E27 ToLEDo RT A60 7W przezroczysta się wysypuje
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

            headings = []       # nazwy kategorii
            for product_specify in product_collateral.find_all('th'):
                #print(product_specify_head)
                product_specify = (product_specify.text).rstrip('\n')       # usunięcie \n
                headings.append(product_specify)
            #print(headings)

            #number_of_rows = 0     # liczba właściwości
            properties = []     # do specyfikacji
            for product_properties in product_collateral.find_all('td'):
                #number_of_rows = number_of_rows + 1
                #print(product_properties_head)
                product_properties = (product_properties.text).rstrip('\n')
                properties.append(product_properties)
            #print(properties)

            #print('liczba właściwości:')
            #print(number_of_rows)

            # merge two list into single one:
            #columns = 2
            #row = number_of_rows

            #merged_list_specify = [[0 for x in range(row)] for y in range(columns)]     # lista z samymi zerami
            merged_list_specify = {}
            for key in headings:
                for value in properties:
                    merged_list_specify[key] = value
                    properties.remove(value)
                    break


            print(merged_list_specify)

            #print('pętla for:')
            #x = 0
            #for x in headings:
            #    print(x)
            #for x in properties:
            #    print(x)


            product_table_feature = []      # nazwy cech właściwości produktu
            product_table_feature.append('nazwa produktu')
            product_table_feature.append('producent')
            product_table_feature.append('cena promocyjna')
            product_table_feature.append('cena')
            product_table_feature.append('koszt dostawy')
            product_table_feature.append('termin dostawy')
            product_table_feature.append('nagłówek opisu')
            product_table_feature.append('opis')
            product_table_feature.append('specyfikacja')
            #print(product_table_feature)


            product_table = []          # właściwości produktu
            product_table.append(product_name)
            product_table.append(manufacturer)
            product_table.append(price_special)
            product_table.append(regular_price)     #todo usunąć \xa0
            product_table.append(delivery_cost)     #todo usunąć \xa0
            product_table.append(date_available)
            product_table.append(description_title)
            product_table.append(description)
            product_table.append(merged_list_specify)
            #print(product_table)


            # merge feature and properties of product:
            product_all_info = {}
            for key in product_table_feature:
                for value in product_table:
                    product_all_info[key] = value
                    product_table.remove(value)
                    break
            print(product_all_info)

        #for cart_benefits in auction.find_all('strong', class_='span'):
            #print(cart_benefits)
        #for shipping in auction.find('span', class_='shipping').get_text():
            #print(shipping)

    print('\n')
    #break

    #todo wysypało się, kiedy produktu już nie było, a był jeszcze wyświetlany w liście w kategorii, np B-Leuchten Miami lampa LED oświetlająca sufit