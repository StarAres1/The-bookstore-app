import datetime


class Customer:
    def __init__(self, id: int, name: str, date_of_birth: datetime.date, points=0, date_of_carding=datetime.date.today()):
        self.id = id
        self.name = name
        self.date_of_birth = date_of_birth
        self.date_of_carding = date_of_carding
        self.points = points

    def pay_by_points(self):
        pay = self.points
        self.points = 0
        return pay

    def add_points(self, points: int):
        self.points += points

