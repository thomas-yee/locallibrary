from django.shortcuts import render
# import the model classes in order to access the data
from catalog.models import Book, Author, BookInstance, Genre
# import the generic list view
from django.views import generic

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

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0) # Sets to 0 if not previously been set
    # Each time a request is received, increment the value and store it back in session
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_game': num_books_game,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    # request - HttpRequest, index.html --> html template wtih placeholders for the data
    # index.html expected to be found in catalog/templates/
    # context - python dictionary containing the data to insert into the placeholders
    return render(request, 'index.html', context=context)

# use a class-based generic list view (ListView) - a class that inherits from an existing view
class BookListView(generic.ListView):
    """The generic view will query the database to get all records for the
    specific model (Book) and render a template"""
    model = Book
    # your own name for the list as a template variable
    #context_object_name = 'my_book_list'
    # Get 5 books containing the title
    #queryset = Book.objects.filter(title__icontains='silent')[:5]
    # Adds pagination to the list views, reducing number of items displayed on each page
    paginate_by = 4
    
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4

class AuthorDetailView(generic.DetailView):
    model = Author