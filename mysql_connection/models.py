from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "student"
    
    stud_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stud_name = Column(String(50))

class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_name = Column(String(100))
    price = Column(Integer)
    stud_id = Column(Integer, ForeignKey('student.stud_id')) 
