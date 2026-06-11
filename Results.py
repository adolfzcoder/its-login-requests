from Module import Module


class Results:
    def __init__(self, student_name: str | None, student_number: str | None, modules: list[Module]):
        self.student_name = student_name
        self.student_number = student_number
        self.modules = modules

    def to_dict(self):
        return {
            "student_name": self.student_name,
            "student_number": self.student_number,
            "results": [module.to_dict() for module in self.modules],
        }