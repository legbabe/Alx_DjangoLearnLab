## Retrieve the Book Instance

### Command:
```python
# Retrieve the created book
retrieved_book = Book.objects.get(id=book.id)
print(retrieved_book)
