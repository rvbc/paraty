﻿from django.db import models
from django.utils import timezone

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
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField()
    purchased = models.BooleanField()
    search = models.CharField(max_length=1000)
    isbn = models.CharField(max_length=100)
	
    def __unicode__(self):
        return self.title
    
class Writer(models.Model):
    name = models.CharField(max_length=100)
    book = models.ForeignKey(Book)
    search = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' wrote \'' + self.book.title + '\''

class Suggestion(models.Model):
    date = models.DateTimeField()
    book = models.ForeignKey(Book)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    search = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name + ' suggests ' + str(self.amount) + ' volumes of \'' + self.book.title + '\''

def addSuggestion(request, writers_list):
    #book
    s = request.POST['titulo'] + ' ' + request.POST['editora']
    book = Book(title=request.POST['titulo'], year=request.POST['ano'], publisher=request.POST['editora'], edition=request.POST['edicao'], purchased=False, search=strip_accents(s), isbn=request.POST['isbn'])
    book.save()
    
    #writer
    for writer_name in writers_list:
        writer = Writer(name=writer_name, book=book, search=strip_accents(writer_name))
        writer.save()
    
    #suggestion
    processed_comment = processTextArea(request.POST['comentario'])
    s = processed_comment + ' ' + request.POST['nome'] + ' ' + request.POST['email']
    suggestion = Suggestion(date=timezone.now(), book=book, name=request.POST['nome'], email=request.POST['email'], amount=request.POST['quantidade'], comment=processed_comment, search=strip_accents(s))
    suggestion.save()

def searchSuggestion(value):
    books_match, suggestions_match, writers_list_list = searchBooks(value)

    books_grouping_by_title = [] #lista de lista
    suggestion_grouping_by_book_title = []
    writers_stringName_for_each_book_group = []

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
        writers_stringName_for_each_book_group.append(getWritersStringFromGroupBookWithSameTitle(goup_list_books))
        
        
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

    return books_grouping_by_title, suggestion_grouping_by_book_title, writers_stringName_for_each_book_group

def searchBooks(value):
    words_list = value.split()
    words_list = words_list if len(words_list) > 0 else [u'']
    book_id_set = Set([])

    #Writer table###################################
   
    writers = Writer.objects.filter(search__icontains=strip_accents(words_list[0]))
    for word in words_list[1:]:
        writers = writers.filter(search__icontains=strip_accents(word))

    for w in writers:
        book_writer = w.book
        book_id_set.add(book_writer.pk)
    
    #Book table######################################

    book_titles = Book.objects.filter(search__icontains=strip_accents(words_list[0]))
    for word in words_list[1:]:
        book_titles = book_titles.filter(search__icontains=strip_accents(word))

    for b in book_titles:
        book_id_set.add(b.pk)


    #Get books from id set (and their corresponding suggestions)
    books_match = Book.objects.filter(pk__in=book_id_set)
    suggestions_match = Suggestion.objects.filter(book__in=book_id_set)

    #Order books by title
    books_match = books_match.order_by('title')
    suggestions_match = suggestions_match.order_by('book__title')

    writers_list_list = getWritersFromBooks(books_match)

    return books_match, suggestions_match, writers_list_list

def getWritersFromBooks(book_list):
    writers_list_list = []

    for b in book_list:
        writers_book = Writer.objects.filter(book__exact=b.id)
        writers_book.order_by('name')
        writers_list_list.append(writers_book)
    
    #x = z#DEBUG

    return writers_list_list

def getWritersStringFromGroupBookWithSameTitle(group_book):

    writers_list_list = getWritersFromBooks(group_book)
    writers_nameSearch_set = Set([])
    writers_string = ''

    for writers_list in writers_list_list:
    
        for writer in writers_list:
            if not writer.search in writers_nameSearch_set:
                writers_nameSearch_set.add(writer.search)
                writers_string = writers_string + ', ' + writer.name
            
        
    writers_string = writers_string[2: ] + '.'

    #x = z#DEBUG

    return writers_string

def joinListListWritersInListWritersString (writers_list_list):

    writers_list_string = []

    for writers_list in writers_list_list:
        string_concat = ''

        for writer in writers_list:
            string_concat = string_concat + writer.name + ', '

        writers_list_string.append(string_concat[:-2])
    
    return writers_list_string
    
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
