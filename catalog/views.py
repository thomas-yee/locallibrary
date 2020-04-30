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

# Used to add the view of list of books loaned to the current user
# This import allows only the logged in user to call this view
from django.contrib.auth.mixins import LoginRequiredMixin
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    # May have different lists of BookInstance records with different views and templates
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    # Restrict query to just BookInstance objects for the current user
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back') 

# Used to add the view of list of all books loaned
# Allows only those with permission to call this view
from django.contrib.auth.mixins import PermissionRequiredMixin
class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """"Generic class-based view listing all books on loan. Can only be viewed
    with the can_edit permission """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# The view for the form when a librarian is renewing a book
import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404 # Raises exception if the record isn't found
from django.http import HttpResponseRedirect # Creates redirect to a specified URL
from django.urls import reverse

# from .forms import RenewBookForm
from catalog.forms import RenewBookForm

# Function decorator
@permission_required('catalog.can_mark_returned')
# pk argument in get_object_or_404() to get the current BookSInstance
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    # Contains our BookInstance
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    
    # Render creates the HTML page
    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

# Need to derive from CreateView in order to create, update, or delete the view
class AuthorCreate(CreateView):
    model = Author
    # Used to specify the fields to display in the form
    fields = '__all__'
    # Specifies initial values for each of the fields
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    # Redirects to the author list after an author has been deleated
    success_url = reverse_lazy('authors')