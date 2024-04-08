from fastapi import FastAPI, HTTPException
from service import create_student, get_students, get_student_by_id, update_student, delete_student
from models import Student, StudentUpdate

app = FastAPI()

@app.post("/students/", response_model=dict, status_code=201)
async def create_new_student(student: Student):
  return create_student(student)

@app.get("/students/", response_model=dict, status_code=200)
async def get_student_list(country: str = None, age: int = None):
  students = get_students(country, age)
  formatted_students = [{"name": student['name'], "age": student['age']} for student in students]
  return {"data": formatted_students}

@app.get("/students/{student_id}", response_model=Student, status_code=200)
async def get_student_by_id_endpoint(student_id: str):
  student = get_student_by_id(student_id)
  if student:
    return student
  else:
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{student_id}", response_model={}, status_code=204)
async def update_student_endpoint(student_id: str, student_data: StudentUpdate):
  if get_student_by_id(student_id):
    update_student(student_id, student_data)
    return {}
  else:
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}", status_code=200)
async def delete_student_endpoint(student_id: str):
  if get_student_by_id(student_id):
    delete_student(student_id)
    return {}
  else:
    raise HTTPException(status_code=404, detail="Student not found")
