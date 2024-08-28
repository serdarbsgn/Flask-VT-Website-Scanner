from flask import request
from app import app
from app.scrape_urls import get_links

@app.route('/scan',methods=['GET'])
def scan():
    url = request.args.get("url",type=str)
    if not url or url.find(".") == -1 or url.startswith("."):
        return "Supply a valid URL",400
    response = get_links(url)
    return response