#question 9
# HomeWork - 0
#Dr.Voigt - Yousef Jarrar, Nicholas Chiodini


class Book:
    def __init__(self, title, year, page):
        self.title = title
        self.year = year
        self.page = page

book = Book("Intro To Artificial Intelligence", 2009, 756)
print("Title: ",book.title)
print("Year: ",book.year)
print("Pages: ",book.page)
