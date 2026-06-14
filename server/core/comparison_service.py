from typing import List


async def get_only_new(data: List[dict]) -> List[dict]:
    result = []
    for obj in data:
        temp = []
        ids_for_notify = obj.get("new_content_ids")

        for card in obj.get("content"):
            if card.get("id") in ids_for_notify:
                temp.append(card)

        result.append(
            {
                "name": obj.get("name"),
                "user_id": obj.get("user_id"),
                "content": temp
            }
        )

    return result
