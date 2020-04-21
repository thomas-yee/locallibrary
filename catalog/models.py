from django.db import models

# Create your models here.
# Genre Model
class Genre (models.Model):
    """Model representing a book genre."""
# ---- Fields ----    
    name = models.CharField(max_length=200, help_text = 'Enter a book genre (e.g. Science Fiction)')

# ---- Methods -----
def __str__ (self):
    """String for representing the Model object."""
    # Returns the name of the genre
    return self.name