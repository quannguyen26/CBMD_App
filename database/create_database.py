import sqlite3
from datetime import datetime

connection=sqlite3.connect(f'database/cbmd_database_{datetime.now().strftime("%d/%m/%Y")[6:10]}.db')
cur=connection.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS cbmd_news(
	"id_news"	INTEGER NOT NULL,"time_now"	TEXT,"date_now"	TEXT,"kind_news"	NUMERIC,
	"Derection"	TEXT,"Velocity"	TEXT,"Zmax"	INTEGER,"location_zmax"	TEXT,"weather13next"TEXT,"hail"	INTEGER,
	"time_send"	TEXT,"day_send"	INTEGER,"observer"	INTEGER,"image"	BLOB,
    "laichau_now"	TEXT,"laichau_13h"	TEXT,
	"dienbien_now"	TEXT,"dienbien_13h"	TEXT,
	"sonla_now"	TEXT,"sonla_13h"	TEXT,
	"hoabinh_now"	TEXT,
	"hoabinh_13h"	TEXT,
	"laocai_now"	TEXT,
	"laocai_13h"	TEXT,
	"yenbai_now"	TEXT,
	"yenbai_13h"	TEXT,
	"name_file"	TEXT,
	PRIMARY KEY("id_news")
)
""")
cur.execute("""CREATE TABLE IF NOT EXISTS cbmd_login(
	"id_login"	INTEGER NOT NULL,
	"name_login"	TEXT,
	"date_login"	TEXT,
	PRIMARY KEY("id_login" AUTOINCREMENT)
)""")
connection.commit()


connection.close()