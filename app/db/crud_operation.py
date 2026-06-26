from app.schemas import Student

class CRUD():
    def __init__(self):
        self.db = {}
        self.current_id = 1

    def create(self, name: str, group: str, average_score: float):
        if not name or name.strip() == "":
            raise ValueError("Ошибка: имя цне должно быть пустым")
        if average_score < 0 or average_score > 100:
            raise ValueError("Ошибка: средний балл должен находится в диапазоне от 0 до 100")
        
        new_student = Student(
            id = self.current_id,
            name  = name,
            group = group,
            average_score = average_score
        )
        self.db[self.currnet_id] = new_student
        self.current_id += 1

        return new_student
    
    def read(self, student_id: int):
        if student_id not in self.db:
            raise ValueError(f"Ошибка: Студент с ID {student_id} не найден")
        student = self.db[student_id]
        if not student.is_active:
            raise ValueError(f"Ошибка: Студент с ID {student_id} удален")
        
        return student
    
    def update(self, student_id: int, new_name: str = None, new_score: float = None,):
        student = self.read(student_id)

        if new_name is not None:
            if new_name.strip() == "":
                raise ValueError("Ошибка: новое имя не может быть пустым")
            student.name = new_name

        if new_score is not None:
            if new_score < 0 or new_score > 100:
                raise ValueError("Ошибка: новый балл должен быть находиться в диапазоне от 0 до 100")
            student.average_score = new_score
            
        return student
    
    def delete(self, student_id: int):
        student = self.read(student_id)
        student.is_active = False
        return f"Студент {student.name} удален"