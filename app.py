from flask import Flask,request,jsonify
import json
import os#path,file
app=Flask(__name__)  #flask object
FILE_NAME= "students.json"#new file

def load_students():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME,"r")as file:
        return json.load(file)
    
def save_students(students):
    with open(FILE_NAME,"w")as file:
        json.dump(students,file,indent=4)

@app.route("/")
def home():
    return jsonify({
        "message":"Welcome to student management API"
    })

@app.route("/students",methods=['POST'])
def add_student():
    students=load_students()
    data=request.json
    if not data.get("id"):
        return jsonify({"message":"Student Id Required"}),400
    if not data.get("name"):
        return jsonify({"message":"Student Name required"}),400
    if not data.get("age"):
        return jsonify({"message":"Age Required"}),400
    if not data.get("course"):
        return jsonify({"message":"Course Required"}),400
    for student in students:
        if student["id"] == data["id"]:
            return jsonify({
                "message":"Student ID Already Exists"
            }),400
    students.append(data)

    save_students(students)

    return jsonify({
        "message":"Student Added Successfully"
    })

@app.route("/students",methods=["GET"])
def get_students():
    students=load_students()
    return jsonify(students)

@app.route("/students/<int:id>",methods=["GET"])
def get_student(id):
    students=load_students()
    for student in students:
        if student["id"]==id:
            return jsonify(student)
        
    return jsonify({
        "message":"Student Not Found"
    }),404

@app.route("/students/<int:id>",methods=["PUT"])
def update_student(id):
    students=load_students()
    data=request.json
    
    for student in students:
        if student["id"]==id:
            student["name"]=data.get("name",student["name"])
            student["course"]=data.get("course",student["course"])
            student["age"]=data.get("age",student["age"])

            save_students(students)
            return jsonify({
                "message":"Student Updated Successfully"
            })
        
    return jsonify({
        "message":"Student Not Found"
    }),404

@app.route("/students/<int:id>",methods=["DELETE"])
def delete_student(id):
    students=load_students()
    for student in students:
        if student["id"]==id:
            students.remove(student)
            save_students(students)
            return jsonify({
                "message":"Student Deleted Successfully"
            })
        
    return jsonify({
        "message":"Student Deleted successfully"
    }),404

@app.route("/students/course/<course>",methods=["GET"])
def search_course(course):
    students=load_students()
    result=[]

    for student in students:
        if student["course"].lower()==course.lower():
            result.append(student)
    return jsonify(result)

@app.route("/students/search/<name>",methods=["GET"])
def search_student(name):
    students=load_students()
    result=[]
    for student in students:
        if name.lower() in student["name"].lower():
            result.append(student)
    return jsonify(result) 

@app.route("/students/statistics")
def statistics():
    students=load_students()
    total=len(students)

    average_age=sum(student["age"] for student in students)/total if total else 0
    python_students=len([student for  student in students if student["course"].lower()=="python"])
    nodjs_students=len([student for student in students if student["course"].lower()=="nodjs"])

    return jsonify({
        "Total Students":total,
        "Average Age":round(average_age, 2),
        "Python Students":python_students,
        "NodeJS Students":nodjs_students
    })

@app.route("/students/count")
def count_students():
    students=load_students()
    return jsonify({
        "Total Students":len(students)
    })
                     
if __name__ == "__main__":#takes as main while executing the file
    app.run(debug=True)