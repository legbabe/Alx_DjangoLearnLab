## Delete the Book Instance

### Command:
```python
# Delete the book
retrieved_book.delete()

# Verify deletion by trying to retrieve all books
all_books = Book.objects.all()
print(list(all_books))
