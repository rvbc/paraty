﻿from django.db import models

from sets import Set
from xlwt import Workbook, easyxf

from tempfile import TemporaryFile

import datetime

import unicodedata

from django.http import HttpResponse

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

# Create your models here.
class User(models.Model):
    login = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=40)

    def __unicode__(self):
        return self.login

class Book(models.Model):
    isbn = models.CharField(max_length=13,primary_key=True)
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField()
    purchased = models.BooleanField()
    search = models.CharField(max_length=1000)
	
    def __unicode__(self):
        return self.title

    def run_query(name):
        Book.objects.filter(search__icontains=name)
    
class Writer(models.Model):
    name = models.CharField(max_length=100)
    book = models.ForeignKey(Book)
    search = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' wrote \'' + self.book.title + '\''

    def run_query(name):
        Writer.objects.filter(search__icontains=name)

class Suggestion(models.Model):
    date = models.DateTimeField()
    book = models.ForeignKey(Book)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    search = models.CharField(max_length=1000)
    course = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' suggests ' + str(self.amount) + ' volumes of \'' + self.book.title + '\''

    def run_query(name):
        Writer.objects.filter(search__icontains=name)

def addSuggestion(request, writers_list):
    #book
    s = request.POST['titulo'] + ' ' + request.POST['editora'] + ' ' + request.POST['isbn'] + ' ' + request.POST['ano']
    book = Book(title=request.POST['titulo'], year=request.POST['ano'], publisher=request.POST['editora'], edition=request.POST['edicao'], purchased=False, search=strip_accents(s), isbn=request.POST['isbn'])
    book.save()
    
    #writer
    for writer_name in writers_list:
        writer = Writer(name=writer_name, book=book, search=strip_accents(writer_name))
        writer.save()
    
    #suggestion
    processed_comment = processTextArea(request.POST['comentario'])
    s = processed_comment + ' ' + request.POST['nome'] + ' ' + request.POST['email'] + ' ' + request.POST['disciplina']
    suggestion = Suggestion(date=datetime.datetime.now(), book=book, name=request.POST['nome'], email=request.POST['email'], course=request.POST['disciplina'], amount=request.POST['quantidade'], comment=processed_comment, search=strip_accents(s))
    suggestion.save()


def searchBooks(value):
    words_list = value.split()
    words_list = words_list if len(words_list) > 0 else [u'']
    book_id_set = Set([])

    #Writer table###################################
    
    for word in words_list:
        writers = Writer.objects.filter(search__icontains=strip_accents(word))
        
        for w in writers:
            book_id_set.add(w.book.pk)
    
    #Book table######################################

    for word in words_list:
        book_titles = Book.objects.filter(search__icontains=strip_accents(word))
        
        for b in book_titles:
            book_id_set.add(b.pk)


    #Get books from id set (and their corresponding suggestions)
    #Order books by title
    books_match = Book.objects.filter(pk__in=book_id_set).order_by('title')

    suggestions_match = []
    writers_list_list = []
    for b in books_match:
        s = Suggestion.objects.filter(book=b.pk).order_by('-date')
        suggestions_match.append(s)

        writers_book = Writer.objects.filter(book=b.pk).order_by('name')
        writers_list_list.append(writers_book)

    return books_match, suggestions_match, writers_list_list


def processTextArea(comment):
    lines = comment.split('\r\n') #['line1', '', '', 'line4', 'line5']

    while '' in lines:#remove empty lines -> ['line1', 'line4', 'line5']
        lines.remove('')

    return '#'.join(lines)#join elements -> 'line1#line4#line5'


def exportWorkbook(query):
    books, suggestions, authors = searchBooks(query)
    book = Workbook(encoding='utf-8')
    sheet = book.add_sheet('Livros Sugeridos')
    #cols = [u'Título','Autores','Ano','Editora',u'Edição','Sugerido por','Email','Quantidade sugerida',u'Comentário'];
    cols = ['ITEM', 'QTD', 'AUTORES', u'TÍTULO', 'EDITORA', 'ISBN', u'EDIÇÃO', 'ANO', 'SUGERIDO POR', 'EMAIL', u'COMENTÁRIO']

    c = 0
    while len(cols) > c:
        sheet.write(0,c,cols[c])
        sheet.col(c).width = len(cols[c])*500
        c = c + 1

    #sheet.col(0).width = sheet.col(0).width * 2; #title
    #sheet.col(1).width = sheet.col(1).width * 2; #authors
    #sheet.col(6).width = sheet.col(6).width * 2; #email
    #sheet.col(7).width = sheet.col(7).width / 2; #amount
    #sheet.col(8).width = sheet.col(8).width * 4; #comment
    
    #sheet.col(0).width = sheet.col(1).width * 2; #amount
    sheet.col(2).width = sheet.col(2).width * 2; #authors
    sheet.col(3).width = sheet.col(3).width * 2; #title
    sheet.col(5).width = sheet.col(5).width * 3; #ISBN
    sheet.col(9).width = sheet.col(9).width * 2; #email
    sheet.col(10).width = sheet.col(10).width * 4; #comment

    c = 0
    item = 0
    while len(books) > item:
        #sheet.write(c+1,0,books[c].title)
        #authorStr = '';
        #for author in authors[c]:
        #    authorStr = authorStr + author.name + ', '
        #if len(authorStr) > 0:
        #    authorStr = authorStr[:-2]
        #
        #sheet.write(c+1,1,authorStr)
        #sheet.write(c+1,2,books[c].year)
        #sheet.write(c+1,3,books[c].publisher)
        #sheet.write(c+1,4,books[c].edition)
        #sheet.write(c+1,5,suggestions[c].name)
        #sheet.write(c+1,6,suggestions[c].email)
        #sheet.write(c+1,7,suggestions[c].amount)
        #sheet.write(c+1,8,suggestions[c].comment)
        
        sheet.write(c+1,0,item+1)
        sheet.write(c+1,1,suggestions[item].amount)
        

        sheet.write(c+1,3,books[item].title)
        sheet.write(c+1,4,books[item].publisher)
        sheet.write(c+1,5,books[item].isbn)
        sheet.write(c+1,6,books[item].edition)
        sheet.write(c+1,7,books[item].year)
        sheet.write(c+1,8,suggestions[item].name)
        sheet.write(c+1,9,suggestions[item].email)
        sheet.write(c+1,10,suggestions[item].comment)
        
        #authorStr = '';
        #for author in authors[c]:
        #    authorStr = authorStr + author.name + ', '
        #if len(authorStr) > 0:
        #    authorStr = authorStr[:-2]        
        #sheet.write(c+1,2,authorStr)

        initial_row = c+1
        authorStr = ''
        for author in authors[item]:
            authorStr = authorStr + author.name + '\n'
            #sheet.write(c+1,2,author.name)
            c = c + 1
        sheet.write_merge(r1=initial_row, c1=2, r2=c, c2=2, label=authorStr[:-1], style=easyxf('alignment: wrap True;'))



        c = c + 1
        item = item + 1

    now = datetime.datetime.now()
    name = strip_accents(query) + '_' + str(now.day) + '-' + str(now.month) + '-' + str(now.year) + '.xls'

    #book.save(name)
    
    book.save(TemporaryFile())

    return book, name

def xls_to_response(xls, fname):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response
