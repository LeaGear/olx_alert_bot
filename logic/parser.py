import httpx
import json
import time

from bs4 import BeautifulSoup
from data.config import HEADERS, QUERY_PARAMS

def save_file(data, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    print("File saved!")

def group_cards_from_url_response(page_info):
    links_ads = []
    soup = BeautifulSoup(page_info, "lxml")

    cards = soup.find_all("div", {"data-cy": "l-card"})
    print(f"Find {len(cards)} cards!")

    main_grid = soup.find("div", {"data-testid": "listing-grid"})

    if main_grid:
        cards = main_grid.find_all("div", {"data-cy": "l-card"})
    else:
        cards = soup.find_all("div", {"data-cy": "l-card"})
    print(f"After filter: {len(cards)} cards")
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

            print(f"Name: {title}\nPrice: {price}\nLink: {link}\n")

            print("-" * 50)
            links_ads.append({"name": title, "price": price, "link": link})
        except Exception as exp:
            print(exp)
            continue

    return links_ads

def parser(user_info):
    for i in user_info:
        url = i["url"]
        if "created_at:desc" not in url:
            if "?" in url:
                url += f"&{QUERY_PARAMS}"
            else:
                url += f"?{QUERY_PARAMS}"

        print(url)
        response = httpx.get(url, headers=HEADERS)

        print("status", response.status_code)

        i["content"] = group_cards_from_url_response(response)
        time.sleep(5)
    return user_info

def main_func_parser():
    #url = "https://www.olx.ua/uk/hobbi-otdyh-i-sport/q-зомбицид/"
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    print(users)
    for user in users:
        print(user)
        user_data = users[user]
        users = parser(user_data)

    save_file(users, "users1.json")
    print(users)

if __name__ == "__main__":
    main_func_parser()