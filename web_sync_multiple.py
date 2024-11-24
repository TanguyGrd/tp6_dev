import sys
import requests
import time

DL_FILE = "D:\tp6_dev"
argv = sys.argv[1:]

def get_content(url:str):
    print(f"✓ {url}")
    response = requests.get(url)
    return response.text

def write_content(content:str, file:str):
    f = open(file, "w", encoding="utf-8")
    f.write(content)
    f.close()

if len(argv)==0:
    print("Usage: python web_sync_multiple.py <URL's file>")
else:
    urls_file = argv[0]
    with open(urls_file, "r", encoding="utf-8") as file:
        urls = file.readlines()
        for url in urls:
            url = url.split("\n")[0]
            url_formatted = url.split("://")[1]
            html_content = get_content(url)

            urlFile = DL_FILE+url_formatted
            write_content(html_content, urlFile)