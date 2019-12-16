import pymysql
import cryptography

# Open database connection
db = pymysql.connect("ec2-18-225-11-231.us-east-2.compute.amazonaws.com","moodleuser","bluehatssjsu","moodle" )

# Connect to the database
connection = pymysql.connect(host='18.225.11.231',
user='moodleuser',
db='moodle',
charset='utf8',
cursorclass=pymysql.cursors.DictCursor)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

cursor.execute("SHOW TABLES")
result = cursor.fetchall()
print(result)
for i in range(len(result)):
	print(result[i])

print('----mdl_user-----')
cursor.execute("SELECT * FROM mdl_user")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])
'''
mdl_user; mdl_sessions
result = cursor.fetchall()
print(result)
for i in range(len(result)):
	print(result[i])

print('----mdl_config-----')
cursor.execute("SELECT * FROM mdl_config")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])
'''
print('----mdl_sessions-----')
cursor.execute("SELECT * FROM mdl_sessions")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])


print('----mdl_role-----')
cursor.execute("SELECT * FROM mdl_role")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])


print('----mdl_enrol-----')
cursor.execute("SELECT * FROM mdl_enrol")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])


print('----mdl_course-----')
cursor.execute("SELECT * FROM mdl_course")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])


print('----mdl_user_enrolments-----')
cursor.execute("SELECT * FROM mdl_user_enrolments")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])


print('----mdl_role_assignments-----')
cursor.execute("SELECT * FROM mdl_role_assignments")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])

print('----Columns: mdl_user-----')
cursor.execute("desc mdl_user")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])

print('----mdl_user-----')
cursor.execute("SELECT id, auth, username,idnumber,  firstname, lastname, password FROM mdl_user")
result = cursor.fetchall()
for i in range(len(result)):
	print(result[i])

