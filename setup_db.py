import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS CivicFix;")
cursor.execute("USE CivicFix;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE,
password VARCHAR(255),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute('''
CREATE TABLE IF NOT EXISTS complaints(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
title VARCHAR(200) NOT NULL, 
description TEXT NOT NULL,
category VARCHAR(100),
location VARCHAR(255),
latitude DECIMAL(10, 7),
longitude DECIMAL(10, 7),
status VARCHAR(50) DEFAULT 'pending',
image VARCHAR(250),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS complaints_images(
# id INT AUTO_INCREMENT PRIMARY KEY,
# complaint_id INT,
# image_path VARCHAR(255),
# FOREIGN KEY (complaint_id) REFERENCES complaints(id)
# );
# """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
complaint_id INT,
message TEXT,
is_read BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (complaint_id) REFERENCES complaints(id)
);
""")


conn.commit()