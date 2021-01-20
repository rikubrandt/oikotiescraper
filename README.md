# Oikotie Scraper

### scrape.py
```python scrape.py ```

Scrapes houses that are being sold at the moment from Vantaa.
Change the baseURL to different location if you want.

### main.py
``` python main.py ```

Check the average price per squares by running averageValueOfDistrict()

### houses.json
Scraped and cleaned houses of Vantaa.
Json is in this format:
Price, Charges, Squares, rooms, floor, year of construction, House type, District, City

You will have to clean the Json with command cleanJSON() in scrape.py because not all houses have the charges informed.
