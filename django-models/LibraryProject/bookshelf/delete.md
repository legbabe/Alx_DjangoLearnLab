## Delete the Book Instance

### Command:
```python
from bookshelf.models import Book

# Delete the book
book.delete()

# Try to retrieve all books
books = Book.objects.all()
print(books)

