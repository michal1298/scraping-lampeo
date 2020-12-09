from bs4 import BeautifulSoup
from requests import get
import sys
import csv
import uuid
from pathlib import Path


# utworzenie folderu do przechowywania zdjęć:
Path("photos").mkdir(parents=True, exist_ok=True)

sys.argv[2] = int(sys.argv[2])      # zmiana string na int

def parse_price(price):  # zamiana stringa na liczbę zmiennoprzecinkową
    return price.replace(' ', '').replace('zł', '').replace(',', '.')

URL = sys.argv[1]       # podany link

page = get(URL)

number_of_products = 0  # liczba pobranych produktów
products_to_scraping = 0    # ilość produktów do pobrania; 0 jeśli ma zostać pobrana cała strona
products_to_scraping = sys.argv[2]      # podana ilość produktów

# w kategorii:
bs = BeautifulSoup(page.content, 'html.parser')
for offers in bs.find_all('li', class_='item'):
    for product_info in offers.find_all('div', class_='product-info'):
        product_name = offers.find('p', class_='product-name').get_text().strip()      # nazwa produktu
        manufacturer = offers.find('p', class_='product-manufacturer').get_text().strip()   # producent
        price_special = None
        for price_special_box in offers.find_all('p', class_='special-price'):
            price_special = parse_price(price_special_box.find('span', class_='price').get_text().strip())
            price_special = price_special.replace(u'\xa0', u'')
            price_special = float(price_special)
        regular_price = parse_price(offers.find('span', class_='price').get_text().strip())
        regular_price = regular_price.replace(u'\xa0', u'')
        regular_price = float(regular_price)

    # pobranie linku do aukcji:
    request = offers.find('a')
    request = (request['href'])     # link do aukcji
    request = get(request)

    # sprawdzenie kodu strony:
    if(request.status_code != 200):
        print('kod strony inny niż 200')
        break       #todo - można zrobić obsługę wyjątku

    # pobranie linku do następnej strony danej kategorii:
    next_page = None
    for page_section in bs.find_all('div', class_='toolbar toolbar-bottom'):
        try:
            next_page = page_section.find('a', class_='next')
            next_page = (next_page['href'])     # link do następnej strony w kategorii
        except:
            next_page = None

    # ---------------------------------------------------------------------------------------------------
    # w aukcji:
    bs_auction = BeautifulSoup(request.content, 'html.parser')
    for auction in bs_auction.find_all('div', class_='wrapper'):
        delivery = auction.find('span', class_='shipping').get_text().strip()  # czy darmowa dostawa

        # obliczenie kosztu wysyłki:
        if (delivery) == 'Należy doliczyć koszty wysyłki':
            if (price_special or regular_price) < 100.0:
                delivery_cost = 32.0
            elif(price_special or regular_price >= 100.0):
                delivery_cost = 20.0
        elif(delivery) == 'bezpłatna dostawa na terenie Polski\n, Dodatkowa opłata za dostawę artykułów o dużych gabarytach':
            delivery_cost = 35.0
        else:
            delivery_cost = 0.0

        # pobranie nazwy kategorii, w której znajduje się dany produkt:
        category_table = []
        for breadcrumbs in auction.find_all('div', class_='breadcrumbs clearfix'):
            for itemscope in breadcrumbs.find_all('li'):
                category_name = itemscope.find('span').get_text()
                category_table.append(category_name)

        # pobranie linków do zdjęć:
        photos = [] # tablica na linki do zdjęć
        for swiper_wrapper in auction.find_all('div', class_='swiper-wrapper'):     # wyszukiwanie linków do zdjęć .jpg
            for swiper_slide in swiper_wrapper.find_all('div', class_='swiper-slide'):
                #image = swiper_slide.find('source', type='image/jpeg')      # rozdzielczość 535x535
                image = swiper_slide.find('img')                             # rozdzielczość 1600x1600

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


                photos.append(image)        # dodanie zdjęć do listy / tablicy ze zdjęciami
                break       # by pojawiły się linki do wszystkich zdjęć, zakomentować tę linię

        # pobieranie zdjęć do katalogu photos/:
        image_name = image
        image_name = uuid.uuid4()
        image = get(image)
        with open('photos/{}'.format(image_name), 'wb') as f:
            f.write(image.content)

        # pobranie informacji o terminie dostawy:
        for product_collateral in auction.find_all('div', class_='product-collateral'):
            try:
                date_available = offers.find('p', {"class": ["availability replenishment date-available",
                                                             "availability in-stock date-available",
                                                             "availability in-stock date-available replenishment",
                                                             "availability replenishment date-available ",
                                                             "availability currently-not-available"]}).getText().strip()       # czas dostawy
            except:
                date_available = 'towar niedostępny'

            date_available = date_available.replace("Termin dostawy: ", "")#.replace(' dni', "").replace(' tygodni', '')

            # pobranie opisu i nagłówka opisu:
            description_title = None
            description = None
            for toggle_content in product_collateral.find_all("div", class_='toggle-content std'):
                try:
                    description_title = toggle_content.find('h2').get_text().strip()        # nagłówek opisu
                except:
                    description_title = ''

                try:
                    description = toggle_content.find('p').get_text().strip()       # opis
                except:
                    description = ''

            # zapisanie informacji o produkcie do listy słownikowej:
            headings = []       # klucz
            for product_specify in product_collateral.find_all('th'):
                product_specify = (product_specify.text).rstrip('\n')       # usunięcie \n
                headings.append(product_specify)

            properties = []     # wartość
            for product_properties in product_collateral.find_all('td'):
                product_properties = (product_properties.text).rstrip('\n')
                properties.append(product_properties)

            # połączenie obu tabel do listy słownikowej:
            merged_list_specify = {}
            for key in headings:
                for value in properties:
                    merged_list_specify[key] = value
                    properties.remove(value)
                    break

            product_table_feature = []      # nazwy cech właściwości produktu
            product_table_feature.append('nazwa produktu')
            product_table_feature.append('producent')
            product_table_feature.append('cena promocyjna')
            product_table_feature.append('cena')
            product_table_feature.append('koszt dostawy')
            product_table_feature.append('termin dostawy')
            product_table_feature.append('nagłówek opisu')
            product_table_feature.append('opis')
            #product_table_feature.append('specyfikacja')
            product_table_feature.append('zdjęcie')
            #print(product_table_feature)
            product_table_feature.append('kategoria 1')
            product_table_feature.append('kategoria 2')
            product_table_feature.append('kategoria 3')

            product_table = []          # właściwości produktu
            product_table.append(product_name)
            product_table.append(manufacturer)
            product_table.append(price_special)
            product_table.append(regular_price)
            product_table.append(delivery_cost)
            product_table.append(date_available)
            product_table.append(description_title)
            product_table.append(description)
            #product_table.append(merged_list_specify)
            product_table.append(image_name)
            #print(product_table)
            product_table.append(category_table[0])
            try:
                product_table.append(category_table[1])
            except:
                product_table.append("")
            try:
                product_table.append(category_table[2])
            except:
                product_table.append("")

            # utworzenie listy słownikowej z całością informacji o produkcie:
            product_all_info = {}
            for key in product_table_feature:
                for value in product_table:
                    product_all_info[key] = value
                    product_table.remove(value)
                    break
            print(product_all_info)

            # utworzenie pliku .csv do przechowywania danych o produktach:
            with open("export.csv", mode='a') as csv_file:
                fieldnames = ['nazwa produktu', 'producent', 'cena promocyjna', 'cena', 'koszt dostawy',
                              'termin dostawy',
                              'nagłówek opisu', 'opis', 'zdjęcie',
                              'kategoria 1', 'kategoria 2', 'kategoria 3']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                #writer.writeheader()  # nagłówki kategorii
                writer.writerow(product_all_info)  # dodanie informacji do pliku csv

    # zliczanie ilości pobranych produktów:
    number_of_products = number_of_products + 1
    if (number_of_products == products_to_scraping):
        break

    price_special = None    # kiedy produkt nie posiadał ceny promocyjnej, zapisywana została cena promocyjna z poprzedniego produktu
