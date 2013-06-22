#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from search.core import search
from sets import Set
from tempfile import TemporaryFile
from xlwt import Workbook, easyxf

import bisect
import datetime
import unicodedata

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
    course = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' suggests ' + str(self.amount) + ' volumes of \'' + self.book.title + '\''

class BookView:
    book = Book()
    writers = []
    suggestions = []
    total_amount = 0

    def __init__(self, book, writers, suggestions, amount):
        self.book = book
        self.suggestions = suggestions
        self.writers = writers
        self.total_amount = amount

def addSuggestion(request, writers_list):
    isbn_field = request.POST['isbn']
    
    #If there is a book with isbn, then dont add book and writers again.
    book = []
    try:
        book = Book.objects.get(pk=isbn_field)
    except ObjectDoesNotExist:
        
        #book
        book = Book(title=request.POST['titulo'], year=request.POST['ano'], publisher=request.POST['editora'], edition=request.POST['edicao'], purchased=False, isbn=request.POST['isbn'].upper())
        book.save()
        
        #writer
        for writer_name in writers_list:
            writer = Writer(name=writer_name, book=book)
            writer.save()
    
    #suggestion
    processed_comment = processTextArea(request.POST['comentario'])
    suggestion = Suggestion(date=datetime.datetime.now(), book=book, name=request.POST['nome'], email=request.POST['email'], course=request.POST['disciplina'], amount=request.POST['quantidade'], comment=processed_comment)
    suggestion.save()

def searchBooks(value):
    book_ids = Set([])
    result = []
    
    #Get books from id set (and their corresponding suggestions)
    books = []
    writers = []
    if value is not None and len(value) > 0:
        books = search(Book, value)
        writers = search(Writer, value)
        print '============================= search: '+value
        print len(books)
    else:
        books = Book.objects.all()
    
    for b in books:
        book_ids.add(b.pk);
        s = Suggestion.objects.filter(book=b.pk).order_by('-date')
        w = Writer.objects.filter(book=b.pk).order_by('name')
        a = 0
        for sug in s:
            a += sug.amount
        result.append(BookView(book=b, suggestions=s, writers=w, amount=a))
    
    for writer in writers:
        if(writer.book not in book_ids):
            book_ids.add(writer.book)
            s = Suggestion.objects.filter(book=writer.book).order_by('-date')
            w = Writer.objects.filter(book=writer.book).order_by('name')
            a = 0
            for sug in s:
                a += sug.amount
            result.append(BookView(book=b, suggestions=s, writers=w, amount=a))

    return result


def processTextArea(comment):
    lines = comment.split('\r\n') #['line1', '', '', 'line4', 'line5']

    while '' in lines:#remove empty lines -> ['line1', 'line4', 'line5']
        lines.remove('')

    return '#'.join(lines)#join elements -> 'line1#line4#line5'


def exportWorkbook(query, withCourse=1):
    books, suggestions, authors = searchBooks(query)
    book = Workbook(encoding='utf-8')
    sheet = book.add_sheet('Livros Sugeridos')
    cols = ['ITEM', 'QTD', 'AUTORES', u'TÍTULO', 'EDITORA', 'ISBN', u'EDIÇÃO', 'ANO', 'SUGERIDO POR', 'EMAIL', u'COMENTÁRIO']

    if withCourse == 1:#Add 'DISCIPLINA'
        cols = ['ITEM', 'QTD', 'AUTORES', u'TÍTULO', 'EDITORA', 'ISBN', u'EDIÇÃO', 'ANO', 'DISCIPLINA','SUGERIDO POR', 'EMAIL', u'COMENTÁRIO']

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
    sheet.col(9).width = sheet.col(9+withCourse).width * 2; #email
    sheet.col(10).width = sheet.col(10+withCourse).width * 4; #comment

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
        #sheet.write(c+1,1,suggestions[item].amount)
        

        sheet.write(c+1,3,books[item].title)
        sheet.write(c+1,4,books[item].publisher)
        sheet.write(c+1,5,books[item].isbn)
        sheet.write(c+1,6,books[item].edition)
        sheet.write(c+1,7,books[item].year)
        #sheet.write(c+1,8,suggestions[item].name)
        #sheet.write(c+1,9,suggestions[item].email)
        #sheet.write(c+1,10,suggestions[item].comment)

        countSuggestion = 0
        
        for suggestion in suggestions[item]:
            sheet.write(c+1 + countSuggestion,1,suggestion.amount)
            
            if withCourse == 1:
                sheet.write(c+1 + countSuggestion,8,suggestion.course)
            
            sheet.write(c+1 + countSuggestion,8+withCourse,suggestion.name)
            sheet.write(c+1 + countSuggestion,9+withCourse,suggestion.email)
            sheet.write(c+1 + countSuggestion,10+withCourse,suggestion.comment)
            countSuggestion = countSuggestion + 1
        
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

        if len(suggestions[item]) > len(authors[item]):
            c = c + (len(suggestions[item]) - len(authors[item]))

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
