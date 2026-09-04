from flask import Flask,request,jsonify
from database import get_connection

app=Flask(__name__)

@app.route("/home")
def home():
    return jsonify({
        "message":"Student Management API using SQLite"
    })

@app.route("/students",methods=["POST"])
def add_student():
    data=request.json
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
        INSERT INTO students(id,name,course,age)
        VALUES(?,?,?,?)
        """,(
            data["id"],
            data["name"],
            data["course"],
            data["age"]
        )
    )
    conn.commit()
    conn.close()
    return jsonify({
        "success":True,
        "message":"Student Added Successfully"
    }),201

@app.route("/students",methods=["GET"])
def get_students():
    conn=get_connection()
    try:
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM students")
        students=cursor.fetchall()
        
        data=[]
        for student in students:
            data.append(dict(student))

        return jsonify({
            "message":True,
            "data":data
        })
       
    finally:
        conn.close()

@app.route("/students/<int:id>",methods=["GET"])
def get_student(id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students  WHERE id=?",(id,))
    student=cursor.fetchone()

    conn.close()
    if student:
        return jsonify({
            "message":True,
            "data":dict(student)
        })
    
    return jsonify({
        "message":False,
        "message":"Student Not Found"
    }),404

@app.route("/students/<int:id>",methods=["PUT"])
def update_student(id):
    data=request.json
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
    UPDATE students 
    SET name=?,
    course=?,
    age=?
    WHERE id=?
    """,
    (
        data["name"],
        data["course"],
        data["age"],
        id
    ))
    conn.commit()
    conn.close()
    return jsonify({
        "success":True,
        "message":"Student Updated Successfully"
    })

@app.route("/students/<int:id>",methods=["DELETE"])
def delete_student(id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?",(id,))
    conn.commit()
    conn.close()

    return jsonify({
        "success":True,
        "message":"Student Deleted Successfully"
    })

@app.route("/students/search/<name>")
def search_name(name):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?",("%"+name+"%",))
    students=cursor.fetchall()
    conn.close()
    return jsonify(
        
        [dict(student) for student in students ]
    )
                   
if  __name__ =="__main__":
    app.run(debug=True)