import datetime
from Customer import Customer
from Product import Book
from WorkClass import Worker, Galya, Person


class WorkerBase:
    def __init__(self, filename: str):
        try:
            self.workers = []
            file = open(filename, 'r')
            count = int(file.readline())
            for i in range(count):
                details = file.readline().split()
                self.workers.append(Worker(int(details[0]), Person(details[1], details[2],
                                           datetime.date(int(details[3]), int(details[4]), int(details[5]))),
                                           datetime.date(int(details[6]), int(details[7]), int(details[8]))))
            file.close()
        except:
            self.workers = []

    def fire(self, worker: Worker):
        for x in self.workers:
            if worker.id == x.id:
                self.workers.remove(x)

    def hire(self, worker: Worker):
        for x in self.workers:
            if worker.id == x.id:
                return False
        self.workers.append(worker)

    def save(self, filename: str):
        file = open(filename, 'w')
        file.write(str(len(self.workers)))
        for x in self.workers:
            file.write(str(x.id)+' '+x.personal.first_name+' '+x.personal.last_name+' '+str(x.personal.date_of_birth.year) +
                       ' '+str(x.personal.date_of_birth.month)+' '+str(x.personal.date_of_birth.day)+' '+
                       str(x.date_of_hire.year)+' '+str(x.date_of_hire.month)+' '+str(x.date_of_hire.day))
        file.close()


class GalyaBase:
    def __init__(self, filename: str):
        try:
            self.workers = []
            file = open(filename, 'r')
            count = int(file.readline())
            for i in range(count):
                details = file.readline().split()
                self.workers.append(Galya(Worker(int(details[0]), Person(details[1], details[2],
                                           datetime.date(int(details[3]), int(details[4]), int(details[5]))),
                                           datetime.date(int(details[6]), int(details[7]), int(details[8]))),
                                    datetime.date(int(details[9]), int(details[10]), int(details[11]))))
            file.close()
        except:
            self.workers = []

    def fire(self, galya: Galya):
        for x in self.workers:
            if galya.id == x.id:
                self.workers.remove(x)

    def hire(self, galya: Galya):
        for x in self.workers:
            if galya.id == x.id:
                return False
        self.workers.append(galya)

    def save(self, filename):
        file = open(filename, 'w')
        file.write(str(len(self.workers)))
        for x in self.workers:
            file.write(str(x.id)+' '+x.personal.first_name+' '+x.personal.last_name+' '+str(x.personal.date_of_birth.year)+' '+
                       str(x.personal.date_of_birth.month)+' '+str(x.personal.date_of_birth.day)+' '+str(x.date_of_hire.year)+ ' '+
                       str(x.date_of_hire.month)+' '+str(x.date_of_hire.day)+' '+str(x.date_of_rising.year)+' '+
                       str(x.date_of_rising.month)+' '+str(x.date_of_rising.day))


class BookBase:
    def __init__(self, filename):
        try:
            self.books = []
            file = open(filename, 'r')
            count = int(file.readline())
            for i in range(count):
                details = file.readline().split()
                self.books.append(Book(details[0], details[1], details[2],
                                       datetime.date(int(details[3]), int(details[4]), int(details[5])),
                                       datetime.date(int(details[6]), int(details[7]), int(details[8])),
                                       details[9], int(details[10]), int(details[11])))
            file.close()
        except:
            self.books = []

    def save(self,filename):
        file = open(filename, 'w')
        file.write(str(len(self.books)))
        for x in self.books:
            file.write(x.name+' '+x.author+' '+x.publisher+' '+str(x.date_of_write.year)+' '+str(x.date_of_write.month)+' '+
                       str(x.date_of_write.day)+' '+str(x.date_of_publish.year)+' '+str(x.date_of_publish.month)+' '+
                       str(x.date_of_publish.day)+' '+x.genre+' '+str(x.price)+' '+str(x.tirage))


class CustomerBase:
    def __init__(self, filename):
        try:
            self.customers = []
            file = open(filename, 'r')
            count = int(file.readline())
            for i in range(count):
                details = file.readline().split()
                self.customers.append(Customer(int(details[0]), details[1], datetime.date(int(details[2]), int(details[3]),
                                                int(details[4])), datetime.date(int(details[5]), int(details[6]),
                                                int(details[7])), int(details[8])))
                file.close()
        except:
            self.customers = []

    def save(self, filename):
        file = open(filename, 'w')
        file.write(str(len(self.customers)))
        for x in self.customers:
            file.write(str(x.id)+' '+x.name+' '+str(x.date_of_birth.year)+' '+str(x.date_of_birth.month)+' '+
                       str(x.date_of_birth.day)+' '+str(x.date_of_carding.year)+' '+str(x.date_of_carding.month)+' '+
                       str(x.date_of_carding.day)+' '+str(x.points))





