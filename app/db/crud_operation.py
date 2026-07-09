from app.db.database import engine, StudentModel, LocalSession

class CRUD():

    def create(self, name: str, group: str, average_score: float) -> StudentModel:
        if not name or name.strip() == "":
            raise ValueError("Ошибка: имя цне должно быть пустым")
        if average_score < 0 or average_score > 100:
            raise ValueError("Ошибка: средний балл должен находится в диапазоне от 0 до 100")
            
        with LocalSession() as session:
            new_student = StudentModel(
                name  = name,
                group = group,
                average_score = average_score
            )
            session.add(new_student)
            session.commit()
            session.refresh(new_student)

            return new_student
        
    def read(self, student_id: int) -> StudentModel:
        with LocalSession() as session:
            student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
            if not student or not student.is_active:
                raise ValueError(f"Ошибка: студент с ID {student_id} не найден или удален")
            
            return student
        
    def read_all(self, group_name: str = None) ->list[StudentModel]:
        with LocalSession() as session:
            search = session.query(StudentModel).filter(StudentModel.is_active == True)
            if group_name:
                search = search.filter(StudentModel.group == group_name)
                
            return search.all()
        
    def update(self, student_id: int, new_name: str = None, new_score: float = None) -> StudentModel:
        if new_name is not None:
            if new_name.strip() == "":
                raise ValueError("Ошибка: новое имя не может быть пустым")

        if new_score is not None:
            if new_score < 0 or new_score > 100:
                raise ValueError("Ошибка: новый балл должен быть находиться в диапазоне от 0 до 100")
        
        with LocalSession() as session:
            student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
            if not student or not student.is_active:
                raise ValueError(f"Ошибка: студент с ID {student_id} не найден или удален")
            if new_name is not None:
                student.name = new_name
            if new_score is not None:
                student.average_score = new_score

            session.commit()
            session.refresh(student)
            return student
        
    def delete(self, student_id: int) -> str:
        with LocalSession() as session:

            student = session.query(StudentModel).filter(StudentModel.id == student_id).first()
            if not student or not student.is_active:
                raise ValueError(f"Ошибка: студент с ID {student_id} не найден или удален")
            student.is_active = False
            session.commit()
            return f"Студент {student.name} удален"