from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os


app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://icblchwfwqiszc:c41e60e6e57a258aa66028eef0dc4e03c34ee6d8e6be12ea6035a988f3067a37@ec2-50-16-197-244.compute-1.amazonaws.com:5432/db12irb85c97sd"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class adopt_item(db.Model):
    __tablename__ = "Adopt Items"
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(300), unique=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    
    def __init__(self, img_url, description):
        self.img_url = img_url
        self.description = description
    

class adoptItemsSchema(ma.Schema):
    class Meta:
        fields = ("id", "img_url", "description")

adopt_item_schema = adoptItemsSchema()
adopt_items_schema = adoptItemsSchema(many=True)

@app.route("/adopt-item", methods=["GET"])
def get_adopt_items():
    adopt_items = adopt_item.query.all()
    result = adopt_items_schema.dump(adopt_items)
    return jsonify(result.data)

if __name__ == "__main__":
    app.debug = True
    app.run()