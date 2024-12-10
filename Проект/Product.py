import datetime


class Book:
    def __init__(self, name: str, author: str, publisher: str,
                 date_of_write: datetime.date, date_of_publish: datetime.date, genre: str, price: int, tirage=0 ):
        self.name = name
        self.author = author
        self.publisher = publisher
        self.date_of_write = date_of_write
        self.date_of_publish = date_of_publish
        self.genre = genre
        self.price = price
        self.tirage = tirage

    def sell(self, count: int):
        if self.tirage >= count:
            self.tirage -= count
            return True
        else:
            return False

    def buy(self, count: int):
        self.tirage += count
