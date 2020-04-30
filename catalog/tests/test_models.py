from django.test import TestCase
from catalog.models import Author

# Create your tests here
class AuthorTestClass(TestCase):
    @classmethod
    # Called at the beginning of the test run for class-level setup
    # Used to create objects that aren't going to be modified or changed in the test methods
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name = 'Big', last_name = 'Bob')

    def test_first_name_label(self):
        # Get an author object to test
        author = Author.objects.get(id=1)
        # Get the metadata for the required field and use it to query the required field data
        # since author.first_name is a string
        field_label = author._meta.get_field('first_name').verbose_name
        # Compare the value to the expected result
        self.assertEquals(field_label, 'first name')

    # This test will fail since it was expecting the label definition to follow
    # Django's convention of not capitalising the first letter of the label
    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')