from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only
import schemas, models, database as db

router = APIRouter(
                    prefix="/api",
                    tags=["Student"]
                )



@router.get('/students/all/')
def get_students(db = Depends(db.db_session)):
    """
    **API Endpoint for getting all students**

    *This endpoint can be used to get all the student details from the database*
    
    """
    try:
                
        db_students  = select(models.Student).options(joinedload(models.Student.subjects))
        db_students = db.scalars(db_students).unique().all()

        if db_students == []:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"no students found"})
        
        db.close()
        return {"data":db_students}
    
    except Exception as err:
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})



@router.get('/students/')
def get_students_by_subject(subject_id:int,db = Depends(db.db_session)):
    """
    **API Endpoint for getting all students according to subject**

    *This endpoint can be used to get all the student applied for a subject from the database*
    
    """
    try:
        chk_subject = db.get(models.Subject, subject_id)

        if not chk_subject:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"invalid subject_id"})        
       
        db_students  = select(models.Subject).filter(models.Subject.id == subject_id).options(joinedload(models.Subject.students))
        db_students = db.scalars(db_students).unique().all()

        if db_students == []:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"no students found"})
        
        db.close()
        return {"data":db_students}
    
    except Exception as err:
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})



@router.post('/students/add/')
def add_student(payload:schemas.NewStudent, db = Depends(db.db_session)):
    """
    **API Endpoint for adding new students**

    *This endpoint can be used to add new student details to the database*
    
    """
    try:
                
        chk_user  = select(models.Student).filter(models.Student.roll_number == payload.roll_number, models.Student.std == payload.std)
        chk_user = db.scalars(chk_user).first()

        if chk_user:
            db.close()
            return JSONResponse(status_code=400, content={"detail":"student already exists"})
        


        new_student = models.Student()
        new_student.name = payload.name
        new_student.std = payload.std
        new_student.roll_number = payload.roll_number
        
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        db.close()
        return JSONResponse(status_code=201, content={"detail":"student has been added", "student_id":new_student.id})
    
    except Exception as err:
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})



@router.delete('/students/delete/')
def remove_student(student_id:int, db = Depends(db.db_session)):
    """
    **API Endpoint for deleting existing students**

    *This endpoint can be used to delete existing student details to the database*
    
    """
    try:
        
        chk_student = db.get(models.Student, student_id)

        if not chk_student:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"invalid student_id"})

        
        
        db.delete(chk_student)
        db.commit()
        db.close()
        return JSONResponse(status_code=203, content={"detail":"student has been deleted"})
    
    except Exception as err:
        print_exc()
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})



@router.patch('students/update/')
def update_student(student_id:int, payload:schemas.UpdateStudent, db = Depends(db.db_session)):
    """
    **API Endpoint for updating students details**

    *This endpoint can be used to update existing student details to the database*
    
    """
    try:
        
        
        chk_student = db.get(models.Student, student_id)

        if not chk_student:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"invalid student_id"})
        
        if payload.roll_number and payload.std:
            chk_user  = select(models.Student).filter(models.Student.roll_number == payload.roll_number, models.Student.std == payload.std)
            chk_user = db.scalars(chk_user).first()

            if chk_user:
                db.close()
                return JSONResponse(status_code=400, content={"detail":"student already exists"})
        
        payload = dict(payload)

        for key in payload:
            if payload[key]:
                setattr(chk_student, key, payload[key])
        
        
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={"detail":"student has been updated"})
    
    except Exception as err:
        print_exc()
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})



@router.post('/students/subject/add/')
def add_subject(student_id:int, subject_id:int, db = Depends(db.db_session)):
    """
    **API Endpoint for adding subjects to specific student**

    *This endpoint can be used to add new subject to a specific student in database*
    
    """
    try:
        
        chk_student = db.get(models.Student, student_id)

        if not chk_student:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"invalid student_id"})

        chk_subject = db.get(models.Subject, subject_id)

        if not chk_subject:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"invalid subject_id"})
        
        new_subject_add = models.StudentSubject(students_id=student_id, subject_id=subject_id)
        db.add(new_subject_add)
        db.commit()
        db.close()
        return JSONResponse(status_code=201, content={"detail":"subject has been assigned"})
    
    except Exception as err:
        print_exc()
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})
    


@router.get('/subjects/all/')
def get_subjects(db = Depends(db.db_session)):
    """
    **API Endpoint to get all present subjects**

    *This endpoint can be used to get all present subjects from database*
    
    """
    try:
                
        db_subjects  = select(models.Subject)
        db_subjects = db.scalars(db_subjects).unique().all()

        if db_subjects == []:
            db.close()
            return JSONResponse(status_code=404, content={"detail":"no subjects found"})
        
        db.close()
        return {"data":db_subjects}
    
    except Exception as err:
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})



@router.post('/subjects/add/')
def add_subjects(payload:schemas.NewSubject ,db = Depends(db.db_session)):
    """
    **API Endpoint to add new subjects**

    *This endpoint can be used to add new subject in database*
    
    """
    try:
        sub_name = payload.subject[0].upper()+payload.subject[1:].lower()
        chk_subject  = select(models.Subject).filter(models.Subject.subject == sub_name)
        chk_subject = db.scalars(chk_subject).first()

        if chk_subject:
            db.close()
            return JSONResponse(status_code=400, content={"detail":"subject already exists"})
        


        new_subject = models.Subject()
        new_subject.subject = sub_name
        
        
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
        db.close()
        return JSONResponse(status_code=201, content={"detail":"subject has been added", "subject_id":new_subject.id})
      
    except Exception as err:
        db.rollback()
        db.close()    
        return JSONResponse(status_code=400, content={"detail":str(err)})

