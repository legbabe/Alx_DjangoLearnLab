from django.shortcuts import render, redirect
from .models import Book
from .forms import ExampleForm  # Import the form

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect after successful form submission
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})
