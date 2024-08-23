from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Library, Book 
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, permission_required
from forms import BookForm

# Create your views here.
def book_list_view(request):
    """Retrieves all books and renders a template displaying the list."""
    books = Book.objects.all()  # Fetch all book instances from the database
    context = {'book_list': books}  # Create a context dictionary with book list
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetails_view(DetailView):
    """A class-based view for displaying details of a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        """Injects additional context data specific to the library."""
        context = super().get_context_data(**kwargs)  # Get default context data
        library = self.get_object()  # Retrieve the current library instance
        context['average_rating'] = library.get_average_rating() 

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "relationship_app/register.html"

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

def check_role(user, role):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role

# Admin view
@user_passes_test(lambda user: check_role(user, 'Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view
@user_passes_test(lambda user: check_role(user, 'Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view
@user_passes_test(lambda user: check_role(user, 'Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Add book view
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

# Edit book view
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})

# Delete book view
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})