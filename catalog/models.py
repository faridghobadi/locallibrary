from django.db import models
from django.urls import reverse
import uuid

class Genre(models.Model) :
    genre_type = models.CharField(max_length=200, help_text="enter a genre for book.")

    def __str__(self):
        return self.genre_type

class Author(models.Model) :
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' %(self.last_name, self.first_name)

class Book(models.Model) :
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="enter a description for this book.")
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre, help_text="select a genre for this book.")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for the book.")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    loan_state = (
        ('m' , 'Maintenance'),
        ('o' , 'On loan'),
        ('a' , 'Available'),
        ('r' , 'Reserved')
    )

    status = models.CharField(max_length=1, choices=loan_state, default='m', help_text="book status")
    class Meta :
        ordering = ["due_back"]

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)

