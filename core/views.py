
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
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
import threading

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
        print(item)
        id = item.get("id", "")
        name = item.get("title", "Unnamed Product")
        
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
                'code': id
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
                'supplier_url': 'https://www.remedydrinks.com/'
            }
        )
            
            

    # products = Product.objects.all()
    # return render(request, 'core/home.html', {'product_info_list': remedy_list})
    

# # fintessvending.com
# from django.shortcuts import render
# from .models import Product
# import requests

def fetch_fintessvending_products(limit=30, offset=0):
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


def fitnessvending(fitness_list):
    # fitness_list = []
    products_data = fetch_fintessvending_products(limit=30, offset=0)

    for item in products_data:
        print('#####################')
        print(item)
        id = item.get("id", "")
        name = item.get("title", "Unnamed Product")
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
                'code': id
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
                'supplier_url': 'https://www.fitnessvending.com/'
            }
        )
            
            

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


def aldi(product_list):
    products_data = fetch_aldi_products(limit=30, offset=0)
    # product_list = []

    for item in products_data:
        code = item.get("sku", "Unnamed Product")
        name = item.get("name", "Unnamed Product")
        print(item)
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
        
        product_list.append({
                'name': name,
                'image_url': image_url,
                'product_link': product_url,
                'currentPrice': price,
                'carton_price': '0',
                'single_price': '0',
                'category': category,
                'code': code
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
                'supplier_url': 'https://www.aldi.com.au/'
            }
        )

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

def kellysdistributors(products_data):
    options = Options()
    options.add_argument("--headless")  # Uncomment for headless scraping
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    CATEGORY_MAP_KELLY = {
        "alkaline-water": "Alkaline Water",
        "carbonated-drinks": "Carbonated Drinks",
        "alchemy-2": "Alchemy",
        # "arkadia-beverages-2": "Arkadia Beverages",
        # "byron-bay-cookies-2": "Byron Bay Cookies",
        # "edlyn-toppings-2": "Edlyn Toppings",
        # "elixirs-latte-powder-4": "Elixirs Latte Powder",
        # "little-bakes-2": "Little Bakes",
        # "naked-syrups-2": "Naked Syrups",
        # "origin-tea-2": "Origin Tea",
        # "stevia-sugar-2": "Stevia Sugar",
        # "coconut-water": "Coconut Water",
        # "coffee-drinks": "Coffee Drinks",
        # "confectionery": "Confectionery",
        # "energy-drinks": "Energy Drinks",
        # "tradie-energy": "Tradie Energy",
        # "enhanced-water": "Enhanced Water",
        # "flavoured-milks": "Flavoured Milks",
        # "flavoured-water": "Flavoured Water",
        # "grocery-products": "Grocery Products",
        # "health-drinks": "Health Drinks",
        # "iced-tea": "Iced Tea",
        # "juices": "Juices",
        # "coconut-water-smoothies-2": "Coconut Water Smoothies",
        # "fruit-juices-4": "Fruit Juices",
        # "prebiotic-smoothies-2": "Prebiotic Smoothies",
        # "smoothies-2": "Smoothies",
        # "veggie-juices-2": "Veggie Juices",
        # "fruity-burst-2": "Fruity Burst",
        # "lemonades": "Lemonades",
        # "plant-based-milks": "Plant Based Milks",
        # "snacks": "Snacks",
        # "soda": "Soda",
        # "sparkling-coconut-water": "Sparkling Coconut Water",
        # "sports-drinks": "Sports Drinks",
        # "the-raw-treats": "The Raw Treats",
        # "takeaway-packaging": "Takeaway Packaging",
        # "water": "Water"
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

def harcher(products_data):
    options = Options()
    options.add_argument("--headless")  # Uncomment for headless scraping
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
    options.add_argument('--headless')
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
    options = Options()
    options.add_argument("--headless")
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
        time.sleep(5)  # wait for SPA to load

        for cat_id, cat_name in CATEGORY_MAP_IGA.items():
            print(f"\n=== Scraping Category: {cat_name} ===")
            for page in range(1, 30):
                script = f'''
                    window.location.hash = "#view=category&saleId=60288&categoryId={cat_id}&page={page}";
                '''
                driver.execute_script(script)
                time.sleep(5)

                items = driver.find_elements(By.CSS_SELECTOR, ".catalogue-product-tile:not(.placeholder)")
                if not items:
                    print(f"No items on page {page}. Stopping category {cat_name}.")
                    break

                for item in items:
                    try:
                        name = item.find_element(By.CSS_SELECTOR, ".product-title").text
                        price = item.find_element(By.CSS_SELECTOR, ".pricing .price-amount").text
                        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                        sku = item.get_attribute("data-sku") or link.split("/")[-1]
                        img = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

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
    options.add_argument("--headless")  # Uncomment when not debugging
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
    options = Options()
    options.add_argument("--headless")  # Enable for production
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
                            'supplier': "Oliver’s",
                            'supplier_url': base_url
                        }
                    )

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
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

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
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tile"))
                )
            except Exception as e:
                print(f"Timeout loading: {category_url} — {e}")
                with open("costco_timeout_debug.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                continue
            product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-tile")

            for item in product_items:
                try:
                    print(item)
                    name = item.find_element(By.CSS_SELECTOR, ".product-title").text.strip()
                    link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    image_url = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                    price = item.find_element(By.CSS_SELECTOR, ".price").text.strip()
                    sku = link.rstrip("/").split("/")[-1]

                    formatted_category = category.split("/")[1].replace("-", " ").title()

                    products.append({
                        "name": name,
                        "code": sku,
                        "currentPrice": price,
                        "image_url": image_url,
                        "product_link": link,
                        "category": formatted_category
                    })
                    
                    Product.objects.update_or_create(
                        item_code=sku,
                        defaults={
                            'name': name,
                            'current_price': price,
                            'image_url': image_url,
                            'product_link': link,
                            'category': formatted_category,
                            'supplier': "Costco",
                            'supplier_url': base_url
                        }
                    )

                except Exception as e:
                    print("Error extracting product:", e)

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
    options.add_argument("--headless")
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
    options.add_argument('--headless')
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


def home(request):
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
    
    if 'product' in request.GET:
    # Create threads
        threads = [
            threading.Thread(target=remedydrinks, args=(remedy_list,)),
            # threading.Thread(target=fitnessvending, args=(fitness_list,)),
            # threading.Thread(target=aldi, args=(aldi_list,)),
            # threading.Thread(target=kellysdistributors, args=(kellysdistributors_list,)),
            # threading.Thread(target=harcher, args=(harcher_list,)),
            # threading.Thread(target=campbells, args=(campbells_list,)),
            # threading.Thread(target=iga, args=(iga_list,)),
            # threading.Thread(target=oliver, args=(oliver_list,)),
            # threading.Thread(target=mylollies, args=(mylollies_list,)),
            # threading.Thread(target=costco, args=(costco_list,)),
            # threading.Thread(target=nippys, args=(nippys_list,)),
            # threading.Thread(target=thedistributorsbrisbane, args=(thedistributorsbrisbane_list,)),
            # threading.Thread(target=atwork, args=(atwork_list,))
            
        ]

        # Start all
        for thread in threads:
            thread.start()

        # Wait for all to finish
        for thread in threads:
            thread.join()

        # Combine and render
        all_products = remedy_list + fitness_list  + aldi_list + kellysdistributors_list + harcher_list + campbells_list + iga_list + oliver_list + mylollies_list + costco_list + nippys_list + thedistributorsbrisbane_list + atwork_list
        
    return render(request, "core/home.html", {"product_info_list": all_products})