import requests
import sys

DL_FILE = "D:\\tp6_dev\\web_page.html"

sys.argv[1:]

def get_content(url:str):
  
  reponse = requests.get(url)
  if reponse.status_code == 200:
    print('c bon')
    return reponse.text
  
  
  
def write(content:str,file:str):
  
  with open (file, "w",encoding="utf-8"):
  
    if len(sys.argv) < 2:
      print("Usage: python web_sync.py <URL>")
    sys.exit(1)

url_request = sys.argv[1]
html_content = get_content(url_request)
write(html_content, DL_FILE)

get_content()