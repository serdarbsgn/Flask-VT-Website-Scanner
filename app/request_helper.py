import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def requests_retry_session(
    retries=6,
    backoff_factor=0.5,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=3,
        connect=2,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def session_get(url,session=None,verify=True,headers=None):
    if session is None:
        session = requests_retry_session()
    get_result = None
    try:
        get_result = session.get(url,verify=verify,headers=headers,timeout=15)
    except Exception as e:
        logging.info(f"Failed GET request to: {url}. Exception: {e}")
    return get_result

def session_post(url,session=None,verify=True,headers=None,data=None):
    if session is None:
        session = requests_retry_session()
    post_result = None
    try:
        post_result = session.post(url,verify=verify,headers=headers,data=data,timeout=15)
    except Exception as e:
        logging.info(f"Failed POST request to: {url}. Exception: {e}")
    return post_result