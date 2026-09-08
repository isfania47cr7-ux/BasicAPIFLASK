import os
from flask import Flask,request,jsonify,send_from_directory #for downloading
from database import get_connection

app=Flask(__name__)
UPLOAD_FOLDER="uploads"
PHOTO_FOLDER=os.path.join(UPLOAD_FOLDER,"photos")
RESUME_FOLDER=os.path.join(UPLOAD_FOLDER,"resume")

os.makedirs(PHOTO_FOLDER,exist_ok=True)
os.makedirs(RESUME_FOLDER,exist_ok=True)

app.config["PHOTO_FOLDER"]=PHOTO_FOLDER
app.config["RESUME_FOLDER"]=RESUME_FOLDER

@app.route("/upload/photo",methods=["POST"])
def upload_photo():
    if "photo" not in request.files:
        return jsonify({
            "message":"Photo is required"
        }),400
    photo=request.files["photo"]

    if photo.filename=="":
        return jsonify({
            "message":"No File Selected"
        }),400
    extension=photo.filename.split(".")[-1].lower()
    
    if extension not in ["jpg","jpeg","png"]:
        return jsonify({
            "message":"Only jpg,png,jpeg files are allowed"
        }),400
    
    filename=photo.filename
    photo.save(
        os.path.join(
            app.config["PHOTO_FOLDER"],
            filename
        )
    )
    return jsonify({
        "success":True,
        "message":"Photo Uploaded Successfully",
        "filename":filename
    })

@app.route("/photos/<filename>")
def get_photo(filename):
    return send_from_directory(
        app.config["PHOTO_FOLDER"],
        filename
    )

if  __name__ =="__main__":
    app.run(debug=True)