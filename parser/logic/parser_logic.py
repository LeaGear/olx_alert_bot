import hashlib

import httpx
import json
import time

from bs4 import BeautifulSoup
from parser.config import HEADERS


def group_cards_from_url_response(page_info):
    links_ads = []
    soup = BeautifulSoup(page_info, "lxml")

    main_grid = soup.find("div", {"data-testid": "listing-grid"})

    cards = main_grid.find_all("div", {"data-cy": "l-card"}) if main_grid else soup.find_all("div",
                                                                                             {"data-cy": "l-card"})

    for card in cards:
        try:

            title_element = card.find("h6") or card.find("h3") or card.find("h4")
            title = title_element.text.strip() if title_element else "No Name"
            link_element = card.find("a")

            link = link_element["href"] if link_element else "No Link"
            if "promoted" in link:
                continue
            if link.startswith("/"):
                link = f"https://www.olx.ua{link}"

            price_element = card.find(attrs={"data-testid": "ad-price"})
            price = price_element.text.strip() if price_element else "No Price"

            #print(f"Name: {title}\nPrice: {price}\nLink: {link}\n")

            #print("-" * 50)
            links_ads.append({"name": title, "price": price, "link": link})
        except (AttributeError, KeyError, TypeError) as exp:
            print(exp)
            continue

    return links_ads


def parser(data_list_for_parsing):
    parsed_data = []
    for subs in data_list_for_parsing:
        time.sleep(1)
        url = subs.get("url")
        print(f'Parsing - - - {url}')
        response = httpx.get(url, headers=HEADERS)  # Add status log
        #response = httpx.get(url)
        print(f"RESPONSE STATUS - - - - {response.status_code}")
        #print(f"RESPONSE TEXT - - - - {response.text}")
        #with open("saved_file.txt", "w", encoding="utf-8") as file:
        #    file.write(response.text)
        actual_content = group_cards_from_url_response(response.text)
        content_string = json.dumps(actual_content, sort_keys=True, ensure_ascii=False)
        content_hash = hashlib.md5(content_string.encode("utf-8")).hexdigest()

        if content_hash == subs.get("content_hash") and subs.get("content"):
            continue
        else:
            subs["content"] = actual_content
            subs["content_hash"] = content_hash
            parsed_data.append(subs)
        print(f"Parsed data for this url - - - - {subs}")
        print(50 * "-")
    return parsed_data
