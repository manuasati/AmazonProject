import pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd

# base_url = f"https://www.amazon.in/SHIRT-THEORY-Sleeves-Premium-Stylish/dp/{asin}/ref=sr_1_1_sspa?crid={asin}&keywords=shirts+for+men&qid=1661419896&s=apparel&sprefix=shir%2Capparel%2C260&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyWkNSSENFWUwwRFRVJmVuY3J5cHRlZElkPUEwMTI4NjE1NUlGT1cyTzM0QzBWJmVuY3J5cHRlZEFkSWQ9QTEwNDE0ODkxUzNPQzBFSTVNTkkyJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

feature_list_final = []
"""HEADERS FOR REQUEST TO THE AMAZON"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

"""READING THE EXCEL FILE FOR given_asin"""
data_frame = pandas.read_excel('prod.xlsx')
url_list = data_frame["given_asin"]
print("Hello: ",url_list[5])

"""LOOPING TO ACHIEVE EACH ELEMENT OF given_asin COLUMN TO APPEND WITH THE BASE URL"""
# for url in url_list:
get_url = f"https://www.amazon.in/SHIRT-THEORY-Sleeves-Premium-Stylish/dp/{url_list[5]}/ref=sr_1_1_sspa?crid={url_list[5]}&keywords=shirts+for+men&qid=1661419896&s=apparel&sprefix=shir%2Capparel%2C260&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyWkNSSENFWUwwRFRVJmVuY3J5cHRlZElkPUEwMTI4NjE1NUlGT1cyTzM0QzBWJmVuY3J5cHRlZEFkSWQ9QTEwNDE0ODkxUzNPQzBFSTVNTkkyJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
# SENDING REQUEST TO OUR URL
response = requests.get(get_url, headers=headers)
print(response.status_code)
data = response.text
# CREATING A SOUP
soup = BeautifulSoup(data, "html.parser")

"""SCRAPING TITLE OF PRODUCT"""
product_title = soup.find(name="h1", id="title")
print(f"TITLE : {product_title.getText()}")

# GETTING DETAIL FEATURE DIV
detail_feature_div = soup.find(name="div", id="detailBullets_feature_div")
# GETTING THE LINE IN WHICH DIMENSIONS ARE DEFINED
dimension_list = detail_feature_div.ul.find_all(name="li")[9].span.find_all(name="span")[1].getText().split("x")

"""LENGTH OF PRODUCT"""
length = dimension_list[0]

"""WIDTH OF PRODUCT"""
width = dimension_list[1]

"""HEIGHT OF PRODUCT"""
height = dimension_list[2].strip().split(" ")[0]

"""WEIGHT OF PRODUCT"""
weight = detail_feature_div.ul.find_all(name="li")[8].span.find_all(name="span")[1].getText().split(" ")[0]

"""BRAND OF PRODUCT"""
brand = detail_feature_div.ul.find_all(name="li")[3].span.find_all(name="span")[1].getText().split(" ")[0]

"""MODEL NUMBER OF PRODUCT"""
model_number = detail_feature_div.ul.find_all(name="li")[5].span.find_all(name="span")[1].getText()

"""GENDER OF PRODUCT"""
gender = detail_feature_div.ul.find_all(name="li")[6].span.find_all(name="span")[1].getText()

"""MANUFACTURER OF PRODUCT"""
manufacturer = detail_feature_div.ul.find_all(name="li")[7].span.find_all(name="span")[1].getText()
print(f"LENGTH : {length}")
print(f"WIDTH : {width}")
print(f"HEIGHT : {height}")
print(f"WEIGHT : {weight}")
print(f"BRAND : {brand}")
print(f"MODEL : {model_number}")
print(f"GENDER : {gender}")
print(f"MANUFACTURER : {manufacturer}")

"""DESCRIPTION OF PRODUCT"""
product_description = soup.find(name="p", class_="a-spacing-base")
print(f"DESCRIPTION: {product_description.getText()}")
print("feature_list_final: ***********")
# GETTING LIST ITEM TO SCRAPE FEATURES
feature_ordered_list = soup.find(name="ul", class_="a-unordered-list a-vertical a-spacing-mini")
feature_list = feature_ordered_list.find_all(name="li")

"""SCRAPING FEATURE OF PRODUCT"""
for feature in feature_list:
    feature_text = feature.span.getText()
    feature_list_final.append(feature_text)

print(feature_list_final)
# GETTING MAP LIST ITEMS TO CREATE MAPPING STRING
mapping_ul_list = soup.find(name="ul", class_="a-unordered-list a-horizontal a-size-small").find_all(name="li")
# print(mapping_ul_list)
mapping_string = ""

"""SCRAPING MAPPING OF THE PRODUCT"""
# for map in mapping_ul_list:
#     mapping_string += map.getText().strip() + " "
# print(mapping_string)
for map in mapping_ul_list[::2]:
    mapping_string += map.getText().strip()
print(mapping_string)

"""SCRAPING PICTURE SOURCE OF PRODUCT"""
pic_src = soup.find(name="img", class_="a-dynamic-image a-stretch-horizontal").get("src")
print("hello",pic_src)
