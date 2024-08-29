import json
import time
import os
import redis
from app.request_helper import session_get, session_post
import sqlalchemy
from app.sql import sqlconn,Select,Insert
from datetime import datetime, timedelta
import logging
def main():
    import app.settings as s
    def scan_url_request(url):
        payload = {"url": url}
        headers = {"accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded",
                    "x-apikey": s.VT_API_KEY}
        
        response = session_post(VT_API_LINK,headers=headers,data=payload)
        if not response or response.status_code != 200:
            logging.warn(f"Scan request went wrong in some way: {url}")
            return None
        return response
    def scan_result_request(hash):
        headers = {"accept": "application/json",
            "x-apikey": s.VT_API_KEY}
        response = session_get(VT_API_LINK+f"/{hash}",headers=headers)
        if not response or response.status_code != 200:
            logging.warn(f"Result read request went wrong in some way: {hash}")
            return None
        return response
    def request_and_insert_results(url,url_hash):
        get_report = scan_result_request(url_hash)
        if get_report:
            get_report = json.loads(get_report.content.decode())
            with sqlconn(sql_engine) as sql:
                sql.execute(Insert.scanned_urls({"url":url,"url_hash":url_hash,
                                                    **get_report["data"]["attributes"]["last_analysis_stats"],
                                                    "date":datetime.fromtimestamp(get_report["data"]["attributes"]["last_analysis_date"])}))
                sql.commit()
                url_id = sql.session.execute(Select.scanned_urls_id_from_hash(url_hash)).fetchone()[0]
                sql.execute(Insert.ms_urls({"main_url_id":main_url_id,"scanned_url_id":url_id}))
                for value in get_report["data"]["attributes"]["last_analysis_results"].values():
                    sql.execute(Insert.report_results({"scanned_url_id":url_id,"engine_name":value["engine_name"],"method":value["method"],"category":value["category"],"result":value["result"]}))
                sql.commit()
        else: return (url,url_hash)
    sql_engine = sqlalchemy.create_engine(
                "mysql://"+s.MYSQL_USER+":"+s.MYSQL_PW+"@db/"+s.MYSQL_DB,
                isolation_level="READ UNCOMMITTED")
    VT_API_LINK = "https://www.virustotal.com/api/v3/urls"
    r = redis.StrictRedis(host=os.getenv('REDIS_HOST',"localhost"), port=6379, db=0,password=s.REDIS_PASSWORD)
    failed_request_flag = False
    failed_result_flag = False
    previous_main_url = None
    while True:
        main_url = None
        if not previous_main_url:
            results = None
            with r.pipeline() as pip:
                pip.rpop("main_url_queue")
                pip.rpop("list_queue")
                results = pip.execute()
            main_url, url_list = results
            if not main_url:
                logging.info("Queue empty, I'll sleep for 2 minutes.")
                time.sleep(120)
                continue
            main_url = main_url.decode()
            logging.info(f"Processing {main_url}")
            url_list = json.loads(url_list)["links"]
            response = scan_url_request(main_url)
            main_url_id = None
            if response and response.status_code == 200:
                main_url_hash = json.loads(response.content.decode())["data"]["id"].split("-")[1]
                with sqlconn(sql_engine) as sql:
                    sql.execute(Insert.main_urls({"url":main_url,"url_hash":main_url_hash}))
                    sql.commit()
                    main_url_id = sql.session.execute(Select.main_urls_id_from_hash(main_url_hash)).fetchone()[0]
            else:
                data = {
                    "links": list(url_list)
                    }
                serialized_data = json.dumps(data)
                with r.pipeline() as pip:
                    pip.lpush('main_url_queue', main_url)
                    pip.lpush('list_queue', serialized_data)
                    pip.execute()
                logging.info("Time to rest (3 minutes) before trying again.")
                time.sleep(180)
                continue
            responses = {main_url:response}
        else:
            main_url = previous_main_url
        failed_scan_request_responses = list()
        if failed_request_flag:
            for url in failed_request_flag:
                temp_response = scan_url_request(url)
                if temp_response is not None:
                    responses[url] = temp_response
        else:
            for url in url_list:
                temp_response = scan_url_request(url)
                if temp_response is None:
                    failed_scan_request_responses.append(url)
                    time.sleep(10)
                else:
                    responses[url] = temp_response

        time.sleep(15)
        failed_scan_result_responses = list()
        if failed_result_flag:
            for item in failed_result_flag:
                url = item[0]
                url_hash = item[1]
                request_and_insert_results(url,url_hash)
        else:
            for url,resp in responses.items():
                content = json.loads(resp.content.decode())
                url_hash = content["data"]["id"].split("-")[1]
                failed = request_and_insert_results(url,url_hash)
                if failed:
                    failed_scan_result_responses.append(failed)
                    time.sleep(10)
        if failed_scan_request_responses:
            failed_request_flag = failed_scan_request_responses
            previous_main_url = main_url
            logging.info("There are some requests that are failed. Will try once more to request it.")
        elif failed_scan_result_responses:
            failed_result_flag = failed_scan_result_responses
            previous_main_url = main_url
            logging.info("There are some results that couldn't be fetched. Will try once more to retrieve it.")
        else:
            failed_request_flag = False
            failed_result_flag = False
            previous_main_url = None
            r.setex(f"worked_main_urls_exp:{main_url}", 3600, str(datetime.now()+timedelta(hours=1)))
            logging.info(f"Finished working on {main_url}, set it a 1 hour cooldown on this URL not to waste api credits.")
            #Reset flags to default.Add 1 hour cooldown to this url.
        r.srem("main_urls",main_url)


if __name__ == "__main__":
    main()