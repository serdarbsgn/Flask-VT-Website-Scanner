import flask
from app import settings
app = flask.Flask(__name__)
app.json.ensure_ascii = False # for weird json not rendering "ş" etc.
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # maximum uploaded jpg size of 2 megabytes.
import redis
import sqlalchemy
r = redis.StrictRedis(host='localhost', port=6379, db=0,password=settings.REDIS_PASSWORD)
sql_engine = sqlalchemy.create_engine(
                "mysql://"+settings.MYSQL_USER+":"+settings.MYSQL_PW+"@localhost/"+settings.MYSQL_DB,
                isolation_level="READ UNCOMMITTED")