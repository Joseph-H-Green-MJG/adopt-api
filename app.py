from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os


app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://broxznhmvrkkqc:24d375880b5ae86c3ce30a89a50b34076813f6b78c8ad7a1448b0675c7064a03@ec2-107-20-185-16.compute-1.amazonaws.com:5432/d810s85l0d5u24"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class adopt_item(db.Model):
    __tablename__ = "Adopt Items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    img_url = db.Column(db.String(300), unique=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    
    def __init__(self, img_url, description, title):
        self.img_url = img_url
        self.description = description
        self.title = title
    

class adoptItemsSchema(ma.Schema):
    class Meta:
        fields = ("id", "img_url", "description")

adopt_item_schema = adoptItemsSchema()
adopt_items_schema = adoptItemsSchema(many=True)

@app.route("/adopt-items", methods=["GET"])
def get_adopt_items():
    adopt_items = adopt_item.query.all()
    result = adopt_items_schema.dump(adopt_items)
    return jsonify(result.data)

@app.route("/adopt-item/<id>", methods=["PUT"])
def edit_adopt_item(id):
    adopt_one_item = adopt_item.query.get(id)
    new_img_url = request.json["img_url"]
    new_title = request.json["title"]
    new_description = request.json["description"]
    adopt_one_item.img_url = new_img_url
    adopt_one_item.title = new_title
    adopt_one_item.description = new_description
    db.session.commit()
    return adopt_item_schema.jsonify(adopt_one_item)

@app.route("/add-adopt-item", methods=["POST"])
def add_adopt_item():
    img_url = request.json["img_url"]
    title = request.json["title"]
    description = request.json["description"]
    record = adopt_item(img_url, title, description)
    db.session.add(record)
    db.session.commit()
    adopt_new_item = adopt_item.query.get(record.id)
    return adopt_item_schema.jsonify(adopt_new_item)

@app.route("/delete-adopt-item/<id>", methods=["DELETE"])
def delete_adopt_item(id):
    record = adopt_item.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify("Record Deleted")

if __name__ == "__main__":
    app.debug = True
    app.run()