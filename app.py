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

if __name__ == "__main__":
    app.run(debug=True)