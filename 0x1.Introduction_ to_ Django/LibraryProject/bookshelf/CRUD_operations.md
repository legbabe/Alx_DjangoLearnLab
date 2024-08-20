# CRUD Operations Documentation

## Create Operation
### Command:

from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

    # Output
    # <1984 by George Orwell, 1949>


## Retrieve Operation
retrieved_book = Book.objects.get(title = "1984")
print(retrieved_book.title, retrieved_book.author, retrieved_book.publication_year)

    # Output
    # <1984 by George Orwell, 1949>


## Update Operation
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)

     # Output
    # <Nineteen Eighty-Four by George Orwell, 1949>


## Delete Operation
from bookshelf.models import Book

# Delete the book
book.delete()

# Try to retrieve all books
books = Book.objects.all()
print(books)

