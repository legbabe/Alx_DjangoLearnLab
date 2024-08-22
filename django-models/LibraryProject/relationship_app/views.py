from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """
    A class-based view that displays details of a specific library,
    listing all books available in that library.
    """
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'