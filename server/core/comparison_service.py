from typing import List

from response_kit import logger


async def get_only_new(data: List[dict]) -> List[dict]:
    result = []
    for obj in data:
        ids_for_notify = set(obj.get("new_content_ids") or [])

        if not ids_for_notify:
            continue

        content = obj.get("content") or []

        temp = [card for card in content if card.get("id") in ids_for_notify]

        if temp:
            result.append(
                {
                    "name": obj.get("name"),
                    "user_id": obj.get("user_id"),
                    "content": temp
                }
            )
    logger.info("Function - <<get_only_new>> in comparison service - Completed")
    return result