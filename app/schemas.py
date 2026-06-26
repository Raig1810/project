class Student():
    def __init__(self, id: int, name: str, group: str, average_score: float, is_active: bool = True):
        self.id = id
        self.name = name
        self.group = group
        self.average_score = average_score
        self.is_active = is_active
        