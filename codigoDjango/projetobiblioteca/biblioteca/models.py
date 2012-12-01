from django.db import models
from django.utils import timezone

from sets import Set

# Create your models here.
class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=40)

    def __unicode__(self):
        return self.login

class Book(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField()
    purchased = models.BooleanField()
    #subject = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title
    
class Writer(models.Model):
    name = models.CharField(max_length=100)
    book = models.ForeignKey(Book)

    def __unicode__(self):
        return self.name + ' wrote \'' + self.book.title + '\''

class Suggestion(models.Model):
    date = models.DateTimeField()
    book = models.ForeignKey(Book)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name + ' suggests ' + str(self.amount) + ' volumes of \'' + self.book.title + '\''

def addSuggestion(request):
    #book
    book = Book(title=request.POST['titulo'], year=request.POST['ano'], publisher=request.POST['editora'], edition=request.POST['edicao'], purchased=False)
    book.save()
    
    #writer
    writer = Writer(name=request.POST['escritor'], book=book)
    writer.save()
    
    #suggestion
    processed_comment = processTextArea(request.POST['comentario'])
    suggestion = Suggestion(date=timezone.now(), book=book, name=request.POST['nome'], email=request.POST['email'], amount=request.POST['quantidade'], comment=processed_comment)
    suggestion.save()

def searchSuggestion(value):
    words_list = value.split('\\s')
    book_id_set = Set([])

    #Writer table###################################
    #writer.name
    
    writers = Writer.objects.filter(name__icontains=words_list[0])
    for word in words_list[1:]:
        writers = writers.filter(name__icontains=word)

    for w in writers:
        book_writer = w.book
        book_id_set.add(book_writer.pk)
    
    #Book table######################################
    #book.title

    book_titles = Book.objects.filter(title__icontains=words_list[0])
    for word in words_list[1:]:
        book_titles = book_titles.filter(title__icontains=word)

    for b in book_titles:
        book_id_set.add(b.pk)

    #book.year is integer...

    #book.publisher

    book_publisher = Book.objects.filter(publisher__icontains=words_list[0])
    for word in words_list[1:]:
        book_publisher = book_publisher.filter(publisher__icontains=word)

    for b in book_publisher:
        book_id_set.add(b.pk)

    
    #book.edition is integer...

    #Get books from id set (and their corresponding suggestions)
    books_match = Book.objects.filter(pk__in=book_id_set)
    suggestions_match = Suggestion.objects.filter(book__in=book_id_set)

    #Order books by title
    books_match = books_match.order_by('title')
    suggestions_match = suggestions_match.order_by('book__title')

    books_grouping_by_title = [] #lista de lista
    suggestion_grouping_by_book_title = []

    #Group books by title
    count = 0
    while len(books_match) > count:
        #Create a group with current title
        goup_list_books = [books_match[count]]
        goup_list_suggestions = [suggestions_match[count]]
        
        current_title = books_match[count].title
        count = count + 1
        
        while len(books_match) > count and books_match[count].title == current_title:
            #Group until found a different title
            goup_list_books.append(books_match[count])
            goup_list_suggestions.append(suggestions_match[count])
            count = count + 1
            
        books_grouping_by_title.append(goup_list_books)
        suggestion_grouping_by_book_title.append(goup_list_suggestions)
        
        
    #Suggestion table###############################
    #suggestion.name
    #suggestion_name = Suggestion.objects.filter(name__icontains=value)
    #for s in suggestion_name:
    #    book_id_set.add(s.book.pk)

    #suggestion.email
    #suggestion_email = Suggestion.objects.filter(email__icontains=value)
    #for s in suggestion_email:
    #    book_id_set.add(s.book.pk)

    #suggestion.comment
    #suggestion_comment = Suggestion.objects.filter(comment__icontains=value)
    #for s in suggestion_comment:
    #    book_id_set.add(s.book.pk)

    #From book_id_set, we get the Book objects and their corresponding Suggestion's
    #books_match = []
    #suggestions_match = []
    #for book_id in book_id_set:
    #    books_match.append(Book.objects.get(pk=book_id))
    #    suggestions_match.extend(Suggestion.objects.filter(book__exact=book_id))

    #x = z #DEBUG!

    return books_grouping_by_title, suggestion_grouping_by_book_title

def processTextArea(comment):
    lines = comment.split('\r\n') #['line1', '', '', 'line4', 'line5']

    while '' in lines:#remove empty lines -> ['line1', 'line4', 'line5']
        lines.remove('')

    return '#'.join(lines)#join elements -> 'line1#line4#line5'