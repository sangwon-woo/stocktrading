import mysql.connector as mc
import DBconfig as dbconf
conn = mc.connect(**dbconf.dbConfig)
cursor = conn.cursor()
cursor.execute("SHOW DATABASES;")


data = cursor.fetchall()
dt = type(data)

print("data:", data)
print("type:", dt)


conn.close()