from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User #used to import the user model
from datetime import date

# Create your models here.
# Genre Model
class Genre (models.Model):
    """Model representing a book genre."""
    # ---- Fields ----    
    name = models.CharField(max_length=200, help_text = 'Enter a book genre (e.g. Science Fiction)')

    # ---- Methods ----
    def __str__ (self):
        """String for representing the Model object."""
        # Returns the name of the genre
        return self.name

class Language (models.Model):
    """Model representing a language"""
    # ---- Fields ----
    name = models.CharField(max_length=200, help_text = 'Enter a language for the book (e.g. French)')

    # ---- Methods ----
    def __str__ (self):
        return self.name

# Book Model
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)"""
    # ---- Fields ----
    title = models.CharField(max_length=200, help_text = "Title of the book")
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    # null = True -> allows database to store a null value if no author is selected
    # on_delete -> set the value of author to NULL if the associated author record is deleted
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null = True)
    summary = models.TextField(max_length=1000, help_text = 'Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null = True)
    
    # ---- Methods ----
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    # Returns a URL that can be used to access a detail record for this model
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin.
            Only shows the first three values of genre."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    # ---- Fields ----
    # UUIDField used to set id as primary key - Allocates a global unique value for each instance
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200, help_text = "Publishing Company")
    due_back = models.DateField(null=True, blank=True, help_text = 'The date the book is due')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Key-pair values - Value is a display value the user can select
    # Keys are the values that are actually saved if it selected
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = 'Book availability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    # Will be sorted alphabetically by due_back
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    # ---- Methods ----
    def __str__ (self):
        """String for representing the Model Object."""
        return f'{self.id} ({self.book.title})'

class Author (models.Model):
    """Model representing an author."""
    # --- Fields ---
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null = True, blank = True)

    # Will be sorted alphabetically by last name and then first name
    class Meta:
        ordering = ['last_name', 'first_name']

    # ---- Methods ----
    # reverses the author-detail URL mapping to get the URL for displaying an individual author
    def get_absolute_url (self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__ (self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'