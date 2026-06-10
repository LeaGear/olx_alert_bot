from typing import List


async def find_diff(old: dict, new: dict) -> List[dict]:
    a
    result = []
    old_map = {item.get("id"): item.get("content") for item in old}

    for new_data in new:
        new_data_id = new_data.get("id")
        new_data_content = new_data.get("content")
        old_data_content = old_map.get(new_data_id)

        if old_data_content:

            old_set = {obj.get("name") for obj in old_data_content}  # set для быстрого поиска
            unique_content = [obj for obj in new_data_content if obj.get("name") not in old_set]
        else:
            unique_content = new_data_content

        if unique_content:  # добавляем в result только если есть новое
            result.append({
                "user_id": new_data.get("user_id"),
                "name": new_data.get("name"),
                "content": unique_content
            })

    return result
