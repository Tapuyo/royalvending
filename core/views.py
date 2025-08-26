
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from core.models import Product
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse
import threading
import re
import hashlib


def fetch_remedydrinks_products():
    url = "https://www.remedydrinks.com/collections/all/products.json"
  
    params = {
        "limit": "1000",
        # "page": 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json().get("products", [])


def remedydrinks(remedy_list):
    # remedy_list = []
    products_data = fetch_remedydrinks_products()
    print(products_data)
    
    for item in products_data:
        print('#####################')
      
        id = item.get("id", "")
        name = item.get("title", "Unnamed Product")
        body = item.get("body_html", "n/a"),
        print(item)
        prices = item.get("variants", [{}])[0]
        price = prices.get("price", "")
        slug = item.get("urlSlugText", "")
        images_url = item.get("images", [{}])[0]
        image_url = images_url.get("src", "")
        product_url = f"https://www.remedydrinks.com/products/{slug}"
        # category = item.get("product_type", "all")
        
        remedy_list.append({
                'name': name,
                'image_url': image_url,
                'product_link': product_url,
                'currentPrice': price,
                'carton_price': '0',
                'single_price': '0',
                'category': 'Drinks',
                'code': id,
                'item_body': body
            })


        Product.objects.update_or_create(
            item_code=id,
            defaults={
                'name': name,
                'current_price': price,
                'image_url': image_url,
                'product_link': product_url,
                'category': 'Drinks',
                'supplier': 'Remedy drinks',
                'supplier_url': 'https://www.remedydrinks.com/',
                'item_body': body
            }
        )
        time.sleep(0.1)
            

    # remedy_list = Product.objects.all()
    # return render(request, 'core/home.html', {'product_info_list': remedy_list})
    

def fetch_fintessvending_products(limit=300, offset=0):
    url = "https://www.fitnessvending.com/collections/all/products.json"
  
    params = {
        "limit": "1000",
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json().get("products", [])

# fitnessvending
def fitnessvending(fitness_list):
    fitness_list = []
    products_data = fetch_fintessvending_products(limit=300, offset=0)

    for item in products_data:
        print('#####################')
        print(item)
        id = item.get("id", "")
        name = item.get("title", "Unnamed Product")
        body = item.get("body_html", "n/a"),
        prices = item.get("variants", [{}])[0]
        price = prices.get("price", "")
        slug = item.get("urlSlugText", "")
        images_url = item.get("images", [{}])[0]
        image_url = images_url.get("src", "")
        product_url = f"https://www.fitnessvending.com/products/{slug}"
        category = item.get("product_type", "all")
        
        fitness_list.append({
                'name': name,
                'image_url': image_url,
                'product_link': product_url,
                'currentPrice': price,
                'carton_price': '0',
                'single_price': '0',
                'category': category,
                'code': id,
                'item_body' : body
            })


        Product.objects.update_or_create(
            item_code=id,
            defaults={
                'name': name,
                'current_price': price,
                'image_url': image_url,
                'product_link': product_url,
                'category': category,
                'supplier': 'Fitness Vending',
                'supplier_url': 'https://www.fitnessvending.com/',
                'item_body' : body
            }
        )
        time.sleep(0.1)
            
            

    # products = Product.objects.all()
    # return render(request, "core/home.html", {"product_info_list": fitness_list})




# # Aldi https://www.aldi.com.au/
# from django.shortcuts import render
# from .models import Product
# import requests

def fetch_aldi_products(limit=30, offset=0):
    url = "https://api.aldi.com.au/v3/product-search"
    params = {
        "currency": "AUD",
        "serviceType": "walk-in",
        "limit": limit,
        "offset": offset,
        "getNotForSaleProducts": 1,
        "sort": "relevance",
        "testVariant": "A",
        "servicePoint": "G452"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json().get("data", [])

# aldi
def aldi(product_list):
    products_data = fetch_aldi_products(limit=30, offset=0)
    # product_list = []

    for item in products_data:
        code = item.get("sku", "Unnamed Product")
        name = item.get("name", "Unnamed Product")
        print(item)
        body = item.get("urlSlugText", "n/a"),
        price = item.get("price", {}).get("amountRelevantDisplay", "N/A")
        categories = item.get("categories", [])
        category = categories[0]["name"] if categories else "all"
        slug = item.get("urlSlugText", "")
        product_url = f"https://www.aldi.com.au/product/{slug}" if slug else ""

        # Image - use the first asset if available
        assets = item.get("assets", [])
        image_url = ""
        if assets:
            raw_url = assets[0].get("url", "")
            if "{width}" in raw_url:
                image_url = raw_url.replace("{width}", "600").replace("{slug}", slug)
                
        bodyString = body[0]
        
        product_list.append({
                'name': name,
                'image_url': image_url,
                'product_link': product_url,
                'currentPrice': price,
                'carton_price': '0',
                'single_price': '0',
                'category': category,
                'code': code,
                'item_body': re.sub(r'[^A-Za-z0-9]', ' ', bodyString)
            })
        
        Product.objects.update_or_create(
            item_code=code,
            defaults={
                'name': name,
                'current_price': price,
                'image_url': image_url,
                'product_link': product_url,
                'category': category,
                'supplier': 'Aldi',
                'supplier_url': 'https://www.aldi.com.au/',
                'item_body': re.sub(r'[^A-Za-z0-9]', ' ', bodyString)
            }
        )
        time.sleep(0.1)

    # products = Product.objects.all()
    # return render(request, "core/home.html", {"product_info_list": product_list})





# # kellysdistributors
# from django.shortcuts import render
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# kellysdistributors
def kellysdistributors(products_data):
    # products_data = []
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless scraping
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_KELLY = {
        "alkaline-water": "Alkaline Water",
        "carbonated-drinks": "Carbonated Drinks",
        "alchemy-2": "Alchemy",
        "arkadia-beverages-2": "Arkadia Beverages",
        "byron-bay-cookies-2": "Byron Bay Cookies",
        "edlyn-toppings-2": "Edlyn Toppings",
        "elixirs-latte-powder-4": "Elixirs Latte Powder",
        "little-bakes-2": "Little Bakes",
        "naked-syrups-2": "Naked Syrups",
        "origin-tea-2": "Origin Tea",
        "stevia-sugar-2": "Stevia Sugar",
        "coconut-water": "Coconut Water",
        "coffee-drinks": "Coffee Drinks",
        "confectionery": "Confectionery",
        "energy-drinks": "Energy Drinks",
        "tradie-energy": "Tradie Energy",
        "enhanced-water": "Enhanced Water",
        "flavoured-milks": "Flavoured Milks",
        "flavoured-water": "Flavoured Water",
        "grocery-products": "Grocery Products",
        "health-drinks": "Health Drinks",
        "iced-tea": "Iced Tea",
        "juices": "Juices",
        "coconut-water-smoothies-2": "Coconut Water Smoothies",
        "fruit-juices-4": "Fruit Juices",
        "prebiotic-smoothies-2": "Prebiotic Smoothies",
        "smoothies-2": "Smoothies",
        "veggie-juices-2": "Veggie Juices",
        "fruity-burst-2": "Fruity Burst",
        "lemonades": "Lemonades",
        "plant-based-milks": "Plant Based Milks",
        "snacks": "Snacks",
        "soda": "Soda",
        "sparkling-coconut-water": "Sparkling Coconut Water",
        "sports-drinks": "Sports Drinks",
        "the-raw-treats": "The Raw Treats",
        "takeaway-packaging": "Takeaway Packaging",
        "water": "Water"
    }

    base_url = "https://kellysdistributors.com.au/product-category"
    # products_data = []

    try:
        for slug, category_name in CATEGORY_MAP_KELLY.items():
            print(f"\n=== Category: {category_name} ===")
            for page in range(1, 5):
                page_url = f"{base_url}/{slug}/page/{page}/"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(6)

                product_cards = driver.find_elements(By.CSS_SELECTOR, "ul.products li.product")
                if not product_cards:
                    print(f"No more products in {category_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        name = card.find_element(By.CSS_SELECTOR, "h2.woocommerce-loop-product__title").text.strip()

                        image_url = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

                        link = card.find_element(By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link").get_attribute("href")

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span.woocommerce-Price-amount").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        sku = link.split("/")[-2] if link else "N/A"

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": "",
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'category': category_name,
                                'supplier': "Kelly’s Distributors",
                                'supplier_url': "https://kellysdistributors.com.au/"
                            }
                        )
                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})



# # www.harcher.com.au
# from django.shortcuts import render
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import urllib.parse
# harcher
def harcher(products_data):
    # products_data = []
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless scraping
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_HARCHER = [
        "Beverages",
        "Chocolate",
        "Grocery",
        "Gum+%26+Mints",
        "Health+%26+Beauty",
        "Lollies",
        "Novelty",
        "Snacks",
        "Top+Sellers"
    ]

    base_url = "https://www.harcher.com.au/shopd"
    # products_data = []

    try:
        for cat in CATEGORY_MAP_HARCHER:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.harcher.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.harcher.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })
                        
                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Harcher',
                                'supplier_url': 'https://www.harcher.com.au/'
                            }
                        )
                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})









# # Campbells
# from django.shortcuts import render
# from bs4 import BeautifulSoup
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

CATEGORY_MAP_CAMPBELL = {
    "117": "Baby",
    "15": "Bakery",
    "06": "Beverages",
    "18": "Food",
    "92": "Coffee & Tea",
    "10": "Biscuits",
    "13": "Household",
    "85": "Health & Beauty",
    "11": "Office",
    "17": "Chilled",
    "09": "Catering",
    "08": "Paper & Disposables",
    "19": "Frozen",
    "01": "New Products",
    "07": "Grocery",
    "16": "Specials"
}

