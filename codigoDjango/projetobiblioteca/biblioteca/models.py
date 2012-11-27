from django.db import models
from django.utils import timezone

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

def processTextArea(comment):
    lines = comment.split('\r\n') #['line1', '', '', 'line4', 'line5']

    while '' in lines:#remove empty lines -> ['line1', 'line4', 'line5']
        lines.remove('')

    return '#'.join(lines)#join elements -> 'line1#line4#line5'