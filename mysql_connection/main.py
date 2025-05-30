from fastapi import FastAPI , HTTPException , Depends, status
from pydantic import BaseModel, Field
from typing import Annotated
import models
from database import engine , SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class Course(BaseModel):
    course_name:str = Field(min_length=4, max_length=100)
    price:int = Field(gt=-1)
    stud_id:int

class Student(BaseModel):
   stud_name:str


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


db_dependancy = Annotated[Session,Depends(get_db)]


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student:Student, db:db_dependancy):
  try:
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    return db_student
  except Exception as e:
    raise HTTPException(
       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
       detail="Error occures"
    )
  
@app.get("/students")
def get_students(db:db_dependancy):
  students = db.query(models.Student).all()
  return students

@app.get("/student/{id}")
def get_single_student(id:int,db:db_dependancy):
  student = db.query(models.Student).filter(models.Student.stud_id == id).first()
  return student

@app.post("/course")
def create_course(course:Course,db:db_dependancy):
   course = models.Course(**course.model_dump())
   db.add(course)
   db.commit()
   return course

@app.get("/courses")
def get_courses(db:db_dependancy):
  courses = db.query(models.Course).all()
  return courses

@app.delete("/course/{id}")
def delete_courses(id,db:db_dependancy):
  db.query(models.Course).filter(models.Course.stud_id == id).delete()
  db.commit()
  return {"message":"course deleted"}

# @app.post("/courses")
# def add_course(course:Course):
#   for c in courses:
#     if c.id == course.id:
#        raise HTTPException(
#           status_code=404,
#           detail="Course already defined"
#        )
#   else:
#      courses.append(course)
#      return {"success":True,"message":"Course added successfully"}
  

# @app.put("/course-update/{id}")
# def update_course(id:int,course:Course):
#     for i,c in enumerate(courses):
#       if c.id == id:
#           courses[i] = course
#           return {"success":True,"message":"Course updated successfully"}
#     else:
#       raise HTTPException(
#        status_code=404,
#        detail="Course not found to update"
#       ) 
    
# @app.delete("/delete/{id}")
# def delete_course(id:int):
#    for c in courses:
#      if c.id == id:
#        courses.remove(c)
#        return {"seccess":True,"message":"Course removed successfully"}
#    else:
#      raise HTTPException(
#         status_code=404,
#         detail="Course id not found"
#      )

