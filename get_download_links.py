import urllib.request
import json
from humanfriendly import format_size

# item token from URL https://figshare.com/s/ee85bb1880921326249b
private_link = "ee85bb1880921326249b"
article_id = 27261219

api_url = (
    f"https://api.figshare.com/v2/articles/{article_id}?private_link={private_link}"
)

# Fetch metadata
req = urllib.request.Request(api_url)
response = urllib.request.urlopen(req)
data = json.loads(response.read().decode("utf-8"))

# Print direct download URLs for each file
for idx, file_info in enumerate(data.get("files", [])):
    print()
    print("-" * 150, idx + 1)
    print(file_info["name"])
    print(file_info["download_url"])
    print(format_size(file_info["size"]))
    print(f"curl -L -C - -o {file_info['name']} {file_info['download_url']}")
