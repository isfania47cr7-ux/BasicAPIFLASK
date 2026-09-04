from flask import Flask, app,request,jsonify
import json
import os

from app import load_students, save_students
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

@customers.route("/home")
def home():
    return jsonify({
        "Welcome":"Welcome to Customer Management "
    })

def save_customers(customers):
    with open(FILE_NAME,"w") as file:
        json.dump(customers,file,indent=4)

@customers.route("/customers",methods=["POST"])
def add_customer():
    customers=load_customers()
    data=request.json
    if not data.get("id"):
        return jsonify({"message":"Customer Id Required"}),400
    if not data.get("product"):
        return jsonify({"message":" Product required"}),400
    if not data.get("quantity"):
        return jsonify({"message":"Product Quantity Required"}),400
    if not data.get("price"):
        return jsonify({"message":"Product Price Required"}),400
    for customer in customers:
        if customer["id"] == data["id"]:
            return jsonify({
                "message":"Customer ID Already Exists"
            }),400
    customers.append(data)
    
    save_customers(customers)
    
    return jsonify({
        "message":"Customer Added Successfully"
    })

@customers.route("/customers",methods=["GET"])
def get_customers():
    customers=load_customers()
    return jsonify(customers)

@customers.route("/customers/<int:id>",methods=["GET"])
def get_customer(id):
    customers=load_customers()
    for customer in customers:
        if customer["id"]==id:
            return jsonify(customer)
        
    return jsonify({
        "message":"Customer Not Found"
    }),404

@customers.route("/customers/<int:id>",methods=["PUT"])
def update_customer(id):
    customers=load_customers()
    data=request.json
    
    for customer in customers:
        if customer["id"]==id:
            customer["product"]=data.get("product",customer["product"])
            customer["quantity"]=data.get("quantity",customer["quantity"])
            customer["price"]=data.get("price",customer["price"])

            save_customers(customers)
            return jsonify({
                "message":"Customer Updated Successfully"
            })
        
    return jsonify({
        "message":"Customer Not Found"
    }),404

@customers.route("/customers/<int:id>",methods=["DELETE"])
def delete_customer(id):
    customers=load_customers()
    for customer in customers:
        if customer["id"]==id:
            customers.remove(customer)
            save_customers(customers)
            return jsonify({
                "message":"Customer Deleted Successfully"
            })
        
    return jsonify({
        "message":"Customer Deleted successfully"
    }),404

@customers.route("/customers/search/<product>",methods=["GET"])
def search_customer(product):
    customers=load_customers()
    result=[]
    for customer in customers:
        if product.lower() in customer["product"].lower():
            result.append(customer)
    return jsonify(result) 

@customers.route("/customers/statistics")
def statistics():
    customers=load_customers()
    total=len(customers)

    average_price=sum(customer["price"] for customer in customers)/total if total else 0
    soap_customers=len([customer for  customer in customers if customer["product"].lower()=="soap"])
    shampoo_customers=len([customer for customer in customers if customer["product"].lower()=="shampoo"])

    return jsonify({
        "Total Customers":total,
        "Average Price":round(average_price, 2),
        "Soap Customers":soap_customers,
        "Shampoo Customers":shampoo_customers
    })

@customers.route("/customers/count")
def count_customers():
    customers=load_customers()
    return jsonify({
        "Total Customers":len(customers)
    })

if __name__ =="__main__":
    customers.run(debug=True)


