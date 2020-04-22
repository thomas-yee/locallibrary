from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language
#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

class BooksInline(admin.TabularInline):
    model = Book

# Define the admin class
class AuthorAdmin (admin.ModelAdmin):
    # Used to display the data in a certain way
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    # used to change how the fields on the form are displayed
    # tuple will display it horizontally
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]
    
admin.site.register(Author, AuthorAdmin)

# Used to add associated records at the same time
# this will book instance informaiton inline to our book detail
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Register the admin classes for Book using the decorator
# Does the same thing as admin.site.register()
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # can't specify the genre field since ManyToManyField would be too large
    # 'display_genre' is a call to the function in book class
    list_display = ('title', 'author', 'display_genre')
    # add the inline class
    inlines = [BooksInstanceInline]
    

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')

    # Used to filter which items are displayed
    list_filter = ('status', 'due_back')

    # Used to add sections within the detail form (Group related model information)
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )