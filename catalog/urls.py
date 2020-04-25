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
]