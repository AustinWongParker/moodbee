import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Check if the first table already exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Mood'")
table1_exists = cursor.fetchone()

# Check if the second table already exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='UserCredential'")
table2_exists = cursor.fetchone()

# # Check if the second table already exists
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_credential'")
# table3_exists = cursor.fetchone()

# If the first table does not exist, create it
if not table1_exists:
    cursor.execute("CREATE TABLE Mood (id, selectedImage, comment, date)")
    print("Table 'Mood' created successfully")
else:
    print("Table 'Mood' already exists")

# If the second table does not exist, create it
if not table2_exists:
    cursor.execute("CREATE TABLE UserCredential (id, username, email, password)")
    print("Table 'UserCredential' created successfully")
else:
    print("Table 'UserCredential' already exists")
    
# # If the second table does not exist, create it
# if not table3_exists:
#     cursor.execute("CREATE TABLE user_credential (user_id, username, email, password)")
#     print("Table 'user_credential' created successfully")
# else:
#     print("Table 'user_credential' already exists")

# Commit the changes and close the connection
conn.commit()
conn.close()
