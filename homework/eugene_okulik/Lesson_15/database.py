import mysql.connector as mysql

db = mysql.connect(
    user='st-onl',
    passwd='AVNS_tegPDkI5BlB2lW5eASC',
    host='db-mysql-fra1-09136-do-user-7651996-0.b.db.ondigitalocean.com',
    port=25060,
    database='st-onl'
)


cursor = db.cursor(dictionary=True)
cursor.execute('SELECT * FROM students')
data = cursor.fetchall()
print(data)
# for student in data:
#     print(student['second_name'])

cursor.execute('SELECT * FROM students WHERE id = 2')
data1 = cursor.fetchone()
cursor.execute('SELECT * FROM students WHERE id = 3')
data2 = cursor.fetchone()
print(data2)

# f"SELECT * FROM users WHERE user = '{user}' and password = '{passw}'"
# query = "SELECT * FROM students WHERE name = '{0}' and second_name = '{1}'"
# cursor.execute(query.format(input('name'), input('second_name')))
# Maksim'; --
# pupkin
query = "SELECT * FROM students WHERE name = %s and second_name = %s"
cursor.execute(query, (input('name'), input('second_name')))
print(cursor.fetchall())

cursor.execute("INSERT INTO students (name, second_name, group_id) VALUES ('Ivan', 'Ivanov', 1)")
student_id = cursor.lastrowid
cursor.execute(f'SELECT * from students where id = {student_id}')
print(cursor.fetchone())

insert_query = "INSERT INTO students (name, second_name, group_id) VALUES (%s, %s, %s)"
cursor.executemany(
    insert_query, [
        ('Ivan', 'Ivanov', 1),
        ('Ivan2', 'Ivanov2', 1)
    ]
)

select_query = '''
SELECT *
FROM students
WHERE name = 'George'
AND second_name = 'Washington'
'''

cursor.execute(select_query)
print(cursor.fetchall())

db.commit()


db.close()
