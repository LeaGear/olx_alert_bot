import re
from parser.config import TIME_DIFFERENCE

def fix_olx_server_time(location_time_str: str) -> str:

    match = re.search(r"(\d{2}):(\d{2})", location_time_str)

    if match:
        hours = int(match.group(1))
        minutes = match.group(2)

        kyiv_hours = (hours + TIME_DIFFERENCE) % 24

        new_time = f"{kyiv_hours:02d}:{minutes}"

        return re.sub(r"\d{2}:\d{2}", new_time, location_time_str)

    return location_time_str