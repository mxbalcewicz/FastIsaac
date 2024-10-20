import json
import os
import re
import shutil

import requests
from bs4 import BeautifulSoup

WIKI_ITEMS_URL = "https://bindingofisaacrebirth.fandom.com/wiki/Items"
ITEMS_PATH = os.path.join(os.path.dirname(__file__), "items/")
ITEM_ID_PREFIX = "5.350."

os.makedirs(ITEMS_PATH, exist_ok=True)


def get_items():
    page = requests.get(WIKI_ITEMS_URL)

    soup = BeautifulSoup(page.text, "html.parser")
    item_rows = soup.find_all(class_="row-collectible")

    items_list = []

    with open("items.json", "w") as f:
        for item in item_rows:
            cells = item.find_all("td")
            item_dict = {
                "name": "",
                "wiki_id": "",
                "icon": "",
                "quote": "",
                "description": "",
                "quality": "",
            }
            for index, key in enumerate(item_dict.keys()):
                if key in ("name", "wiki_id"):
                    value = cells[index].attrs.get("data-sort-value")
                    if key == "wiki_id":
                        value = ITEM_ID_PREFIX + str(value)
                elif key == "icon":
                    img_cell = cells[index].find("img")
                    img_url = img_cell.attrs.get("data-src")
                    img_name = img_cell.attrs.get("alt")
                    img_name = re.sub(r"[\W\s]", "", img_name) + ".png"
                    value = img_name
                    r = requests.get(img_url, stream=True)
                    img_path = os.path.join(ITEMS_PATH, img_name)
                    with open(img_path, "wb") as img_file:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, img_file)
                else:
                    value = cells[index].get_text()
                clean_text = value.replace("\n", "")
                item_dict[key] = clean_text
            items_list.append(item_dict)

        json_list = json.dumps(items_list)
        f.write(json_list)
