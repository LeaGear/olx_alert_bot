from typing import List


async def find_diff(old:dict, new: dict) -> List[dict]:
    '''print("-----"*30)
    print(f"OLD OLD OLD:\n {old}\n")
    print("-----"*30)

    print(f"NEW NEW NEW:\n {new}\n")
    print("-----"*30)'''

    result = []
    for new_data in new:
        new_data_id = new_data.get("id")
        new_data_user_id = new_data.get("user_id")
        new_data_content = new_data.get("content")

        for old_data in old:
            print(f"{'========' * 20}\n{old_data}\n{'========' * 20}")
            old_data_id = old_data.get("id")
            if old_data_id == new_data_id:
                old_data_content = old_data.get("content")

                '''print("----" * 40)
                print(f"OLD CONTENT \n{old_data_content}")
                print("----" * 40)
                print(f"NEW CONTENT \n{new_data_content}")
                print("----" * 40)'''

                if old_data_content:
                    unique_content = [obj for obj in new_data_content if obj not in old_data_content]
                else:
                    unique_content = new_data_content
                result.append({"user_id": new_data_user_id, "name": new_data.get("name"), "content": unique_content})


    print(f"RESULT RESULT RESULT ------ {result}")
    return result