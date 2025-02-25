from flask import Flask, request, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["data-sensor"]

app = Flask(_name_)

client = MongoClient('mongodb://localhost:27017/')
db = client['data-sensor']  
collection = db['data']  

@app.route('/data', methods=['POST'])
def post_data():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = collection.insert_one(data)

    return jsonify({"message": "Data saved", "id": str(result.inserted_id)}), 201

if _name_ == '_main_':
    app.run(debug=True)
