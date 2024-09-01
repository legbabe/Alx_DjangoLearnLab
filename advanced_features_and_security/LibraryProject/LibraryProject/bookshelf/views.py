from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm  # Import the form

@permission_required('bookshelf.can_add_book', raise_exception=True)
def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list') 
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})
