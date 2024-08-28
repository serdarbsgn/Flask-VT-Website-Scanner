from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class MainURLs(Base):
    __tablename__ = "main_urls"
    id = Column(Integer(),primary_key = True)
    url_hash = Column(String(64), unique=True, nullable=False)
    url = Column(String(2047), nullable=False)
    last_scanned = Column(DateTime, default=datetime.now)
    
class ScannedURLs(Base):
    __tablename__ = "scanned_urls"
    id = Column(Integer, primary_key=True, nullable=False)
    url_hash = Column(String(64), unique=True, nullable=False)
    url = Column(String(2047))
    malicious = Column(Integer, default=0)
    suspicious = Column(Integer, default=0)
    undetected = Column(Integer, default=0)
    harmless = Column(Integer, default=0)
    timeout = Column(Integer, default=0)
    last_scanned = Column(DateTime, default=datetime.now)

class MSURLs(Base):
    __tablename__ = "ms_urls"
    main_url_id = Column(Integer(),primary_key = True)
    scanned_url_id = Column(Integer(),primary_key = True)

class ReportResults(Base):
    __tablename__ = "report_results"
    scanned_url_id = Column(Integer,  nullable=False, primary_key=True)
    engine_name = Column(String(255), nullable=False, primary_key=True)
    method = Column(String(50))
    category = Column(String(50))
    result = Column(String(50))