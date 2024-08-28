from dotenv import load_dotenv
import os
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
REDIS_PASSWORD = os.getenv("REDIS_PASS")
VT_API_KEY = os.getenv("VT_API_KEY")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_PW = os.getenv("MYSQL_PASSWORD")