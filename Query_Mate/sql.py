import sqlite3

# Connect to SQLite
connection = sqlite3.connect("student.db")

# Create a cursor object
cursor = connection.cursor()

# Create the STUDENT table (use IF NOT EXISTS to avoid errors on multiple executions)
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    GRADE VARCHAR(25),
    MARKS INT,
    SECTION VARCHAR(5)
);
"""
cursor.execute(table_info)

# Insert some records
cursor.execute('''Insert Into STUDENT values('Kane','Data Science','A+',95,'A')''')
cursor.execute('''Insert Into STUDENT values('Jiten','Data Science','A',90,'B')''')
cursor.execute('''Insert Into STUDENT values('Austin','Data Science','A',81,'B')''')
cursor.execute('''Insert Into STUDENT values('Raj','ECE','B',50,'C')''')
cursor.execute('''Insert Into STUDENT values('Monicka','ECE','C',35,'D')''')
cursor.execute('''Insert Into STUDENT values('Serena','ECE','A',90,'C')''')
cursor.execute('''Insert Into STUDENT values('Shivansh','Data Science','A',90,'A')''')
cursor.execute('''Insert Into STUDENT values('Darren','Data Science','A',86,'A')''')
cursor.execute('''Insert Into STUDENT values('Mike','ECE','A+',100,'D')''')
cursor.execute('''Insert Into STUDENT values('Drake','ECE','F',25,'C')''')

# Display all the records
print("The inserted records are:")
data = cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

# Get the number of columns in the STUDENT table
cursor.execute("PRAGMA table_info(STUDENT);")
columns = cursor.fetchall()  # Fetch all column info
column_count = len(columns)  # The number of rows in the result is the number of columns
print(f"The number of columns in the STUDENT table is: {column_count}")

# Commit changes and close the connection
connection.commit()
connection.close()

