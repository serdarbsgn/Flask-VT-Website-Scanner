from flask import flash, jsonify, redirect, render_template, request, url_for
from app import app,sql_engine
from app.scrape_urls import get_links
from app.sql import sqlconn,Select

def listify(map):
    templist = []
    for row in map:
        dicx = {}
        for key,val in row.items():
            dicx[key] = val
        templist.append(dicx)
    return templist
@app.route('/',methods = ['GET'])
def home():
    return render_template("home.html")

@app.route('/scan',methods=['GET'])
def scan():
    url = request.args.get("url",type=str)
    if not url or url.find(".") == -1 or url.startswith("."):
        return "Supply a valid URL",400
    response = get_links(url)
    return response

@app.route('/results',methods=['GET'])
def results():
    with sqlconn(sql_engine) as sql:
        main_urls = listify(sql.session.execute(Select.main_urls()).mappings().fetchall())
    return render_template("results.html",results_list = main_urls)

@app.route('/result/<int:main_id>',methods=['GET'])
def result(main_id):
    with sqlconn(sql_engine) as sql:
        main_url = sql.session.execute(Select.main_urls_url_from_id(main_id)).fetchone()
        if not main_url:
            flash("This url is not scanned")
            return redirect(url_for('results'))
        scan_result = listify(sql.session.execute(Select.scanned_urls_from_main_id(main_id)).mappings().fetchall())
    return render_template("result.html",scan_result = scan_result,main_url=main_url[0])

@app.route('/result/details/<int:scan_id>',methods=['GET'])
def detail(scan_id):
    with sqlconn(sql_engine) as sql:
        scan_url = sql.session.execute(Select.scanned_urls_url_from_id(scan_id)).fetchone()
        if not scan_url:
            flash("This is not avalid scan id")
            return redirect(url_for('results'))
        detail_results = listify(sql.session.execute(Select.report_results_from_scanned_id(scan_id)).mappings().fetchall())
    return render_template("detail.html",detail_results = detail_results,scanned_url=scan_url[0])