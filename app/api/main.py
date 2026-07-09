from fastapi import FastAPI, HTTPException
from typing import Optional
from loguru import logger
from app.db.crud_operation import CRUD
from app.schemas.schemas import StudentCreate, StudentUpdate

app = FastAPI()

db = CRUD()

logger.add("app.log", format="{time} | {level} | {message}")

@app.on_event("startup")
def startup_event():
    logger.info(f"Запуск сервиса")

@app.get("/")
def read_root():
    return {"message": "База данных студентов"}

@app.get("/health", summary="Проверка работоспособности сервиса")
def health_check():
    return {"status": "ok", "message": "Сервер работает стабильно"}

@app.post("/create", summary="Создание новой записи")
def create_student(student: StudentCreate):
    try:
        new_student = db.create(
            name=student.name, 
            group=student.group, 
            average_score=student.average_score
            )
        logger.info(f"Создание записи: добавлен студент {new_student.name} (id: {new_student.id})")
        return {"message": "Запись добавлена в базу данных", "student_id": new_student.id}
    except ValueError as error:
        logger.error(f"Ошибка при создании записи: {error}")
        raise HTTPException(status_code=400, detail=str(error)) 

@app.get("/read", summary="Получение записи или списка записей")
def read_student(student_id: Optional[int] = None, group: Optional[str] = None):
    try:
        if student_id is not None:
            return db.read(student_id)
        return db.read_all(group_name=group)
    except ValueError as error:
        logger.error(f"Ошибка получения записи: {error}")
        raise HTTPException(status_code=404, detail=str(error))

@app.put("/update/{student_id}", summary="Изменение существующей записи")
def update_student(student_id: int, student_data: StudentUpdate):
    try:
        updated_student = db.update(
            student_id=student_id, 
            new_name=student_data.new_name, 
            new_score=student_data.new_score
            )
        logger.info(f"Изменение записи: обновлен студент с id {student_id}")
        return {"message": "Запись изменена"}
    except ValueError as error:
        logger.error(f"Ошибка изменения записи: {error}")
        raise HTTPException(status_code=400, detail=str(error))

@app.delete("/delete/{student_id}", summary="Удаление записи")
def delete_student(student_id: int):
    try:
        message = db.delete(student_id)
        logger.info(f"Удаление записи: {message}")
        return {"status": "success", "message": message}
    except ValueError as error:
        logger.error(f"Ошибка удаления записи: {error}")
        raise HTTPException(status_code=404, detail=str(error))