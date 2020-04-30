from django.urls import path
from . import views

# URL pattern is an empty string
# view function that will be called if the URL pattern is detected : views.index()
urlpatterns = [
    path('', views.index, name='index'),
    # as_view() function used to create an instance of the class
    path('books/', views.BookListView.as_view(), name='books'), 
    # <> define the part of the URL to be captured, enclosing the name of the variable
    # that the view can use to access the captured data
    # <something> capture the pattern and pass the value to the view as a variable something
    # can precede the variable name with a converter specification like int, str, path
    # pk (short for primary key) - id that is being used to store the book uniquely
    path('book/<int:pk>', views.BookDetailView.as_view(), name ='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name = 'authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name = 'renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]