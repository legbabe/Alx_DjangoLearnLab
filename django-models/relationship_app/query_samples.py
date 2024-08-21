from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)  # Filtering books by the author instance
        return books
    except Author.DoesNotExist:
        return f"Author '{author_name}' does not exist."

def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using related_name 'libraries' to access related Book objects
        return books
    except Library.DoesNotExist:
        return f"Library '{library_name}' does not exist."

def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # Get the librarian by filtering on the library
        return librarian
    except Library.DoesNotExist:
        return f"Library '{library_name}' does not exist."
    except Librarian.DoesNotExist:
        return f"No librarian found for the library '{library_name}'."

# Sample usage:
# if __name__ == "__main__":
#     # Query all books by an author
#     author_name = "J.K. Rowling"
#     books_by_author = query_books_by_author(author_name)
#     print(f"Books by {author_name}:")
#     if isinstance(books_by_author, list):
#         for book in books_by_author:
#             print(f"- {book.title}")
#     else:
#         print(books_by_author)

#     # List all books in a library
#     library_name = "Central Library"
#     books_in_library = list_books_in_library(library_name)
#     print(f"\nBooks in {library_name}:")
#     if isinstance(books_in_library, list):
#         for book in books_in_library:
#             print(f"- {book.title}")
#     else:
#         print(books_in_library)

#     # Get the librarian for a library
#     librarian = get_librarian_for_library(library_name)
#     if isinstance(librarian, Librarian):
#         print(f"\nLibrarian for {library_name}: {librarian.name}")
#     else:
#         print(librarian)
