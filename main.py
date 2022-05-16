from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__,
  template_folder='templates',
  static_folder='static')

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

#connect and create a db named as mydb
app.config["MONGO_URI"] = "mongodb+srv://nafishandoko:nafis_mongo_password@cluster0.utrxa.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#initializing the client for mongodb
mongo = PyMongo(app)
#creating the customer collection
barang_collection = mongo.db.barang

@app.route('/login', methods=["POST"])
def login():
  email = request.json.get("email", None)
  password = request.json.get("password", None)
  if email != "test@mail.com" or password != "123456":
    return jsonify({"msg": "Bad email or password"}), 401

  access_token = create_access_token(identity=email)
  resp = jsonify(access_token=access_token)
  return resp

@app.route('/')
def hello():
    return 'Hello from Flask!'

@app.route('/form')
def form():
  return render_template('form.html')

@app.route("/data", methods=['GET'])
def show_data():
  if request.method == 'GET':
    nama = request.args.get("nama")
    harga = request.args.get("harga")
    stock = request.args.get("stock")
  if nama != "" and harga != "" and stock != "":
    barang = barang_collection.insert_one({"nama": nama, "harga": harga, "stock": stock})
    return ("data added to the database")
  else:
    return ("Kindly fill the form")

@app.route("/read")
@jwt_required()
def read_data():
  barang = (barang_collection.find())
  # return render_template('index.html', barang=barang)
  return dumps(list(barang))

@app.route("/read2")
def read_from_web():
  barang = (barang_collection.find())
  # return render_template('index.html', barang=barang)
  return dumps(list(barang))

@app.route("/delete")
def delete():
  barang_collection.drop()
  return "All data deleted"

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


app.run(host='0.0.0.0', port=81)