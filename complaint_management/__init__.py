# loading pymysql as mysql, only needed when using mysql db
import pymysql

pymysql.version_info = (1, 4, 0, "final", 0)
pymysql.install_as_MySQLdb()