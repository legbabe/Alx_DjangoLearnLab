from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
 


class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_staff')
    # Fields to display in the detailed view
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    # Search fields for the user list view
    search_fields = ('username', 'email')
    # Filter options in the list view
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_of_birth')

admin.site.register(CustomUser, CustomUserAdmin)