def slow_scroll(driver, times=10, delay=5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_authenticated_content(login_url, category_id, username, password, max_pages=382):
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    pages_source = []

    try:
        driver.get(login_url)
        wait = WebDriverWait(driver, 10)

        # Login
        username_input = wait.until(EC.presence_of_element_located((By.ID, "customerIDInput")))
        password_input = wait.until(EC.presence_of_element_located((By.ID, "passwInput")))
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait for redirect after login

        for page in range(1, max_pages + 1):
            page_url = f"https://campbells.sorted.au/c/{category_id}?query=:relevance&currentPage={page}"
            driver.get(page_url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "olympus-plp-item"))
                )
            except:
                print(f"[SKIP] No content on category {category_id} page {page}")
                break

            slow_scroll(driver, times=5, delay=5)

            print(f"[CATEGORY {category_id}] Page {page}")
            pages_source.append(driver.page_source)

    except Exception as e:
        print(f"[ERROR] Failed for category {category_id}: {e}")
    finally:
        driver.quit()

    return pages_source

def extract_product_info(html_pages, category_name):
    product_list = []

    for html in html_pages:
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('olympus-plp-item')
        print(items)

        for item in items:
            print(item)
            name_tag = item.find('p', class_='item-name')
            name = name_tag.get_text(strip=True) if name_tag else 'Unnamed Product'

            link_tag = item.find('a', href=True)
            product_link = f"https://campbells.sorted.au{link_tag['href']}" if link_tag else ''

            image_tag = item.find('img')
            image_url = (
                image_tag.get('src') or
                image_tag.get('data-src') or
                image_tag.get('ng-src') or
                ''
            ) if image_tag else ''

            item_code_tag = item.find('p', class_='item-code')
            item_code = 'N/A'
            if item_code_tag:
                item_code_text = item_code_tag.get_text(strip=True)
                if 'Item code:' in item_code_text:
                    item_code = item_code_text.split('Item code:')[-1].strip()

            current_price_tag = item.find('div', class_='currentPrice')
            current_price = current_price_tag.get_text(strip=True) if current_price_tag else 'N/A'

            # Extract carton and single prices
            carton_price = 'N/A'
            single_price = 'N/A'
            price_desc = item.find('div', class_='price-desc')

            if price_desc:
                for col in price_desc.find_all('div', class_='price-col'):
                    value_tag = col.find('div', class_='price')
                    label_tag = col.find('p')
                    price = value_tag.get_text(strip=True) if value_tag else 'N/A'
                    label = label_tag.get_text(strip=True).lower() if label_tag else ''
                    if 'carton' in label:
                        carton_price = price
                    elif 'single' in label:
                        single_price = price

            product_list.append({
                'name': name,
                'image_url': image_url,
                'product_link': product_link,
                'currentPrice': current_price,
                'carton_price': carton_price,
                'single_price': single_price,
                'category': category_name,
                'code': item_code
            })

            Product.objects.update_or_create(
                item_code=item_code,
                defaults={
                    'name': name,
                    'current_price': current_price,
                    'image_url': image_url,
                    'product_link': product_link,
                    'supplier': 'Campbells',
                    'supplier_url': 'https://campbells.sorted.au/'
                }
            )
            # time.sleep(1)

    return product_list

def campbells(reqall_productsuest):
    # all_products = []

    if 'product' in request.GET:
        login_url = 'https://campbells.sorted.au/login'
        username = '33228628'
        password = 'Royal2023$$##!!'

        for category_id, category_name in CATEGORY_MAP_CAMPBELL.items():
            html_pages = get_authenticated_content(login_url, category_id, username, password)
            product_data = extract_product_info(html_pages, category_name)
            all_products.extend(product_data)

    # return render(request, 'core/home.html', {'product_info_list': all_products})



# #need to fix the indentation of the code below-
# # iga
# from django.shortcuts import render
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time

def iga(products):
    products = []
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_IGA = {
  "683": "Half Price Special",
  "696": "Low Price Everyday",
  "540": "Drinks",
  "542": "Frozen Food",
  "543": "Health & Wellbeing",
  "545": "Home & Outdoor",
  "546": "Household Cleaning",
  "548": "Jams & Spreads",
  "550": "Papergoods, Wraps & Bags",
  "551": "Pet care",
  "552": "Toiletries",
  "563": "Bakery",
  "192": "Confectionery",
  "524": "Dairy",
  "525": "Deli & Chilled",
  "526": "Fruit & Vegetables",
  "527": "Meat",
  "529": "Baby",
  "530": "Baking",
  "191": "Groceries",
  "533": "Biscuits & Snacks",
  "534": "Breakfast Foods",
  "535": "Canned & Packet food",
  "537": "Condiments",
  "538": "Cooking, Seasoning & Gravy",
  "539": "Desserts"
    }

    base_url = "https://www.iga.com.au/catalogue/"
    # products = []

    try:
        driver.get(base_url)
        time.sleep(5)

        for cat_id, cat_name in CATEGORY_MAP_IGA.items():
            print(f"\nScraping Category: {cat_name}")
            for page in range(1, 30):
                driver.execute_script(
                    f'window.location.hash = "#view=category&saleId=60288&categoryId={cat_id}&page={page}";'
                )
                time.sleep(3)

                items = driver.find_elements(By.CSS_SELECTOR, "#sf-items-table td.sf-item")
                if not items:
                    print(f"No items on page {page}.")
                    break

                for item in items:
                    try:
                        heading = item.find_element(By.CSS_SELECTOR, "a.sf-item-heading")
                        name = heading.text.strip()
                        link = heading.get_attribute("href")
                        price = item.find_element(
                            By.CSS_SELECTOR, "span.sf-pricedisplay"
                        ).text.strip()
                        img = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                        sku = item.get_attribute("data-itemid") or link.split("/")[-1]

                        products.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "image_url": img,
                            "product_link": link,
                            "category": cat_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': img,
                                'product_link': link,
                                'category': cat_name,
                                'supplier': 'IGA',
                                'supplier_url': 'https://www.iga.com.au'
                            }
                        )
                        time.sleep(0.1)
                    except NoSuchElementException:
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products})

#oliver
# from django.shortcuts import render
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # Optional: from core.models import Product

def oliver(products):
    options = Options()
    # options.add_argument("--headless")  # Uncomment when not debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    base_url = "https://shop.olivers.com.au/collections/all"
    # products = []

    try:
        driver.get(base_url)

        # Wait for grid to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#product-grid .grid__item"))
        )

        # Scroll to load more if needed
        scroll_pause = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get all products
        product_items = driver.find_elements(By.CSS_SELECTOR, "#product-grid .grid__item")
        print(f"Found {len(product_items)} products")

        for item in product_items:
            try:
                # Product name and link
                name_element = item.find_element(By.CSS_SELECTOR, "h3.card-information__text a.full-unstyled-link")
                name = name_element.text.strip()
                link = name_element.get_attribute("href")

                # Image
                img_tag = item.find_element(By.CSS_SELECTOR, "img")
                image_url = img_tag.get_attribute("src") or img_tag.get_attribute("data-src") or ""

                # Price
                price_element = item.find_element(By.CSS_SELECTOR, "span.product_price")
                price = price_element.text.strip()

                # SKU/code from link
                sku = link.rstrip("/").split("/")[-1]

                # Append to list
                products.append({
                    "name": name,
                    "code": sku,
                    "currentPrice": price,
                    "image_url": image_url,
                    "product_link": link,
                    "category": "Snacks"
                })

               
                Product.objects.update_or_create(
                    item_code=sku,
                    defaults={
                        'name': name,
                        'current_price': price,
                        'image_url': image_url,
                        'product_link': link,
                        'category': 'Snacks',
                        'supplier': "Oliver’s",
                        'supplier_url': base_url
                    }
                )
                time.sleep(0.1)

            except Exception as e:
                print("Error extracting product:", e)

        # Save page for debug (optional)
        with open("olivers_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products})



# # mylollies
# from django.shortcuts import render
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time


def mylollies(products):
    # products = []
    options = Options()
    # options.add_argument("--headless")  # Enable for production
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    base_url = "https://mylollies.com.au/chocolate-confectionery/page/{}/"
    # products = []

    try:
        page = 1
        while True:
            url = base_url.format(page)
            driver.get(url)
            print(f"Scraping page {page}: {url}")

            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.products li.product"))
                )
            except Exception:
                print("No products found or last page reached.")
                break

            product_items = driver.find_elements(By.CSS_SELECTOR, "ul.products li.product")
            print(f"Found {len(product_items)} products on page {page}")

            if not product_items:
                break

            for item in product_items:
                try:
                    # Product link
                    link = item.find_element(By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link").get_attribute("href")

                    # Product name
                    name = item.find_element(By.CSS_SELECTOR, "h4.woocommerce-loop-product__title").text.strip()

                    # Image URL
                    img_tag = item.find_element(By.CSS_SELECTOR, "img")
                    image_url = img_tag.get_attribute("src")

                    # Price
                    price = item.find_element(By.CSS_SELECTOR, "span.price").text.strip()

                    # SKU from data-product_id or URL slug
                    sku = item.get_attribute("data-product_id")
                    if not sku:
                        sku = link.rstrip("/").split("/")[-1]

                    products.append({
                        "name": name,
                        "code": sku,
                        "currentPrice": price,
                        "image_url": image_url,
                        "product_link": link,
                        "category": "snacks"
                    })
                    
                    Product.objects.update_or_create(
                        item_code=sku,
                        defaults={
                            'name': name,
                            'current_price': price,
                            'image_url': image_url,
                            'product_link': link,
                            'category': 'snacks',
                            'supplier': "Mylollies",
                            'supplier_url': base_url
                        }
                    )
                    time.sleep(0.1)

                except Exception as e:
                    print("Error extracting product:", e)

            # Check if next page exists (pagination might stop at 404 or no product items)
            page += 1
            time.sleep(2)

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products})





#costco
# from django.shortcuts import render
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time


