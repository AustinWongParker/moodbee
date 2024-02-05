import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('test-database.db')
cursor = conn.cursor()

# Check if the first table already exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_mood_table'")
table1_exists = cursor.fetchone()

# Check if the second table already exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_user_credential_table'")
table2_exists = cursor.fetchone()

# If the first table does not exist, create it
if not table1_exists:
    cursor.execute("CREATE TABLE test_mood_table (emotion_id, user_id, selectedImage, comment, date)")
    print("Table 'test_mood_table' created successfully")
else:
    print("Table 'test_mood_table' already exists")

# If the second table does not exist, create it
if not table2_exists:
    cursor.execute("CREATE TABLE test_user_credential_table (user_id, username, email, password)")
    print("Table 'test_user_credential_table' created successfully")
else:
    print("Table 'test_user_credential_table' already exists")

# Commit the changes and close the connection
conn.commit()
conn.close()
