import datetime


class Person:
    def __init__(self, first_name: str, last_name: str, date_of_birth: datetime.date):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth


class Worker:
    def __init__(self, id: int, personal: Person, date_of_hire=datetime.date.today()):
        self.id = id
        self.personal = personal
        self.date_of_hire = date_of_hire


class Galya:
    def __init__(self, worker: Worker, date_of_rising=datetime.date.today()):
        self.id = worker.id
        self.personal = worker.personal
        self.date_of_hire = worker.date_of_hire
        self.date_of_rising = date_of_rising