def costco(products):
    # products = []

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)

    base_url = "https://www.costco.com.au"
    CATEGORY_MAP_COSTCO = [
        "/Appliances/c/cos_2",
        "/Electronics/c/cos_21",
        "/Computers/c/cos_22",
        "/Furniture-Mattresses/c/cos_11",
        "/Tyres-Automotive/c/cos_9",
        "/Health-Beauty/c/cos_8",
        "/Home-Improvement/c/cos_5",
        "/Sports-Fitness/c/cos_6",
        "/Patio-Lawn-Garden/c/cos_4",
        "/Wine-Spirits/c/cos_10",
        "/Baby-Kids-Toys/c/cos_16",
        "/Grocery-Household/c/cos_18",
        "/Gift-Cards-Books-Office-Supplies/c/cos_23",
        "/Home-Kitchen/c/cos_3",
        "/Jewellery-Watches-Sunglasses/c/cos_7",
        "/Clothing-Luggage-Handbags/c/cos_15",
        "/Hampers-Flowers/c/cos_17",
        "/Preorder-Cakes-Platters/c/cos_19",
        "/Business-Delivery/c/cos_30",
    ]

    # products = []

    try:
        for category in CATEGORY_MAP_COSTCO:
            category_url = base_url + category
            driver.get(category_url)

            try:
                WebDriverWait(driver, 20).until(
                    # EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-item"))
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-name a"))
                )
            except Exception as e:
                print(f"Timeout loading: {category_url} — {e}")
                continue

            product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-item")
            time.sleep(10)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(1)
            for item in product_items:
                
                    name_elem = item.find_elements(By.CSS_SELECTOR, "div.item-name a")
                    price_elem = item.find_elements(By.CSS_SELECTOR, "span.product-price-amount span.notranslate")

                    if not name_elem or not price_elem:
                        print("Skipping item due to missing name or price")
                        continue  # Skip this product
                    
                    name = item.find_element(By.CSS_SELECTOR, "div.item-name a").text.strip()
                    link = item.find_element(By.CSS_SELECTOR, "div.item-name a").get_attribute("href")
                    price = item.find_element(By.CSS_SELECTOR, "span.product-price-amount span.notranslate").text.strip()
                    image_url = item.find_element(By.CSS_SELECTOR, "div.thumb img").get_attribute("src")
                    sku = link.rstrip("/").split("/")[-1]
                    category_name = category.split("/")[-1].replace("-", " ").title()

                    products.append({
                        "name": name,
                        "code": sku,
                        "currentPrice": price,
                        "image_url": image_url,
                        "product_link": link,
                        "category": category_name
                    })

                    Product.objects.update_or_create(
                        item_code=sku,
                        defaults={
                            'name': name,
                            'current_price': price,
                            'image_url': image_url,
                            'product_link': link,
                            'category': category_name,
                            'supplier': "Costco",
                            'supplier_url': base_url
                        }
                    )

                    time.sleep(0.1)
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, ".owl-next")
                        if "disabled" in next_button.get_attribute("class"):
                            break
                        ActionChains(driver).move_to_element(next_button).click().perform()
                        time.sleep(1.2)  # Wait for new items to load
                    except:
                        break

    finally:
        driver.quit()
    # return render(request, 'core/home.html', {'product_info_list': products})

# from django.shortcuts import render
# from core.models import Product
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

def nippys(products):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    base_url = "https://nippys.com.au/site/shop-online/"
    # products = []

    try:
        driver.get(base_url)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.products.columns-3 li.product"))
        )

        items = driver.find_elements(By.CSS_SELECTOR, "ul.products.columns-3 li.product")

        for item in items:
            try:
                link_elem = item.find_element(By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link")
                link = link_elem.get_attribute("href")

                name = item.find_element(By.CSS_SELECTOR, "h2.woocommerce-loop-product__title").text.strip()

                image = item.find_element(By.CSS_SELECTOR, "img.attachment-woocommerce_thumbnail")
                image_url = image.get_attribute("src")

                price_elem = item.find_element(By.CSS_SELECTOR, "span.price")
                price = price_elem.text.strip()

                # Generate fallback code from product name
                code = name.lower().replace("'", "").replace(" ", "-")

                products.append({
                    "name": name,
                    "code": code,
                    "currentPrice": price,
                    "image_url": image_url,
                    "product_link": link,
                    "category": ""
                })
                
                Product.objects.update_or_create(
                    item_code=code,
                    defaults={
                        'name': name,
                        'current_price': price,
                        'image_url': image_url,
                        'product_link': link,
                        'category': '',
                        'supplier': "Nippys",
                        'supplier_url': base_url
                    }
                )
                time.sleep(0.1)

            except Exception as e:
                print("Error parsing product:", e)

    except Exception as e:
        print("Timeout loading:", base_url, "— Message:", e)

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products})


#atwork.woolworths
# from django.shortcuts import render
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

CATEGORY_MAP_ATWORK = {
    "fresh": "Fresh",
    "fridge": "Fridge",
    "pantry": "Pantry",
    "breakfast-bakery": "Breakfast bakery",
}


