import httpx
import time

from bs4 import BeautifulSoup
from parser.config import HEADERS


def group_cards_from_url_response(cards):
    links_ads = []

    for card in cards:
        try:
            card_id = card.get("id")

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

            links_ads.append({"name": title, "price": price, "link": link, "id": card_id})
        except (AttributeError, KeyError, TypeError) as exp:
            print(exp)
            continue

    return links_ads


def parser(data_list_for_parsing):
    parsed_data = []
    for subs in data_list_for_parsing:
        time.sleep(1)
        url = subs.get("url")
        old_db_ids = subs.get("content_ids")
        response = httpx.get(url, headers=HEADERS)  # Add status log

        soup = BeautifulSoup(response.text, "lxml")
        main_grid = soup.find("div", {"data-testid": "listing-grid"})
        cards = main_grid.find_all("div", {"data-cy": "l-card"}) if main_grid else soup.find_all("div",
                                                                                                 {"data-cy": "l-card"})
        new_content_ids = [card.get("id") for card in cards]
        content_difference = list(set(new_content_ids) - set(old_db_ids))

        actual_content = group_cards_from_url_response(cards)

        if content_difference:
            subs["content"] = actual_content
            subs["content_ids"] = new_content_ids
            subs["new_content_ids"] = content_difference
            parsed_data.append(subs)
        else:
            continue

    return parsed_data
