class LibraryItem:
    def __init__(self,title,item_id,pages):
        self.title = title
        self.item_id = item_id
        self.pages = pages
    def __str__(self):
        return f'{self.title} (ID: {self.item_id}), страниц: {self.pages}'
    def __lt__(self,other):
        return self.pages < other.pages
    def __eq__(self,other):
        try:
            return self.pages == other.pages
        except:
            return 'NotImplemented'
    
    def __add__(self,other):


class Book(LibraryItem):
    def __init__(self,title,item_id,pages,author):
        super().__init__(title,item_id,pages)
        self.author = author
    def __str__(self):
        return f'{self.title} от {self.author} (ID: {self.item_id}), страниц: {self.pages}'
    def __add__(self, other):
        if not isinstance(other, Book):
            raise ValueError("Можно складывать только книги")

        if self.author != other.author:
            raise ValueError("Авторы должны совпадать")

        new_title = f"{self.title} и {other.title}"
        new_pages = self.pages + other.pages

        return Book(new_title, "new_id", new_pages, self.author)
    
book1 = Book("Harry Potter",'2012',400,'rowling')
book2 = Book("Holy Bible",'555',300,'someone')
print(book1 == book2)