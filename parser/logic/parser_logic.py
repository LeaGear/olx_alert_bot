import httpx
import time

from bs4 import BeautifulSoup
from response_kit import logger

from parser.config import HEADERS
from parser.logic.time_fix import fix_olx_server_time


def group_cards_from_url_response(cards):
    links_ads = []

    for card in cards:
        try:
            photo_url = "No Photo"

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

            location_date = card.find(attrs={"data-testid": "location-date"})
            location = location_date.text.strip() if location_date else "No Location"
            location = fix_olx_server_time(location)

            img_element = card.find("img")
            if img_element:
                srcset = img_element.get("srcset")
                if srcset:
                    photo_url = srcset.split(",")[-1].strip().split(" ")[0]
                else:
                    photo_url = img_element.get("src") or "No Photo"

            links_ads.append(
                {"name": title, "image": photo_url, "location": location, "price": price, "link": link, "id": card_id})
        except (AttributeError, KeyError, TypeError):
            logger.error(f"Error in function - <<group_cards_from_url_response>> - - - - ", exc_info=True)
            continue

    return links_ads


def parser(data_list_for_parsing):
    logger.info("Starting function - <<parser>>")
    try:
        parsed_data = []
        for subs in data_list_for_parsing:
            time.sleep(1)
            url = subs.get("url")
            old_db_ids = subs.get("content_ids")

            try:
                response = httpx.get(url, headers=HEADERS, timeout=15)
                response.raise_for_status()
            except httpx.ReadTimeout:
                logger.error("OLX server timed out - continue")
                continue
            except httpx.HTTPStatusError as e:
                logger.error(f"OLX return code error: {e.response.status_code}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                continue

            if response.status_code != 200:
                logger.warning(f"OLX return status code - >{response.status_code}< for URL: {url}")
                continue

            soup = BeautifulSoup(response.text, "lxml")
            main_grid = soup.find("div", {"data-testid": "listing-grid"})

            if main_grid:
                separator = main_grid.find("div", {"data-cy": "baxter-slot-div-gpt-liting-after-promoted"})
                if separator:
                    cards = separator.find_next_siblings("div", {"data-cy": "l-card"})
                else:
                    cards = main_grid.find_all("div", {"data-cy": "l-card"})
            else:
                cards = soup.find_all("div", {"data-cy": "l-card"})

            new_content_ids = [card.get("id") for card in cards if card.get("id")]
            content_difference = list(set(new_content_ids) - set(old_db_ids))

            actual_content = group_cards_from_url_response(cards)

            if content_difference:
                subs["content"] = actual_content
                subs["content_ids"] = new_content_ids
                subs["new_content_ids"] = content_difference
                parsed_data.append(subs)
            else:
                continue

        logger.info(f"Finished function - <<parser>>")

        return parsed_data

    except Exception as e:
        logger.error(f"Function - <<parser>> not completed with ERROR - {e}", exc_info=True)
