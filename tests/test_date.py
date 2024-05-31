import pytz
from datetime import datetime, timezone

startTimestampUTC = "2024-05-30T15:17:20.521Z"
utc_datetime = datetime.strptime(startTimestampUTC, "%Y-%m-%dT%H:%M:%S.%fZ")
# convert utc_datetime to local time
singapore_tz = pytz.timezone("Asia/Singapore")
local_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=singapore_tz)

print(f"{local_datetime.strftime('%Y-%m-%d %H:%M:%S SGT')}")