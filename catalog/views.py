from django.shortcuts import render
# import the model classes in order to access the data
from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.
# Used to process an HTTP request, fetch data from the database, and render
# the data in an HTML page


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    num_books_game = Book.objects.filter(title__contains='game').count()
    num_genres = Genre.objects.all().count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_game': num_books_game,
        'num_genres': num_genres
    }

    # Render the HTML template index.html with the data in the context variable
    # request - HttpRequest, index.html --> html template wtih placeholders for the data
    # index.html expected to be found in catalog/templates/
    # context - python dictionary containing the data to insert into the placeholders
    return render(request, 'index.html', context=context)