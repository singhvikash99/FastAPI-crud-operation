from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import List



class Base(DeclarativeBase):
    pass

class Student(Base):

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index = True)
    name: Mapped[str] = mapped_column(String(45))
    std : Mapped[int]
    roll_number : Mapped[int]


    subjects: Mapped[List['Subject']] = relationship('Subject', back_populates='students',
                                                     secondary='student_subject')
class Subject(Base):

    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index = True)
    subject: Mapped[str] = mapped_column(String(45))


    students: Mapped[List['Student']] = relationship('Student', back_populates='subjects',
                                                     secondary='student_subject')
    
class StudentSubject(Base):
    __tablename__ = "student_subject"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index = True)
    students_id : Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id : Mapped[int] = mapped_column(ForeignKey('subject.id'))






