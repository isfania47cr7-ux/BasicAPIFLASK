from flask import Flask, app,request,jsonify
import json
import os
customers=Flask(__name__)
FILE_NAME="customers.json"

def load_customers():
    if not os.path.exists(FILE_NAME):
        return[]
    with open(FILE_NAME,"r")as file:
        return json.load(file)

def save_customers(customers):
    with open(FILE_NAME,"w")as file:
        json.dump(customers,file,indent=4)

@customers.route("/")
def home():
    return jsonify({
        "Welcome":"Welcome to Customer Management "
    })

def save_customers(customers):
    with open(FILE_NAME,"w") as file:
        json.dump(customers,file,indent=4)

@customers.route("/customers",methods=["POST"])
def add_customer()")

if __name__ =="__main__":
    customers.run(debug=True)


