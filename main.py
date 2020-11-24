from bs4 import BeautifulSoup
from requests import get
import sys
#import time

print('podany link:', sys.argv[1])
print('podana ilość produktów:', sys.argv[2])
#print(type(sys.argv[2]))
sys.argv[2] = int(sys.argv[2])      # zmiana string na int
#print(type(sys.argv[2]))

def parse_price(price):  # zamiana stringa na liczbę zmiennoprzecinkową
    return price.replace(' ', '').replace('zł', '').replace(',', '.')

#URL = 'https://www.lampy.pl/lampy-wiszace-do-kuchni/'      # na tym linku początkowo robiłem
#URL = 'https://www.lampy.pl/oswietlenie-biurowe/'
URL = sys.argv[1]       # podany link

page = get(URL)

number_of_products = 0  # liczba pobranych produktów
products_to_scraping = 0    # ilość produktów do pobrania; 0 jeśli ma zostać pobrana cała strona
products_to_scraping = sys.argv[2]      # podana ilość produktów

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
        price_special = None
        for price_special_box in offers.find_all('p', class_='special-price'):
            price_special = parse_price(price_special_box.find('span', class_='price').get_text().strip())
            #price_special = price_special_box.find('span', class_='price').get_text().strip()
            price_special = price_special.replace(u'\xa0', u'')
            #price_special.replace(' ', '')
            #price_special.replace('zł', '')
            #price_special.replace(',', '.')
            price_special = float(price_special)
            print(price_special)
            #print(type(price_special))
        #regular_price = offers.find('span', class_='price').get_text().strip()
        #print(regular_price)
        regular_price = parse_price(offers.find('span', class_='price').get_text().strip())
        regular_price = regular_price.replace(u'\xa0', u'')
        #regular_price.replace(' ', '')
        #regular_price.replace('zł', '')
        #regular_price.replace(',', '.')
        #print('cena string:', regular_price)
        regular_price = float(regular_price)
        #print('cena float:', regular_price)
        print(regular_price)
        #print(type(regular_price))


    request = offers.find('a')
    #print(type(request))
    request = (request['href'])     # link do aukcji
    print(request)
    request = get(request)

    # sprawdzenie kodu:
    print(request.status_code)
    if(request.status_code != 200):
        print('kod strony inny niż 200')
        break
        #todo przejście do następnej oferty - tylko raz się ten błąd zdarzył:
        #todo https://www.lampy.pl/gu10-5-5w-840-led-zarowka-refl-superstar-36.html - 410
    next_page = None
    for page_section in bs.find_all('div', class_='toolbar toolbar-bottom'):
        #print(page_section)
        try:
            next_page = page_section.find('a', class_='next')
            next_page = (next_page['href'])     # link do następnej strony w kategorii
        except:
            next_page = None

    # ---------------------------------------------------------------------------------------------------
    # w aukcji:
    #print('aukcja:\n')
    bs_auction = BeautifulSoup(request.content, 'html.parser')
    #time.sleep(3)
    for auction in bs_auction.find_all('div', class_='wrapper'):
        delivery = auction.find('span', class_='shipping').get_text().strip()  # czy darmowa dostawa
        #delivery = delivery.rstrip("\n")
        print(delivery)
        #print('wszystkie znaki w wysyłce:')
        #print(repr(delivery))

        #float (price_special)
        #float (regular_price)
        if (delivery) == 'Należy doliczyć koszty wysyłki':
            #expensive_shipping = 100.0
            #expensive_shipping_str = str(expensive_shipping)
            #delivery_cost = 32.0
            if (price_special or regular_price) < 100.0:
                delivery_cost = 32.0
            #elif (price_special or regular_price) >= 100:
            elif(price_special or regular_price >= 100.0):
                delivery_cost = 20.0
        elif(delivery) == 'bezpłatna dostawa na terenie Polski\n, Dodatkowa opłata za dostawę artykułów o dużych gabarytach':
            delivery_cost = 35.0
        else:
            delivery_cost = 0.0

        print(delivery_cost)

        for product_collateral in auction.find_all('div', class_='product-collateral'):
            #print(product_collateral)

            #description = product_collateral.find('div', class_='toggle-content std').get_text()
            #print(description)

            try:
                date_available = offers.find('p', {"class": ["availability replenishment date-available", "availability in-stock date-available", "availability in-stock date-available replenishment", "availability replenishment date-available ", "availability currently-not-available"]}).getText().strip()       # czas dostawy
            except:
                date_available = 'towar niedostępny'
                #date_available['val1'].append(date_available.text if date_available else "towar niedostępny")
            # print('data:')

            date_available = date_available.replace("Termin dostawy: ", "")#.replace(' dni', "").replace(' tygodni', '')
            print(date_available)

            description_title = None
            description = None
            for toggle_content in product_collateral.find_all("div", class_='toggle-content std'):
                #print(toggle_content)
                try:
                    description_title = toggle_content.find('h2').get_text().strip()        # nagłówek opisu
                    print(description_title)
                except:
                    description_title = ''

                try:
                    description = toggle_content.find('p').get_text().strip()       # opis
                    print(description)
                except:
                    description = ''


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
            product_table.append(regular_price)
            product_table.append(delivery_cost)
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

        photos = [] # tablica na linki do zdjęć
        for swiper_wrapper in auction.find_all('div', class_='swiper-wrapper'):     # wyszukiwanie linków do zdjęć .jpg
            #print(swiper_wrapper)
            for swiper_slide in swiper_wrapper.find_all('div', class_='swiper-slide'):
                #print(swiper_slide)
                #image = swiper_slide.find('source', type='image/jpeg')      # rozdzielczość 535x535
                image = swiper_slide.find('img')                             # rozdzielczość 1600x1600
                #print(image)
                #image = image(attrs = {"img":"srcset"})
                #image = slice(image)

                # rozdzielczość 535x535:
                #try:
                #    image = (image['srcset'])
                #except:
                #    image = (image['data-srcset'])

                # rozdzielczość 1600x1600:
                try:
                    image = (image['data-src'])
                except:
                    image = (image['src'])

                #print(image)
                #image.replace('" type="image/jpeg"/>', '')
                #image = image["image/jpeg"]
                #print(image)

                photos.append(image)        # dodanie zdjęć do listy / tablicy ze zdjęciami
        print (photos)

    number_of_products = number_of_products + 1  # zliczanie ilości pobranych produktów
    if (number_of_products == products_to_scraping):
        break

    price_special = None    # kiedy produkt nie posiadał ceny promocyjnej, zapisywana została cena promocyjna z poprzedniego produktu
    print('\n')
    #break

print('następna strona aukcji:', next_page)    # link do następnej strony aukcji
print('ilość pobranych produktów:', number_of_products)

    #todo wysypało się, kiedy produktu już nie było, a był jeszcze wyświetlany w liście w kategorii, np B-Leuchten Miami lampa LED oświetlająca sufit - prawdopodobnie rozwiązane
    #todo sprawdzanie wersji danego produktu i informacji o nim
    #todo przejście do następnej strony