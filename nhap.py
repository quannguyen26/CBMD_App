import sqlite3
from datetime import datetime
cbmd_db=sqlite3.connect(f'database/cbmd_database_{datetime.now().strftime("%d/%m/%Y")[6:10]}.db')
mycursor = cbmd_db.cursor()
mycursor.execute("SELECT MAX(id_news) FROM cbmd_news")
observer=mycursor.fetchone()[0]
#number_news_ent_var.set(id_news)
cbmd_db.close()
print(observer)
cbmd_db.close()