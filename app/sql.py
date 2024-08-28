from sqlalchemy.orm import Session
from sqlalchemy import  delete, func, select
from sqlalchemy.dialects.mysql import insert
from app.sql_tables import MainURLs,ScannedURLs,MSURLs,ReportResults
class sqlconn:

    def __init__(self,def_engine):
        engine = def_engine
        connection = engine.connect()
        connection = connection.execution_options(
        stream_results=True,
        isolation_level="READ UNCOMMITTED"
)
        self.session = Session(engine)
        self.connection = connection

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def execute(self,query):
        try:
            self.session.execute(query)
            return True
        except Exception as e:
            print(F"Error in sql query execution. query was: {str(query)} exception :{e}")
            return False
    
    def commit(self):
        try:
            self.session.commit()
            return True
        except:
            print("Error while committing to the database.")
            return False

    def close(self):
        try:
            self.session.invalidate()
            self.connection.close()
        except:
            print("Error closing connections")

class Select:
    def main_urls():
        return select(MainURLs.id,MainURLs.url_hash,MainURLs.url,MainURLs.last_scanned)
    
    def main_urls_url_from_id(id):
        return select(MainURLs.url).where(MainURLs.id == id)
    
    def main_urls_id_from_hash(url_hash):
        return select(MainURLs.id).where(MainURLs.url_hash == url_hash)

    def scanned_urls_from_main_id(main_id):
        return select(ScannedURLs.id,ScannedURLs.url,ScannedURLs.url_hash,ScannedURLs.malicious,ScannedURLs.suspicious,ScannedURLs.undetected,ScannedURLs.harmless,ScannedURLs.timeout,ScannedURLs.last_scanned
                           ).where(MSURLs.scanned_url_id == ScannedURLs.id,MainURLs.id == MSURLs.main_url_id
                                              ).join(MSURLs,ScannedURLs.id == MSURLs.scanned_url_id).join(MainURLs,MSURLs.main_url_id == MainURLs.id).where(MainURLs.id == main_id)
    def scanned_urls_url_from_id(scan_id):
        return select(ScannedURLs.url).where(ScannedURLs.id == scan_id)
        
    def scanned_urls_id_from_hash(url_hash):
        return select(ScannedURLs.id).where(ScannedURLs.url_hash == url_hash)
    
    def report_results_from_scanned_id(scanned_id):
        return select(ReportResults.engine_name,ReportResults.method,ReportResults.category,ReportResults.result).where(ReportResults.scanned_url_id == scanned_id)

    
class Insert:
    def main_urls(data):
        return insert(MainURLs).values(url = data["url"],url_hash = data["url_hash"]
                                       ).on_duplicate_key_update(last_scanned = func.now())
    
    def scanned_urls(data):
        return insert(ScannedURLs).values(url = data["url"],url_hash = data["url_hash"],
                                          malicious = data["malicious"],suspicious = data["suspicious"],
                                          undetected = data["undetected"],harmless=data["harmless"],
                                          timeout = data["timeout"],last_scanned = data["date"]
                                          ).on_duplicate_key_update(malicious = data["malicious"],suspicious = data["suspicious"],
                                            undetected = data["undetected"],harmless=data["harmless"],
                                            timeout = data["timeout"],last_scanned = data["date"])
    
    def ms_urls(data):
        return insert(MSURLs).values(main_url_id=data["main_url_id"],scanned_url_id = data["scanned_url_id"]
                                     ).on_duplicate_key_update(scanned_url_id = data["scanned_url_id"])
    
    def report_results(data):
        return insert(ReportResults).values(scanned_url_id=data["scanned_url_id"],engine_name=data["engine_name"],
                                            method=data["method"],category=data["category"],result=data["result"]
                                            ).on_duplicate_key_update(method=data["method"],category=data["category"],
                                                                      result=data["result"])
class Delete:
    def main_urls(data):
        return delete(MainURLs).where(MainURLs.url_hash == data["url_hash"])