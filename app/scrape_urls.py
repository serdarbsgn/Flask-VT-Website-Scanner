from datetime import datetime
import json
from multiprocessing import Process
from bs4 import BeautifulSoup as bs
from app.request_helper import session_get
from urllib.parse import urljoin
from app import r


def get_links(main_url):
    headers = {"User-Agent": "Mozilla"}
    if not main_url.startswith(("http://", "https://")):
        main_url = "http://"+main_url
    response = session_get(main_url,headers=headers)
    if not response:
        return "Supplied URL seems wrong/non-reachable.",400
    main_url = response.url
    if r.sismember("main_urls",main_url):
        return "Already queued URL",202
    if r.exists(f"worked_main_urls_exp:{main_url}"):
        return f"Please request the scan after a while : {str(r.get(f'worked_main_urls_exp:{main_url}'))}, it's currently : {str(datetime.now())}",400
    if response.content is not None:
        thread = Process(target = scrape_html_for_urls,args =(response,))
        thread.start()
        return "Processing URL...",200
    
def scrape_html_for_urls(response):
    main_url = response.url
    response = response.content.decode()
    html = bs(response,features="html.parser")
    links = set() #Prevent duplicates.
    for tag in html.find_all(['a', 'img', 'script', 'link']):
        templink = None
        if tag.has_attr("src"):
            templink = tag["src"]
        elif tag.has_attr("href"):
            templink = tag["href"]
        if not templink or templink=="#" or templink=="/":
            continue
        templink = urljoin(main_url, templink)
        links.add(templink)
    with r.pipeline() as pip:
        data = {
            "links": list(links)
            }
        serialized_data = json.dumps(data)
        pip.sadd('main_urls',main_url)
        pip.lpush('main_url_queue', main_url)
        pip.lpush('list_queue', serialized_data)
        pip.execute()

