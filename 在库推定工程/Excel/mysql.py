import pymysql

db = pymysql.connect('localhost', 'root', '123', 'TEST')
cursor = db.cursor()