def slow_scroll(driver, times=10, delay=2):
    """Scrolls slowly to load all content."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def login_to_woolworths(driver, login_url, username, password):
    driver.get(login_url)
    wait = WebDriverWait(driver, 20)
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = driver.find_element(By.ID, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(60)  # Wait for redirection manually


def extract_products(driver, category_name):
    from core.models import Product
    product_list = []

    tiles = driver.find_elements(By.CSS_SELECTOR, "shared-product-tile")
    for tile in tiles:
        try:
            wc_tile = tile.find_element(By.CSS_SELECTOR, "wc-product-tile")
            shadow_root = driver.execute_script("return arguments[0].shadowRoot", wc_tile)

            name = driver.execute_script(
                "return arguments[0].querySelector('h3')?.innerText || 'Unnamed Product';",
                shadow_root
            )

            img_url = driver.execute_script(
                "return arguments[0].querySelector('img')?.src || '';",
                shadow_root
            )

            price = driver.execute_script(
                "return arguments[0].querySelector('.price')?.innerText || 'N/A';",
                shadow_root
            )

            item_code = name.lower().replace(" ", "-").replace("'", "")

            product_list.append({
                'name': name,
                'image_url': img_url,
                'current_price': price,
                'category': category_name,
                'code': item_code,
            })

            # Uncomment to save to DB:
            Product.objects.update_or_create(
                item_code=item_code,
                defaults={
                    'name': name,
                    'current_price': price,
                    'image_url': img_url,
                    'product_link': '',
                    'supplier': 'Woolworths At Work',
                    'supplier_url': 'https://atwork.woolworths.com.au/',
                }
            )
            time.sleep(0.1)

        except Exception as e:
            print(f"[ERROR] Product extraction failed: {e}")
            continue

    return product_list


def atwork(all_products):
    # all_products = []
    if 'product' in request.GET:
        login_url = 'https://auth-atwork.woolworths.com.au/u/login'
        username = 'info@royalvending.com.au'
        password = 'Royal2020$$'

        # Launch Chrome with current user profile to keep session
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        # options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        # options.add_argument("--user-data-dir=/Users/johnpaultapuyo/Library/Application Support/Google/Chrome")

        # options.add_argument("--user-data-dir=/Users/johnpaultapuyo/Library/Application Support/Google/Chrome")  # macOS
        options.add_argument("--profile-directory=Default")  # or your Chrome profile name

        driver = webdriver.Chrome(options=options)

        try:
            login_to_woolworths(driver, login_url, username, password)

            for category_id, category_name in CATEGORY_MAP_ATWORK.items():
                for page_num in range(1, 6):  # up to 5 pages per category
                    url = f"https://atwork.woolworths.com.au/shop/browse/{category_id}?pageNumber={page_num}"
                    driver.execute_script("window.open(arguments[0], '_blank');", url)
                    driver.switch_to.window(driver.window_handles[-1])
                    try:
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "shared-product-tile"))
                        )
                        slow_scroll(driver, times=12, delay=1.5)
                        products = extract_products(driver, category_name)
                        all_products.extend(products)
                        print(f"[SUCCESS] {category_id} - page {page_num} with {len(products)} products")
                    except Exception as e:
                        print(f"[SKIP] No content on category {category_id} page {page_num}: {e}")
                        break
                    finally:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

        finally:
            driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': all_products})




CATEGORY_MAP_DISTRIBUTOR = {
    "AMERICAN+LINES": "AMERICAN LINES",
    "ARNOTTS": "ARNOTTS",
    "BEVERAGES+%25252F+DRINKS": "BEVERAGES / DRINKS",
    "BISCUITS": "BISCUITS",
    "BISCUITS+-+SNACK+SIZE": "BISCUITS - SNACK SIZE",
    "CEREAL+%25252F+SNACKS+ETC": "CEREAL / SNACKS ETC",
    "CHILLED": "CHILLED",
    "CHIPS%25252FSNACKS+-+OTHER": "CHIPS/SNACKS - OTHER",
    "CHOCOLATE+-+BULK": "CHOCOLATE - BULK",
    "CLEANING": "CLEANING",
    "CONFECTIONERY": "CONFECTIONERY",
    "DRINKS": "DRINKS",
    "FOOD+SERVICE": "FOOD SERVICE",
    "GENERAL+FOOD+LINES": "GENERAL FOOD LINES",
    "GROCERY": "GROCERY",
    "HEALTH+%25252F+BEAUTY+%25252F+HYGENE": "HEALTH / BEAUTY / HYGENE",
    "HEALTHY+SNACK": "HEALTHY SNACK",
    "ICE+CONFECTIONERY": "ICE CONFECTIONERY",
    "OTHER": "OTHER",
    "PACKAGING": "PACKAGING",
    "PARTY": "PARTY",
    "PET+LINES": "PET LINES",
    "SALTY+SNACKS": "SALTY SNACKS",
    "SMOKING": "SMOKING",
    "SUGAR+-+COUNT+LINES": "SUGAR - COUNT LINES",
    "SUGAR+-+SELF+LINES": "SUGAR - SELF LINES",
    "TOP+SELLERS": "TOP SELLERS",
    "UNITED+PETROLEUM+RANGE": "UNITED PETROLEUM RANGE",
    "USA+LINES": "USA LINES",
}

def get_authenticated_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.thedistributorsbrisbane.com.au/Login")
    wait.until(EC.presence_of_element_located((By.ID, "ctl05_UsernameTextBox"))).send_keys("accounts@royalvending.com.au")
    password_input = wait.until(EC.presence_of_element_located((By.ID, "ctl05_PasswordTextBox")))
    password_input.send_keys("Royal2023$$##!!")
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)

    return driver

def slow_scroll(driver, times=5, delay=2):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(delay)

def get_category_pages(driver, category_id, max_pages=100):
    pages_source = []
    for page in range(1, max_pages + 1):
        url = f"https://www.thedistributorsbrisbane.com.au/shop/{category_id}?%24Page={page}"
        driver.get(url)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid-4-3-2.loadMore div.single-product"))
            )
        except:
            print(f"[SKIP] No content on category {category_id} page {page}")
            break

        slow_scroll(driver, times=10, delay=2)
        print(f"[SCRAPE] Category: {category_id}, Page: {page}")
        pages_source.append(driver.page_source)

    return pages_source

def extract_product_info(pages_html, category_name):
    products = []
    for html in pages_html:
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.select('div.single-product')

        for item in items:
            # print(item)
            # Extract name from the <a class="title"> but only the main text (excluding children like <span>)
            title_tag = item.select_one("a.title")
            if not title_tag:
                continue

            # Get only the direct string content (exclude SKU and others)
            title = ""
            for content in title_tag.contents:
                if isinstance(content, str):
                    title += content.strip()
            print(title)
            # SKU
            sku_tag = item.select_one("span.sku")
            sku = sku_tag.get_text(strip=True).replace('- SKU', '') if sku_tag else ""

            # Image
            image_tag = item.select_one("a.product-img img")
            image = image_tag['src'] if image_tag else ""

            # Price (prefer discounted, fallback to no-discount)
            price_tag = item.select_one('span[name="UnitPriceDiscount"]')
            if not price_tag or not price_tag.get_text(strip=True):
                price_tag = item.select_one('span[name="UnitPriceNoDiscount"]')
            price = price_tag.get_text(strip=True).replace('$', '') if price_tag else ""
   
            
            href = title_tag.get('href', '')
            product_link = f"https://www.thedistributorsbrisbane.com.au/product/{href}" if href else ""
            
            products.append({
                "name": title,
                "code": sku,
                "currentPrice": price,
                "image_url": f"https://www.thedistributorsbrisbane.com.au{image}",
                "product_link": product_link,
                "category": category_name
            })
                
            Product.objects.update_or_create(
                item_code=sku,
                defaults={
                    'name': title,
                    'current_price': price,
                    'image_url': f"https://www.thedistributorsbrisbane.com.au{image}",
                    'product_link': product_link,
                    'category': category_name,
                    'supplier': "The Distributors Brisbane",
                    'supplier_url': "https://www.thedistributorsbrisbane.com.au"
                }
            )
            time.sleep(0.1)

    return products

def thedistributorsbrisbane(product_info_list):
    # product_info_list = []

    # if 'product' in request.GET:
    driver = get_authenticated_driver()
    try:
        for category_id, category_name in CATEGORY_MAP_DISTRIBUTOR.items():
            pages = get_category_pages(driver, category_id)
            products = extract_product_info(pages, category_name)
            product_info_list.extend(products)
    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': product_info_list})


# coffscordials
def coffscordials(products_data):
    # products_data = []

    # Set up Chrome driver
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Category paths
    CATEGORY_LIST = [
        "specials",
        "new-lines",
        "category/food-services",
        "category/confectionery",
        "category/cold-beverages",
        "category/snack-foods",
        "category/coffee-tea",
        "category/packaging",
        "category/household-needs"
    ]

    base_url = "https://www.coffscordials.com.au"

    try:
        for category_path in CATEGORY_LIST:
            category_name = category_path.split("/")[-1].replace("-", " ").title()
            print(f"\n=== Scraping Category: {category_name} ===")

            for page in range(1, 110):  # Loop pages 1–8
                page_url = f"{base_url}/{category_path}?page={page}"
                print(f"Fetching: {page_url}")

                try:
                    driver.get(page_url)

                    # Wait for product cards to load
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".category-product.elevation-4"))
                    )
                    
                    product_cards = driver.find_elements(By.CSS_SELECTOR, ".category-product.elevation-4")

                    if not product_cards:
                        print(f"No products on page {page}, skipping.")
                        continue
                    
                    

                    for card in product_cards:
                        try:
                            # Name + size
                            name = card.find_element(By.CSS_SELECTOR, ".product-desc-name").text.strip()
                            size = card.find_element(By.CSS_SELECTOR, ".product-desc-size").text.strip()
                            full_name = f"{name} {size}"

                            # Link & image
                            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            image_src = card.find_element(By.CSS_SELECTOR, ".product-image img").get_attribute("src")
                            image_url = base_url + image_src if image_src.startswith("/") else image_src

                            # Price handling (fallbacks)
                            try:
                                carton_price = (
                                    card.find_element(By.CSS_SELECTOR, ".product-price-special").text.strip()
                                    if card.find_elements(By.CSS_SELECTOR, ".product-price-special")
                                    else card.find_element(By.CSS_SELECTOR, ".product-price-current").text.strip()
                                )
                            except NoSuchElementException:
                                carton_price = "N/A"

                            try:
                                single_price = (
                                    card.find_element(By.CSS_SELECTOR, ".product-price-specialcurrent").text.strip()
                                    if card.find_elements(By.CSS_SELECTOR, ".product-price-specialcurrent")
                                    else ""
                                )
                            except NoSuchElementException:
                                single_price = ""

                            # Extract SKU from URL
                            sku = link.split("/")[-1].split("?")[0] if link else "N/A"

                            # Add to results list
                            products_data.append({
                                "name": full_name,
                                "code": sku,
                                "currentPrice": carton_price,
                                "single_price": single_price,
                                "carton_price": carton_price,
                                "image_url": image_url,
                                "product_link": link,
                                "category": category_name
                            })

                            # Save to DB
                            Product.objects.update_or_create(
                                item_code=sku,
                                defaults={
                                    'name': full_name,
                                    'current_price': carton_price,
                                    'image_url': image_url,
                                    'product_link': link,
                                    'category': category_name,
                                    'supplier': "Coffs Cordials",
                                    'supplier_url': base_url
                                }
                            )

                            time.sleep(0.1)  # Light throttle

                        except Exception as e:
                            print(f"Error parsing product: {e}")
                            continue

                except TimeoutException:
                    print(f"Timeout loading products for {category_name} on page {page}, skipping.")
                    continue

                except Exception as e:
                    print(f"Unexpected error on page {page} of {category_name}: {e}")
                    continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})
# harcher
def harcher(products_data):
    # products_data = []
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless scraping
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_HARCHER = [
        "Beverages",
        "Chocolate",
        "Grocery",
        "Gum+%26+Mints",
        "Health+%26+Beauty",
        "Lollies",
        "Novelty",
        "Snacks",
        "Top+Sellers"
    ]

    base_url = "https://www.harcher.com.au/shopd"
   
    try:
        for cat in CATEGORY_MAP_HARCHER:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.harcher.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.harcher.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })
                        
                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Harcher',
                                'supplier_url': 'https://www.harcher.com.au/'
                            }
                        )
                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})





#new
# thedistributorscentralcoast
def thedistributorscentralcoast(products_data):
    products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_TDCC = [
        "AMERICAN+LINES",
        "BEVERAGES",
        "BISCUITS",
        "CADBURY+CONFECTIONERY",
        "CONFECTIONERY",
        "FOOD+SERVICE",
        "GROCERY",
        "HEALTHY+SNACK",
        "LOLLY+BAR",
        "NOVELTIES",
        "PACKAGING",
        "PARTY",
        "PHONE+ACCESSORIES",
        "SALTY+SNACKS",
        "SCHOOL+LINES",
        "SMOKING",
        "TOP+SELLERS",
    ]

    base_url = "https://www.thedistributorscentralcoast.com.au/shop"

    try:
        for cat in CATEGORY_MAP_TDCC:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # limit to max 50 pages
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.thedistributorscentralcoast.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.thedistributorscentralcoast.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Harcher',
                                'supplier_url': 'https://www.thedistributorscentralcoast.com.au/'
                            }
                        )
                        
                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


def thedistributorsbathurst(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_TDBATHURST = [
        "ACCOMODATION",
        "ASSORTMENTS",
        "BAGS",
        "BARS",
        "BEVERAGES",
        "BISCUITS",
        "BULK",
        "CARTONS+%26+TUBS",
        "CHEMICALS",
        "CHILDRENS+LINES",
        "COFFEE",
        "CONFECTIONERY",
        "COUNT+LINES",
        "DARRELL+LEA",
        "DISPENERS",
        "DRINKS",
        "EXCLUDED+FROM+FORMS",
        "EXCLUSIVE",
        "FOOD+SERVICE",
        "GROCERY",
        "GUM+LINES",
        "HAND+CARE",
        "HEALTHY+SNACK",
        "HEALTHY+SNACKS",
        "HOSPITALITY%25252FBAR",
        "JANITORIAL",
        "KITCHEN",
        "LOLLY+BAR",
        "MACHINERY",
        "MOBILE+ACCESSORIES",
        "MOULDED+CHOCOLATE",
        "NOVELTIES",
        "PACKAGING",
        "PAPER",
        "PARTY",
        "PHARMACEUTICAL",
        "ROLLS+-+STICKS+-+PACKETS",
        "SAFETY",
        "SALTY+SNACKS",
        "SMOKING",
        "SNACK+FOODS",
        "TOBACCO+PRODUCTS",
        "TOP+SELLERS",
    ]

    base_url = "https://www.thedistributorsbathurst.com.au/shop"

    try:
        for cat in CATEGORY_MAP_TDBATHURST:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # limit to max 50 pages
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.thedistributorsbathurst.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.thedistributorsbathurst.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'The Distributors Bathurst',
                                'supplier_url': 'https://www.thedistributorsbathurst.com.au/'
                            }
                        )
                        
                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})



# inlanddistributors doesnt have price yet
def inlanddistributors(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment if you don't want to see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_URLS_INLAND = [
        "https://www.inlanddistributors.com.au/shop/BEVERAGE?%24Page=1",
        "https://www.inlanddistributors.com.au/shop/CHEMICALS?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/CLEANING?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/COFFEE+%26+CAFE+SUPPLIES?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/COFFEE+EQUIPMENT?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/CONFECTIONERY?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/DRY+GOODS?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/GROCERY?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/HEALTHY+SNACKS?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/ICED+TEA?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/ISOTONIC+SPORTS+%26+FUNCTIONAL?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/JASOL?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/JUICE?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/KOMBUCHA?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/PACKAGING+PRODUCTS?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/PHONE+ACCESSORIES?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/PORTION+CONTROL?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/SALTY+SNACKS+%26+SALSA?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/SMOKING?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/SPARKLING+WATER?%24Mode=Grid",
        "https://www.inlanddistributors.com.au/shop/WATER?%24Mode=Grid",
    ]

    try:
        for category_url in CATEGORY_URLS_INLAND:
            category_name = urllib.parse.unquote(category_url.split("/shop/")[1].split("?")[0]).replace("+", " ")
            print(f"\n=== Category: {category_name} ===")

            for page in range(1, 50):  # Limit to 8 pages per category
                # Replace $Page if exists, otherwise append
                if "%24Page=" in category_url:
                    page_url = re.sub(r'%24Page=\d+', f'%24Page={page}', category_url)
                else:
                    join_char = "&" if "?" in category_url else "?"
                    page_url = f"{category_url}{join_char}%24Page={page}"

                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No products found for {category_name} page {page}, stopping.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.inlanddistributors.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.inlanddistributors.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Inland Distributors',
                                'supplier_url': 'https://www.inlanddistributors.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})



# thedistributorscentralcoast
def thedistributorscentralcoast(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_TDCC = [
        "AMERICAN+LINES",
        "BEVERAGES",
        "BISCUITS",
        "CADBURY+CONFECTIONERY",
        "CONFECTIONERY",
        "FOOD+SERVICE",
        "GROCERY",
        "HEALTHY+SNACK",
        "LOLLY+BAR",
        "NOVELTIES",
        "PACKAGING",
        "PARTY",
        "PHONE+ACCESSORIES",
        "SALTY+SNACKS",
        "SCHOOL+LINES",
        "SMOKING",
        "TOP+SELLERS",
    ]

    base_url = "https://www.thedistributorscentralcoast.com.au/shop"

    try:
        for cat in CATEGORY_MAP_TDCC:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # adjust here if you want fewer pages
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.thedistributorscentralcoast.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.thedistributorscentralcoast.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'The Distributors Central Coast',
                                'supplier_url': 'https://www.thedistributorscentralcoast.com.au/'
                            }
                        )
                        
                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})

# saxbysdrury scraper
def saxbysdrury(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_SAXBYS = [
        "BAGS",
        "BEVERAGES",
        "BISCUITS",
        "CARBONATED+SOFT+DRINKS",
        "CATERING",
        "CATERING+MISC",
        "CHEMICALS",
        "CHIPS",
        "CHIPS+%26+SNACKS",
        "CHOC+EASTER",
        "CHOCOLATE+BARS",
        "CHOCOLATE+BLOCK",
        "CHOCOLATE+BOXED",
        "CLEANING",
        "CLEANING+SUPPLIES",
        "COFFEE+-+CAFE",
        "CONFEC",
        "CONFECTIONERY",
        "COOKING",
        "CUPS%25252FLIDS%25252FSTRAWS",
        "EG+BEVERAGES",
        "EG+GROCERY",
        "GAS",
        "GROCERY",
        "GUM",
        "HEALTH%26BEAUTY",
        "HOSPITALITY+%26+ACCOMMODATION",
        "MILK+%26+SOY+DRINKS",
        "PACKAGING",
        "POST+MIX%25252FSLUSH+MIX",
        "SNACKS+GENERAL",
        "SPORTS+DRINKS",
        "TABLEWARE",
        "TOP+SELLERS",
        "TRADESHOW+CONFECT",
        "TRADESHOW+DRINKS",
    ]

    base_url = "https://www.saxbysdrury.com/shop"

    try:
        for cat in CATEGORY_MAP_SAXBYS:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # Adjust if you want fewer pages
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.saxbysdrury.com" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.saxbysdrury.com" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Saxbys Drury',
                                'supplier_url': 'https://www.saxbysdrury.com/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


# beachandbush scraper
def beachandbush(products_data):
    products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_BNB = [
        "BEVERAGE",
        "BEVERAGES",
        "BISCUITS",
        "CATERING+LINES",
        "CHEMICALS",
        "CHEMICALS+BULK",
        "CHIPS+SUNDRY",
        "CHIPS%25252FSNACKS+-+OTHER",
        "CHOCOLATE+-+ASSORTMENTS",
        "CHOCOLATE+-+BARS",
        "CHOCOLATE+-+BULK",
        "CHOCOLATE+-+C+PACKS",
        "CHOCOLATE+-+COUNT+LINES",
        "CHOCOLATE+-+MOULDED",
        "CHOCOLATE+-+SEASONAL",
        "CHOCOLATE+-+SELF+LINES",
        "COFFEE+COMMERCIAL",
        "COFFEE+PRODUCT",
        "CONFECTIONERY",
        "Default",
        "DISPOSABLE",
        "EXCLUSIVE",
        "FOOD+SERVICE",
        "GROCERY",
        "HEALTH+%25252F+MUESLI+BAR+LINES",
        "HEALTHY+SNACK",
        "KENMAN",
        "KETTLE+CHIPS",
        "MISC+SNACK+FOODS",
        "PACKAGING",
        "PARTY",
        "PHARMACY",
        "POS+%26+STANDS",
        "PRINGLES",
        "S%25252EB%25252EA+CC%27S",
        "S%25252EB%25252EA%25252E+THINS",
        "SALTY+SNACKS",
        "SBA+NATURAL+CHIP+CO",
        "SMITHS+CHIPS",
        "SMOKING",
        "SUGAR+-+BAGS",
        "SUGAR+-+BULK",
        "SUGAR+-+COUNT+LINES",
        "SUGAR+-+NOVELTY",
        "SUGAR+-+SEASONAL",
        "SUGAR+-+SELF+LINES",
        "SUGAR+-+SINGLE%25252FSTICK+PK",
        "SUNDRY+GENERAL+PRODUCTS",
        "TELECOMMUNICATIONS",
        "TOP+SELLERS",
        "USA+IMPORTS"
    ]

    base_url = "https://www.beachandbush.net.au/shop"

    try:
        for cat in CATEGORY_MAP_BNB:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # You can lower if needed
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.beachandbush.net.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.beachandbush.net.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Beach and Bush',
                                'supplier_url': 'https://www.beachandbush.net.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


# Sweeties Confectionery scraper need account price are hiddern
def sweetiesconfectionery(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_SWEETIES = [
        "BEVERAGES",
        "BISCUITS",
        "Chips%25252FSnacks",
        "CONFECTIONERY",
        "GROCERY",
        "PACKAGING",
        "Protein%25252FHealth",
        "Usa+Products"
    ]

    base_url = "https://www.sweetiesconfectionery.com.au/shop"

    try:
        for cat in CATEGORY_MAP_SWEETIES:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # adjust page range as needed
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.sweetiesconfectionery.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.sweetiesconfectionery.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Sweeties Confectionery',
                                'supplier_url': 'https://www.sweetiesconfectionery.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})

# The Distributors Cairns scraper
# thedistributorscairns
def thedistributorscairns(products_data):
    products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_CAIRNS = [
        "BEVERAGES",
        "BISCUITS",
        "CONFECTIONERY",
        "EXCLUSIVE",
        "FOOD+SERVICE",
        "GROCERY",
        "HEALTHY+SNACK",
        "PACKAGING",
        "PARTY",
        "SALTY+SNACKS",
        "SMOKING",
        "TOP+SELLERS"
    ]

    base_url = "https://www.thedistributorscairns.com.au/shop"

    try:
        for cat in CATEGORY_MAP_CAIRNS:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # Adjust if you want fewer pages
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.thedistributorscairns.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.thedistributorscairns.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'The Distributors Cairns',
                                'supplier_url': 'https://www.thedistributorscairns.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})
    
    
    
# thedistributorsmackay
def thedistributorsmackay(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_MACKAY = [
        "BEVERAGES",
        "BISCUITS",
        "CHILLED",
        "COFFEE+ICED",
        "CONFECTIONERY",
        "DEFAULT",
        "ENERGY",
        "ENERGY+SUGAR",
        "ENERGY+SUGAR+FREE",
        "FOOD+SERVICE",
        "FRUIT+DRINKS",
        "GROCERY",
        "GUM",
        "HEALTHY+SNACK",
        "MILK",
        "NONFOOD",
        "PACKAGING",
        "PARTY",
        "SALTY+SNACKS",
        "SMOKING",
        "SNACKS",
        "SOFT+DRINKS",
        "SOFT+DRINKS+SUGAR",
        "SOFT+DRINKS+SUGAR+FREE",
        "TEA",
        "TEA+ICED",
        "TOP+SELLERS",
        "WATER",
        "WATER+SPORTS",
        "WATER+SUGAR",
    ]

    base_url = "https://www.thedistributorsmackay.com.au/shop"

    try:
        for cat in CATEGORY_MAP_MACKAY:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # Limit pages as needed
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.thedistributorsmackay.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.thedistributorsmackay.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'The Distributors Mackay',
                                'supplier_url': 'https://www.thedistributorsmackay.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


# acwsunshine scraper
def acwsunshine(products_data):
    products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_ACW = [
        "BEVERAGES",
        "BISCUITS",
        "CHOCOLATE+-+BULK",
        "CONFECTIONERY",
        "DRINKS",
        "EXCLUSIVE",
        "FOOD+SERVICE",
        "GROCERY",
        "HEALTHY+SNACK",
        "PACKAGING",
        "PARTY",
        "PHARMACY",
        "SALTY+SNACKS",
        "SMOKING",
        "SUGAR+-+BAGS",
        "SUGAR+-+BULK",
        "SUGAR+-+COUNT+LINES",
        "SUGAR+-+NOVELTY",
        "SUGAR+IMPORTS",
        "SUNDRY+GENERAL+PRODUCTS",
        "TOP+SELLERS",
    ]

    base_url = "https://www.acwsunshine.com.au/shop"

    try:
        for cat in CATEGORY_MAP_ACW:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # You can reduce if needed
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.acwsunshine.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.acwsunshine.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'ACW Sunshine',
                                'supplier_url': 'https://www.acwsunshine.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


# thedistributorstoowoomba scraper
def thedistributorstoowoomba(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_TOOWOOMBA = [
        "72+Unknown",
        "BAGS",
        "BARS",
        "BEVERAGES",
        "BISCUITS",
        "BOX+CHOCOLATE%25252FASST",
        "BULK",
        "CHILLED",
        "CHIPS",
        "CLEANING",
        "COCA+COLA",
        "CONFECTIONERY",
        "DAIRY",
        "DRINKS+%26+ICES",
        "ENERGY+DRINKS",
        "EXCLUSIVE",
        "FOOD+SERVICE",
        "FROZEN",
        "FRUCOR+BEVERAGES",
        "FRUIT+DRINKS",
        "GENERAL+FOOD+LINES",
        "GROCERY",
        "HEALTH%25252F+BEAUTY%25252F+HYGENE",
        "HEALTHY+SNACK",
        "HEALTHY+SNACKS+OTHER",
        "MERCHANDISING",
        "MOULDED+CHOCOLATE",
        "NONFOOD",
        "NOVELTIES",
        "NUTS",
        "PACKAGING",
        "PARTY",
        "ROLLS-STICKS",
        "SALTY+SNACKS",
        "SCHWEPPES+390-600ML",
        "SCHWEPPES+CANS",
        "SEASONAL+PRODUCTS",
        "SELF+LINES+PKT%25252FDISP",
        "SMALL+GOODS",
        "SMOKING",
        "SOFT+DRINKS+-+others",
        "STATIONARY",
        "TOP+SELLERS",
    ]

    base_url = "https://www.thedistributorstoowoomba.com.au/shop"

    try:
        for cat in CATEGORY_MAP_TOOWOOMBA:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 100):  # Adjust as needed
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.thedistributorstoowoomba.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.thedistributorstoowoomba.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'The Distributors Toowoomba',
                                'supplier_url': 'https://www.thedistributorstoowoomba.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})



# albury accredited scraper
def alburyaccredited(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_ALBURY = [
        "1%25252E25+LTR",
        "250ML",
        "90G-100G+CHIPS",
        "ASSORTED+DRINKS",
        "ASSORTMENTS",
        "BABY+GOODS",
        "BEVERAGES",
        "BISCUITS",
        "BONUS+STOCK+ONLY",
        "CARTONS+%26+TUBS",
        "CHOC+BARS%25252FROLLS",
        "CHOC+COUNT+LINES",
        "CHOC+NOVELTY",
        "CONFECTIONERY",
        "COUNT+LINES",
        "EXCLUSIVE",
        "FRUIT",
        "GROCERY",
        "GUM",
        "H%25252FSNACK+BARS",
        "H%25252FSNACK+NUTS",
        "HEALTH+%26+BEAUTY",
        "HEALTH+SLICES",
        "ICE+CREAM",
        "JELLY+BELLY",
        "LARGE+BAGS",
        "LIQUID+FOOD+DRINKS",
        "MEDIUM+BAGS",
        "NONFOOD",
        "NOVELTIES",
        "OTHER",
        "PARTY",
        "PHARMACY+MEDICINE",
        "PHARMACY+SKIN",
        "S%25252FF+BAGS",
        "S%25252FF+SEASONAL",
        "SMOKING",
        "SNACKS",
        "SOFT+DRINKS+SUGAR",
        "SUGAR+BAGS",
        "SUGAR+BAR%25252FROL%25252FSTK%25252FPOP",
        "SUGAR+BOXED",
        "SUGAR+NOVELTY",
        "TOP+SELLERS",
        "TROLLI",
        "WAFERS",
        "WATER+PLAIN",
    ]

    base_url = "https://albury.accredited.com.au/shop"

    try:
        for cat in CATEGORY_MAP_ALBURY:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2.loadMore .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://albury.accredited.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://albury.accredited.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Albury Accredited',
                                'supplier_url': 'https://albury.accredited.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})




# bendigo accredited scraper
def bendigo(products_data):
    products_data = []

    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_BENDIGO = [
        "1+LTR+DRINKS",
        "27G-30G+CHIPS",
        "90G-100G+CHIPS",
        "ASSORTED+DRINKS",
        "ASSORTMENTS",
        "BATTERIES+%25252F+FILM",
        "BEVERAGES",
        "BISCUITS",
        "BULK+LINES",
        "CATERING",
        "CEREALS",
        "CHARGES+VARIOUS",
        "CHEEZELS",
        "CHILDRENS+LINES",
        "CHOC+BAGS",
        "CHOC+BULK",
        "CLEANING",
        "CONFECTIONERY",
        "CORN+BAGS",
        "COUNTLINES",
        "CUPS+%26+PLASTIC+CUTLERY",
        "ENERGY+SUGAR",
        "EXCLUSIVE",
        "EXTRUDED",
        "FRUIT",
        "GROCERY",
        "GUM",
        "H%25252FSNACK+BARS",
        "H%25252FSNACK+NUTS",
        "HARTZ",
        "HEALTH+%26+BEAUTY",
        "HEALTH+SLICES",
        "ICE+CREAM",
        "JELLY+BELLY",
        "MEDIUM+BAGS",
        "MEDIUM+BARS",
        "NONFOOD",
        "NOVELTIES",
        "PHARMACY+MEDICINE",
        "PHARMACY+SKIN",
        "POPCORN",
        "S%25252FF+SEASONAL",
        "SMALL+BAGS",
        "SMOKING",
        "SNACK+SIZE",
        "SNACKS",
        "SOFT+DRINKS+SUGAR",
        "STATIONERY",
        "STICKS+%26+BARS",
        "SUGAR+BAGS",
        "SUGAR+BAR%25252FROL%25252FSTK%25252FPOP",
        "TOP+SELLERS",
        "VARIOUS",
        "WATER+SPORTS"
    ]

    base_url = "https://bendigo.accredited.com.au/shop"

    try:
        for cat in CATEGORY_MAP_BENDIGO:
            category_display_name = urllib.parse.unquote(cat.replace("+", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 100):  # up to 50 pages
                page_url = f"{base_url}/{cat}?%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2 .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.split("SKU")[0].strip()

                        try:
                            sku = title_element.find_element(By.CSS_SELECTOR, ".sku").text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = "N/A"

                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://bendigo.accredited.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://bendigo.accredited.com.au" + link

                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Bendigo Accredited',
                                'supplier_url': 'https://bendigo.accredited.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


def geelong(products_data):
    # products_data = []

    # Chrome options
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    # Categories for Geelong Accredited
    CATEGORY_PATHS = [
        "ASSORTED%20DRINKS",
        "ASSORTMENTS",
        "BEVERAGES",
        "BISCUITS",
        "BONUS%20STOCK%20ONLY",
        "CHOC%20BARS%252FROLLS",
        "CHOC%20COUNT%20LINES",
        "CLEANING",
        "CONFECTIONERY",
        "COUNTLINES",
        "ENERGY%20SUGAR",
        "ENERGY%20SUGAR%20FREE",
        "EXCLUSIVE",
        "FOOD%20SERVICE",
        "FRUIT",
        "GROCERY",
        "GUM",
        "H%252FSNACK%20NUTS",
        "H%252FSNACK%20OTHER",
        "HARTZ",
        "ICE%20CREAM",
        "JELLY%20BELLY",
        "MEDIUM%20BARS",
        "NONFOOD",
        "NOVELTIES",
        "OTHER",
        "PARTY",
        "S%252FF%20SEASONAL",
        "SMOKING",
        "SNACKS",
        "SOFT%20DRINKS%20SUGAR",
        "SUGAR%20BAGS",
        "SUGAR%20BULK",
        "SUGAR%20COUNT%20LINES",
        "SUGAR%20NOVELTY",
        "TOP%20SELLERS",
        "TROLLI",
        "VARIOUS",
        "WATER%20PLAIN"
    ]

    BASE_URL = "https://geelong.accredited.com.au/shop/"

    try:
        for cat in CATEGORY_PATHS:
            category_name = urllib.parse.unquote(cat.replace("%20", " "))
            print(f"\n=== Category: {category_name} ===")

            for page in range(1, 9):  # limit to max 8 pages
                url = f"{BASE_URL}{cat}?%24Page={page}"
                print(f"Fetching: {url}")
                driver.get(url)
                time.sleep(2)

                products = driver.find_elements(By.CSS_SELECTOR, ".single-product")
                if not products:
                    print("No more products in this category.")
                    break

                for p in products:
                    name = p.find_element(By.CSS_SELECTOR, "a.title").text.strip()
                    link = p.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                    img = p.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                    price = p.find_element(By.CSS_SELECTOR, ".price").text.strip()

                    sku_raw = (name + link).encode('utf-8')
                    sku = hashlib.md5(sku_raw).hexdigest()[:10].upper()
                    
                    products_data.append({
                        "name": name,
                        "code": sku,  # SKU not shown on listing
                        "currentPrice": price,
                        "single_price": price,
                        "carton_price": "",
                        "image_url": img,
                        "product_link": link,
                        "category": category_name
                    })

                    Product.objects.update_or_create(
                        item_code=sku,
                        defaults={
                            'name': name,
                            'current_price': price,
                            'image_url': img,
                            'product_link': link,
                            'supplier': 'Geelong Accredited',
                            'supplier_url': 'https://geelong.accredited.com.au/'
                        }
                    )

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


# aygee.com.au scraper
def aygee(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_URLS = [
        "AUTOMOTIVE", "BEVERAGES", "BISCUITS", "CHIPS", "CHOC%20OTHER",
        "CLEANING%20PRODUCTS", "COFFEE", "CONFEC%20BAGS", "CONFEC%20OTHER",
        "CONFECTIONERY", "FOOD%20SERVICE", "GROCERIES", "GROCERY", "GUM",
        "GUM%20&%20MINTS", "HEALTH%20FOODS", "HEALTHY%20SNACK", "MISCELLANEOUS",
        "PACKAGING", "SALTY%20SNACKS", "SMOKING", "SPECIAL%20EVENTS", "TOP%20SELLERS"
    ]

    base_url = "https://www.aygee.com.au/shop"

    try:
        for cat in CATEGORY_URLS:
            category_display_name = urllib.parse.unquote(cat)
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # stop earlier if no products
                page_url = f"{base_url}/{cat}?%24Mode=Grid&%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        # Product Name & Link
                        title_element = card.find_element(By.CSS_SELECTOR, ".product-title a")
                        name = title_element.text.strip()
                        link = title_element.get_attribute("href")

                        # Generate SKU based on name + link
                        sku = hashlib.md5((name + link).encode()).hexdigest()[:10].upper()

                        # Product Image
                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                        except NoSuchElementException:
                            image_url = ""

                        # Price
                        try:
                            price = card.find_element(By.CSS_SELECTOR, ".price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": "",
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        # Save or update in DB
                        # Product.objects.update_or_create(
                        #     item_code=sku,
                        #     defaults={
                        #         'name': name,
                        #         'current_price': price,
                        #         'image_url': image_url,
                        #         'product_link': link,
                        #         'supplier': 'Aygee',
                        #         'supplier_url': 'https://www.aygee.com.au/'
                        #     }
                        # )

                        time.sleep(0.05)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})







# sldistributors.com.au scraper
def sldistributors(products_data):
    # products_data = []

    options = Options()
    # options.add_argument("--headless")  # Uncomment to run without opening browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_SLD = [
        "BABY%20PRODUCTS",
        "BEVERAGES",
        "BISCUITS",
        "CLEANING",
        "CLEANING%20VARIOUS",
        "COFFEE",
        "CONFECTIONERY",
        "CORDIALS%20&%20SYRUPS",
        "FOOD%20SERVICE",
        "GROCERY",
        "HEALTHY%20SNACK",
        "NOAHS",
        "NOVELTIES",
        "PACKAGING",
        "PACKAGING%20-%20CONTAINERS",
        "PARTY",
        "SALTY%20SNACKS",
        "SMOKING",
        "TABLEWARES",
        "TOP%20SELLERS"
    ]

    base_url = "https://www.sldistributors.com.au/shop"

    try:
        for cat in CATEGORY_MAP_SLD:
            category_display_name = urllib.parse.unquote(cat)
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # Adjust if you want fewer pages
                page_url = f"{base_url}/{cat}?%24Mode=Grid&%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(2)

                # Product selector based on SLD layout
                product_cards = driver.find_elements(By.CSS_SELECTOR, ".single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        # Product title
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.strip()

                        # SKU
                        try:
                            sku_element = card.find_element(By.CSS_SELECTOR, ".sku")
                            sku = sku_element.text.replace("SKU", "").replace("-", "").strip()
                        except NoSuchElementException:
                            sku = hashlib.md5(name.encode()).hexdigest()[:10].upper()  # fallback SKU

                        # Image
                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                            if image_url.startswith("/"):
                                image_url = "https://www.sldistributors.com.au" + image_url
                        except NoSuchElementException:
                            image_url = ""

                        # Product link
                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.sldistributors.com.au" + link

                        # Prices
                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span[name='UnitPriceNoDiscount'].price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        try:
                            each_price = card.find_element(By.CSS_SELECTOR, "span[name='PerIndividualPriceNoDiscountText'].each").text.strip("()")
                        except NoSuchElementException:
                            each_price = ""

                        # Store product in list
                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "single_price": price,
                            "carton_price": each_price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        # Save to DB
                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'SL Distributors',
                                'supplier_url': 'https://www.sldistributors.com.au/'
                            }
                        )

                        time.sleep(0.1)

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})


def generate_sku(name, link):
    """Generate SKU from name + link hash."""
    raw = f"{name}-{link}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()[:10].upper()

def mcdonaldswholesalers(products_data):
    # products_data = []

    # Chrome options
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_URLS = [
        "BAKING,%20SUGARS,%20NUTS%20&%20FLOUR",
        "BATTERIES,%20TORCH%20&%20STATIONERY",
        "BBQ,%20FIRE%20&%20CAMPING",
        "BEVERAGES",
        "BREAKFAST,%20CEREALS%20&%20MILK%20(LL)",
        "CAKES,%20DESSERTS%20&%20TOPPINGS",
        "CANNED%20MEALS",
        "CHEMICALS%20&%20CLEANING",
        "CHIPS,%20NUTS,%20SNACKS%20&%20BISCUITS",
        "COFFEE,%20TEA%20&%20HOT%20BEVERAGES",
        "CONFECTIONERY",
        "DAIRY,%20EGGS%20&%20CHEESE%20-%20CHILLER",
        "DRINKS,%20JUICES%20&%20BEVERAGES",
        "FROZEN%20-%20CAKES%20&%20DESSERTS",
        "FROZEN%20GOODS",
        "FRUITS%20-%20CANNED%20&%20DRIED",
        "HEALTH,%20BABY%20&%20COSMETIC",
        "HOSPITALITY%20CATERING%20&%20KITCHEN",
        "INTERNATIONAL%20FOODS",
        "LIGHTERS,%20MATCHES%20AND%20FILTERS",
        "OILS",
        "PAPER,%20PACKAGING%20&%20PLASTIC",
        "PASTA,%20RICE%20&%20SOUPS",
        "PET%20FOOD",
        "SAUCES,%20DRESSINGS%20&%20SPREADS",
        "SEAFOOD",
        "SMALL%20GOODS%20&%20MEATS%20-%20CHILLER",
        "SPICES,%20GRAINS%20&%20SEASONINGS",
        "TOILET%20ROLLS,%20TOWELS%20&%20TISSUES",
        "VEGETABLES%20-%20CANNED%20&%20DRIED",
    ]

    base_url = "https://www.mcdonaldswholesalers.com.au/shop"

    try:
        for cat in CATEGORY_URLS:
            category_display_name = urllib.parse.unquote(cat.replace("%20", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # Adjust max page if needed
                page_url = f"{base_url}/{cat}?%24Mode=Grid&%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(10)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2 .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.strip()

                        link = title_element.get_attribute("href")
                        if link.startswith("/"):
                            link = "https://www.mcdonaldswholesalers.com.au" + link

                        # Image
                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                        except NoSuchElementException:
                            image_url = ""

                        # Prices
                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span.price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        # SKU: generate from name+link
                        sku = generate_sku(name, link)

                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'McDonalds Wholesalers',
                                'supplier_url': 'https://www.mcdonaldswholesalers.com.au/'
                            }
                        )

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    # return render(request, 'core/home.html', {'product_info_list': products_data})



USERNAME = "35992"
PASSWORD = "Royal2023$$##!!"

def generate_sku(name, link):
    """Generate SKU from name + link hash."""
    raw = f"{name}-{link}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()[:10].upper()

def dandenong(request):
    products_data = []

    # Chrome options
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_URLS = [
        "BAGS%20OTHER",
        "BEVERAGES",
        "BISCUITS",
        "CHILLER",
        "CHOC%20BAGS",
        "CHOC%20BARS%252FROLLS",
        "CONDIMENTS",
        "CONFECTIONERY",
        "COUNTLINES",
        "CREAM",
        "CREDITS",
        "ENERGY%20SUGAR",
        "EXCLUSIVE",
        "FUNDRAISING",
        "GROCERY",
        "GUM",
        "H%252FSNACK%20NUTS",
        "H%252FSNACK%20OTHER",
        "ICE%20CREAM",
        "MEALS",
        "NONFOOD",
        "NOVELTIES",
        "PACKAGING",
        "PHARMACY%20MEDICINE",
        "SMOKING",
        "SNACKS",
        "SOFT%20DRINKS%20SUGAR",
        "SUGAR%20BAGS",
        "SUGAR%20COUNT%20LINES",
        "SUGAR%20NOVELTY",
        "TEA",
        "TOP%20SELLERS",
        "UNCATEGORISED"
    ]

    base_url = "https://dandenong.accredited.com.au/shop"

    try:
        # === LOGIN ===
        driver.get("https://dandenong.accredited.com.au/login")
        time.sleep(2)  # allow page to load

        driver.find_element(By.NAME, "ctl05$UsernameTextBox").send_keys(USERNAME)
        driver.find_element(By.NAME, "ctl05$PasswordTextBox").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        time.sleep(3)  # wait for login to process

        # === SCRAPE EACH CATEGORY ===
        for cat in CATEGORY_URLS:
            category_display_name = urllib.parse.unquote(cat.replace("%20", " "))
            print(f"\n=== Category: {category_display_name} ===")

            for page in range(1, 50):  # adjust max page if needed
                page_url = f"{base_url}/{cat}?%24Mode=Grid&%24Page={page}"
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(3)  # delay for slow loading

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2 .single-product")
                if not product_cards:
                    print(f"No more products in {category_display_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.strip()
                        link = title_element.get_attribute("href")

                        if link.startswith("/"):
                            link = "https://dandenong.accredited.com.au" + link

                        # Image
                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                        except NoSuchElementException:
                            image_url = ""

                        # Price
                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span.price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        # SKU
                        sku = generate_sku(name, link)

                        # Store in memory
                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_display_name
                        })

                        # Save/update in DB
                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'Accredited Dandenong',
                                'supplier_url': 'https://dandenong.accredited.com.au/'
                            }
                        )

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    return render(request, 'core/home.html', {'product_info_list': products_data})




# ---- CONFIG ----
USERNAME = ""  # Leave empty for now
PASSWORD = ""  # Leave empty for now

BASE_URL = "https://www.thedistributorsmildura.com.au"
CATEGORY_URLS = [
    "https://www.thedistributorsmildura.com.au/shop/V%20DRINKS",
    "https://www.thedistributorsmildura.com.au/shop/100G%20CHIPS",
    "https://www.thedistributorsmildura.com.au/shop/100G%20CHOCOLATES",
    "https://www.thedistributorsmildura.com.au/shop/175G%20CHIPS",
    "https://www.thedistributorsmildura.com.au/shop/250ML",
    "https://www.thedistributorsmildura.com.au/shop/30G%20CHIPS",
    "https://www.thedistributorsmildura.com.au/shop/40G%20&%2045G%20CHIPS",
    "https://www.thedistributorsmildura.com.au/shop/ASSORTED%20DRINKS",
    "https://www.thedistributorsmildura.com.au/shop/ASSORTMENTS",
    "https://www.thedistributorsmildura.com.au/shop/BEVERAGES",
    "https://www.thedistributorsmildura.com.au/shop/BISCUITS",
    "https://www.thedistributorsmildura.com.au/shop/BUBBLEGUM",
    "https://www.thedistributorsmildura.com.au/shop/CHILDRENS%20LINES",
    "https://www.thedistributorsmildura.com.au/shop/CHUPA%20RANGE",
    "https://www.thedistributorsmildura.com.au/shop/CLEANING",
    "https://www.thedistributorsmildura.com.au/shop/CONFECTIONERY",
    "https://www.thedistributorsmildura.com.au/shop/COUNTLINES",
    "https://www.thedistributorsmildura.com.au/shop/EASTER%20LINES",
    "https://www.thedistributorsmildura.com.au/shop/FAMILY%20BLOCKS",
    "https://www.thedistributorsmildura.com.au/shop/GROCERY",
    "https://www.thedistributorsmildura.com.au/shop/GUM%20&%20MINTS",
    "https://www.thedistributorsmildura.com.au/shop/GUM%20(SUGAR)",
    "https://www.thedistributorsmildura.com.au/shop/HEALTH%20&%20BEAUTY",
    "https://www.thedistributorsmildura.com.au/shop/HEALTH%20SLICES",
    "https://www.thedistributorsmildura.com.au/shop/HEALTHY%20SNACK",
    "https://www.thedistributorsmildura.com.au/shop/KETTLE%20CHIPS",
    "https://www.thedistributorsmildura.com.au/shop/LIFESAVERS",
    "https://www.thedistributorsmildura.com.au/shop/MEDIUM%20BAGS",
    "https://www.thedistributorsmildura.com.au/shop/MEDIUM%20BARS",
    "https://www.thedistributorsmildura.com.au/shop/NOVELTIES",
    "https://www.thedistributorsmildura.com.au/shop/PACKAGING",
    "https://www.thedistributorsmildura.com.au/shop/SALTY%20SNACKS",
    "https://www.thedistributorsmildura.com.au/shop/SMALL%20BAGS",
    "https://www.thedistributorsmildura.com.au/shop/SMOKING",
    "https://www.thedistributorsmildura.com.au/shop/STICKS%20&%20BARS",
    "https://www.thedistributorsmildura.com.au/shop/TOP%20SELLERS",
    "https://www.thedistributorsmildura.com.au/shop/VARIOUS",
    "https://www.thedistributorsmildura.com.au/shop/WASHROOM",
    "https://www.thedistributorsmildura.com.au/shop/WONKA",
    "https://www.thedistributorsmildura.com.au/shop/XMAS%20LINES",
]

# ---- SKU Generator ----
def generate_sku(name, link):
    raw = f"{name}-{link}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()[:10].upper()

# ---- Main View ----
def home(request):
    products_data = []

    # Chrome Options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Uncomment for no browser popup
    driver = webdriver.Chrome(options=options)

    try:
        # ---- Try Login ----
        try:
            driver.get(f"{BASE_URL}/login")
            time.sleep(2)

            if USERNAME and PASSWORD:
                driver.find_element(By.NAME, "ctl05$UsernameTextBox").send_keys(USERNAME)
                driver.find_element(By.NAME, "ctl05$PasswordTextBox").send_keys(PASSWORD)
                driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
                time.sleep(3)
                print("Login attempted.")
            else:
                print("No credentials provided. Skipping login.")

        except Exception as e:
            print("Login failed, continuing without login:", e)

        # ---- Loop Through Categories ----
        for cat_url in CATEGORY_URLS:
            category_name = urllib.parse.unquote(cat_url.split("/")[-1])
            print(f"\n=== Category: {category_name} ===")

            for page in range(1, 120):  # Max 8 pages
                if(cat_url == "https://www.thedistributorsmildura.com.au/shop/V%20DRINKS"):
                     page_url = f"https://www.thedistributorsmildura.com.au/shop?%24Mode=Grid&%24Page={page}"
                else:
                     page_url = f"{cat_url}?%24Mode=Grid&%24Page={page}"
                
               
                print(f"Fetching: {page_url}")
                driver.get(page_url)
                time.sleep(3)

                product_cards = driver.find_elements(By.CSS_SELECTOR, ".grid-4-3-2 .single-product")
                if not product_cards:
                    print(f"No more products in {category_name}, stopping at page {page}.")
                    break

                for card in product_cards:
                    try:
                        title_element = card.find_element(By.CSS_SELECTOR, "a.title")
                        name = title_element.text.strip()
                        link = title_element.get_attribute("href")

                        if link.startswith("/"):
                            link = BASE_URL + link

                        # Image
                        try:
                            image_url = card.find_element(By.CSS_SELECTOR, "a.product-img img").get_attribute("src")
                        except NoSuchElementException:
                            image_url = ""

                        # Price
                        try:
                            price = card.find_element(By.CSS_SELECTOR, "span.price").text.strip()
                        except NoSuchElementException:
                            price = "N/A"

                        # SKU
                        sku = generate_sku(name, link)

                        # Save to list
                        products_data.append({
                            "name": name,
                            "code": sku,
                            "currentPrice": price,
                            "image_url": image_url,
                            "product_link": link,
                            "category": category_name
                        })

                        # Save/Update in DB
                        Product.objects.update_or_create(
                            item_code=sku,
                            defaults={
                                'name': name,
                                'current_price': price,
                                'image_url': image_url,
                                'product_link': link,
                                'supplier': 'The Distributors Mildura',
                                'supplier_url': BASE_URL
                            }
                        )

                    except Exception as e:
                        print("Error parsing product:", e)
                        continue

    finally:
        driver.quit()

    return render(request, 'core/home.html', {'product_info_list': products_data})



def home5(request):
    all_products = []
    remedy_list = []
    fitness_list = []
    aldi_list = []
    kellysdistributors_list = []
    harcher_list = []
    campbells_list = []
    iga_list = []
    oliver_list = []
    mylollies_list = []
    costco_list = []
    nippys_list = []
    atwork_list = []
    thedistributorsbrisbane_list = []
    coffscordials_list = []
    
    if 'product' in request.GET:
    # Create threads
        threads = [
            threading.Thread(target=remedydrinks, args=(remedy_list,)),
            threading.Thread(target=fitnessvending, args=(fitness_list,)),
            threading.Thread(target=aldi, args=(aldi_list,)),
            threading.Thread(target=kellysdistributors, args=(kellysdistributors_list,)),
            threading.Thread(target=harcher, args=(harcher_list,)),
            threading.Thread(target=campbells, args=(campbells_list,)),
            threading.Thread(target=iga, args=(iga_list,)),
            threading.Thread(target=oliver, args=(oliver_list,)),
            threading.Thread(target=mylollies, args=(mylollies_list,)),
            threading.Thread(target=costco, args=(costco_list,)),
            threading.Thread(target=nippys, args=(nippys_list,)),
            threading.Thread(target=thedistributorsbrisbane, args=(thedistributorsbrisbane_list,)),
            threading.Thread(target=atwork, args=(atwork_list,)),
            threading.Thread(target=coffscordials, args=(coffscordials_list,))
            
        ]

        # Start all
        for thread in threads:
            thread.start()

        # Wait for all to finish
        for thread in threads:
            thread.join()

        # Combine and render
        all_products = remedy_list + fitness_list  + aldi_list + kellysdistributors_list + harcher_list + campbells_list + iga_list + oliver_list + mylollies_list + costco_list + nippys_list + thedistributorsbrisbane_list + atwork_list + coffscordials_list
        
    return render(request, "core/home.html", {"product_info_list": all_products})