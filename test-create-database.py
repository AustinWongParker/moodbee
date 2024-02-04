import sqlite3

connection = sqlite3.connect("test-database.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE test_mood_table (emotion_id, user_id, selectedImage, comment, date)")
connection.commit()
connection.close()