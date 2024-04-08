from bson import ObjectId
from db import collection
from models import Student, StudentUpdate
from typing import List
from pymongo.errors import PyMongoError
from fastapi import HTTPException

def create_student(student: Student):
  student_data = student.dict()
  inserted_student = collection.insert_one(student_data)
  return {"id": str(inserted_student.inserted_id)}

def get_students(country: str = None, min_age: int = 0) -> List[dict]:
  query = {}
  if country:
    query["address.country"] = country
  if min_age:
     query["age"] = {"$gte": min_age}
  students = []
  for student_data in collection.find(query):
    students.append(student_data)
  return students

def get_student_by_id(student_id: str) -> Student:
  student_data = collection.find_one({"_id": ObjectId(student_id)})
  if student_data:
    return student_data
  else:
    return None

def update_student(student_id: str, student_data: StudentUpdate):
  try:
    update_fields = {}
    if student_data.name is not None:
      update_fields["name"] = student_data.name
    if student_data.age is not None:
      update_fields["age"] = student_data.age
    if student_data.address is not None:
      update_fields["address"] = student_data.address.dict()

    result = collection.update_one({"_id": ObjectId(student_id)}, {"$set": update_fields})
    if result.matched_count == 0:
      raise HTTPException(status_code=404, detail="Student not found")
  except PyMongoError as e:
    raise HTTPException(status_code=500, detail="Internal server error")

def delete_student(student_id: str) -> bool:
  try:
    result = collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
      raise HTTPException(status_code=404, detail="Student not found")
  except PyMongoError as e:
    raise HTTPException(status_code=500, detail="Internal server error")
    
