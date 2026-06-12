from typing import List


async def get_only_new(data) -> List[dict]:
    result = []
    print(f"NEW DATA DATA DATA DATA !!!!!!!!!!!!!!!!!!!!!!!!!!\n\n{data}\n\n")
    for obj in data:
        temp = []
        print(f"THIS OBJECT NOW WORK====================>>>>>>>>>>>>>>\n{obj}\n\n")
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
