from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
students_collection = db["students"]

@app.route('/students', methods=['GET'])
def get_students():
    students = list(students_collection.find())
    for student in students:
        student['_id'] = str(student['_id'])
    return jsonify(students)

    # formatted_students = []
    # for student in students:
    #     formatted_student = {
    #         '_id': str(student['_id']),
    #         'Full Name': f"{student['first_name']} {student['last_name']}",
    #         'DOB': student['dob'],
    #         'Gender': student['gender'],
    #         'School': student['school'],
    #         'Major': student['major']
    #     }
    #     formatted_students.append(formatted_student)
    # return jsonify(formatted_students)

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    student = students_collection.find_one({"_id": ObjectId(id)})
    if student:
        student['_id'] = str(student['_id'])
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    result = students_collection.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)})

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    students_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"msg": "Student updated"})

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    students_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Student deleted"})

if __name__ == '_main_':
    app.run(debug=True) 