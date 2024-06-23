import mysql.connector as mysql
import creds
import os
import dotenv

dotenv.load_dotenv()

db = mysql.connect(
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSW'),
    host=creds.host,
    port=creds.port,
    database=creds.database
)


cursor = db.cursor(dictionary=True)
cursor.execute('SELECT * FROM students')
data = cursor.fetchall()
print(data)
