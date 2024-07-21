import requests
from bs4 import BeautifulSoup
import json
import shutil
import os
import re

WIKI_ITEMS_URL = "https://bindingofisaacrebirth.fandom.com/wiki/Items"
IMG_PATH = os.path.join(os.path.dirname(__file__), 'images/')
os.makedirs(IMG_PATH, exist_ok=True)

page = requests.get(WIKI_ITEMS_URL)

soup = BeautifulSoup(page.text, 'html.parser')

item_rows = soup.find_all(class_="row-collectible")

items_list = []

with open("items.json", "w") as f:
    for item in item_rows:
        cells = item.find_all("td")
        item_dict = {
            "name": "",
            "id": "",
            "icon": "",
            "quote": "",
            "description": "",
            "quality": ""
        }
        for index, key in enumerate(item_dict.keys()):
            if key in ("name", "id"):
                value = cells[index].attrs.get("data-sort-value")
            elif key == "icon":
                img_cell = cells[index].find("img")
                img_url = img_cell.attrs.get("data-src")
                img_name = img_cell.attrs.get("alt")
                img_name = re.sub(r'[\W\s]', '', img_name) + ".png"
                value = img_name
                r = requests.get(img_url, stream=True)
                img_path = os.path.join(IMG_PATH, img_name)
                with open(img_path, 'wb') as img_file:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, img_file)
            else:
                value = cells[index].get_text()
            clean_text = value.replace("\n", "")
            item_dict[key] = clean_text
        items_list.append(item_dict)

    json_list = json.dumps(items_list)
    f.write(json_list)
        

        