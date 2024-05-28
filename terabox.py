import re
from urllib.parse import parse_qs, urlparse
import requests
from tools import get_formatted_size
import aiohttp
import json

def check_url_patterns(url):
    patterns = [
        r"ww\.mirrobox\.com",
        r"www\.nephobox\.com",
        r"freeterabox\.com",
        r"www\.freeterabox\.com",
        r"1024tera\.com",
        r"4funbox\.co",
        r"www\.4funbox\.com",
        r"mirrobox\.com",
        r"nephobox\.com",
        r"terabox\.app",
        r"terabox\.com",
        r"www\.terabox\.ap",
        r"www\.terabox\.com",
        r"www\.1024tera\.co",
        r"www\.momerybox\.com",
        r"teraboxapp\.com",
        r"momerybox\.com",
        r"tibibox\.com",
        r"www\.tibibox\.com",
        r"www\.teraboxapp\.com",
    ]

    for pattern in patterns:
        if re.search(pattern, url):
            return True

    return False

def get_urls_from_string(string: str) -> list[str]:
    pattern = r"(https?://\S+)"
    urls = re.findall(pattern, string)
    urls = [url for url in urls if check_url_patterns(url)]
    if not urls:
        return []
    return urls[0]

def find_between(data: str, first: str, last: str) -> str | None:
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None

def extract_surl_from_url(url: str) -> str | None:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    surl = query_params.get("surl", [])

    if surl:
        return surl[0]
    else:
        return False

async def get_data(url):
    api_url = "https://teraboxdown.com/api/get-data"
    headers = {"Content-Type": "application/json"}
    payload = {"url": url}
    print(f"{payload}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, data=json.dumps(payload)) as response:
                response.raise_for_status()
                data = await response.json()

                if not data:
                    raise ValueError("Unable to get download URL...")

    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None
    except ValueError as e:
        print(e)
        return None

    details = data[0]
    direct_link = details['resolutions']['Fast Download']
    file_name = details['title']
    thumb = details['thumbnail']

    data = {
        "file_name": file_name,
        "direct_link": direct_link,
        "thumb": {thumb}.mp4,
    }
    print(f"{data}")

    return data
