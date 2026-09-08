import sqlite3

DATABASE="student.db"

def get_connection():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def create_table():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                age INTEGER NOT NULL
                )""")

    cursor.execute("PRAGMA table_info(students)")
    columns_student=cursor.fetchall()
    column_names_student=[column[1] for column in columns_student]
    if "photo" not in column_names_student:
        cursor.execute("ALTER TABLE students ADD COLUMN photo TEXT")
    if "resume" not in column_names_student:
        cursor.execute("ALTER TABLE students ADD COLUMN resume TEXT")

    conn.commit()
    conn.close()

create_table()