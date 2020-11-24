# Scraping Lampeo

## Requirements
- python3
- pip3
## Preparation in project folder
```
pip install bs4
pip install requests
```
## Run
```
python3 main.py URL_to_category_page numer_of_products
```
Example:
```
python3 main.py https://www.lampy.pl/oswietlenie-biurowe/ 5
```
It will scrap 5 products from category "oświetlenie biurowe".