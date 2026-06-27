import json
from app.schemas import Student

class CRUD():
    def __init__(self, db_path: str = "data/students.json"):
        self.db_path = db_path
        self.db = {}
        self.current_id = 1
        self._load_data()

    def _load_data(self):        
        try:
            with open(self.db_path, "r", encoding = "utf-8") as file:
                data = json.load(file)
                for k, v in data.items():
                    self.db[int(k)] = Student(**v)
                if self.db:
                    self.current_id = max(self.db.keys()) + 1
        except FileNotFoundError:
            pass
                    
    def _save_data(self):
        try:
            data_to_save = {str(k): v.__dict__ for k, v in self.db.items()}
            with open(self.db_path, "w", encoding = "utf-8") as file:
                json.dump(data_to_save, file, ensure_ascii = False, indent = 4)
        except Exception as error:
            print("Ошибка при сохранении файла")

    def create(self, name: str, group: str, average_score: float) -> Student:
        if not name or name.strip() == "":
            raise ValueError("Ошибка: имя не должно быть пустым")
        if average_score < 0 or average_score > 100:
            raise ValueError("Ошибка: средний балл должен находится в диапазоне от 0 до 100")
        
        new_student = Student(
            id = self.current_id,
            name  = name,
            group = group,
            average_score = average_score
        )
        self.db[self.current_id] = new_student
        self.current_id += 1

        self._save_data()
        return new_student
    
    def read(self, student_id: int) -> Student:
        if student_id not in self.db:
            raise ValueError(f"Ошибка: Студент с ID {student_id} не найден")
        student = self.db[student_id]
        if not student.is_active:
            raise ValueError(f"Ошибка: Студент с ID {student_id} удален")
        
        return student
    
    def update(self, student_id: int, new_name: str = None, new_score: float = None,) -> Student:
        student = self.read(student_id)

        if new_name is not None:
            if new_name.strip() == "":
                raise ValueError("Ошибка: новое имя не может быть пустым")
            student.name = new_name

        if new_score is not None:
            if new_score < 0 or new_score > 100:
                raise ValueError("Ошибка: новый балл должен находиться в диапазоне от 0 до 100")
            student.average_score = new_score
            
        self._save_data()
        return student
    
    def delete(self, student_id: int) -> str:
        student = self.read(student_id)
        student.is_active = False
        self._save_data()
        return f"Студент {student.name} удален"