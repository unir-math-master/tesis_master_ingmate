import mysql.connector

ingmate_bdd = mysql.connector.connect(user='jbalsells', password='12345678', host='127.0.0.1', database='unir_ingmate')
cursor = ingmate_bdd.cursor()

cursor.execute("SHOW TABLES")
myresult = cursor.fetchall()

print(myresult)

cursor.close()
ingmate_bdd.close()
