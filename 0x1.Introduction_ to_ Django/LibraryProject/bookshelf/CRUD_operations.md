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
retrieved_book = Book.objects.get(id=book.id)
print(retrieved_book)

    # Output
    # <1984 by George Orwell, 1949>


## Update Operation
retrieved_book.title = "Nineteen Eighty-Four"
retrieved_book.save()

print(retrieved_book)

     # Output
    # <Nineteen Eighty-Four by George Orwell, 1949>


## Delete Operation
retrieved_book.delete()

# Verify deletion by trying to retrieve all books
all_books = Book.objects.all()
print(list(all_books))

