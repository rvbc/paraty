# Create your views here.
from biblioteca.models import Book, User, Writer, Suggestion
from biblioteca import models
from biblioteca.insertionForms import SuggestionForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import django.template.loader
import django.template  
from django.contrib import messages
from django.template.response import TemplateResponse
from django.template import RequestContext

import json
import tkMessageBox

def home(request):
    t = django.template.loader.get_template("index.html")
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def suggestion(request):
    if request.method == 'POST':#form submitted
        return add_suggestion(request)
    else:#suggestion's home
        t = django.template.loader.get_template("suggestion.html")
        c = RequestContext(request)
        return HttpResponse(t.render(c))
    
def books(request):
    if request.method == 'POST':#export excel!
        return export(request)
    else:#books' home
        t = django.template.loader.get_template("books.html")
        c = RequestContext(request)
        return HttpResponse(t.render(c))

    #if request.method == 'POST'

def add_suggestion(request):
    form = SuggestionForm(request.POST)
    c = RequestContext(request)
    witers_list, has_writer_error, writer_error_message = form.validate_writers(request)
    errorMessage = ''
    #warningMessage = 'Caso queira alterar os dados da tentativa anterior, volte.'
    if form.is_valid() and not has_writer_error:#add suggestion at DB and notify user
        #x = request.POST['comentario']
        #y=x.split('\r\n')
        #y = (value for value in y if value != '\n') 
        #form.get_error_message(x)
        #tkMessageBox.showinfo(title="Greetings", message="Hello World!")
        #z = 1 + k
        models.addSuggestion(request, witers_list)
        c['msg'] = {'title' : 'OK', 'content' : 'Seu livro sugerido foi cadastrado com sucesso. Obrigado!'}
        return TemplateResponse(request, 'suggestion.html', c)
    else:#Notify errors and user must try again
        emptyFields = []
        if has_writer_error:
            if writer_error_message == 'Nenhum escritor.':
                emptyFields.append('autor')
            else:
                errorMessage = errorMessage + 'Cada campo \'autor\' suporta somente 100 caracteres. '
        for key in form.errors:#wrong fields
            field = str(key)
            value = request.POST[key]
            message = form.get_error_message(field, value)
            if message == 'empty':#field left blank
                emptyFields.append(field)
            else:#field contains invalid value
                errorMessage = errorMessage + message + '. '
        if len(emptyFields) > 0:
            errorMessage = errorMessage + 'O(s) seguinte(s) campo(s) deve(m) ser preenchido(s): \'' + emptyFields.pop(0) + '\''
            for i in emptyFields:
                errorMessage = errorMessage + ', \'' + i + '\''
            errorMessage = errorMessage + '.'
        #errorMessage = errorMessage + request.POST['escritor']
        #return HttpResponse(errorMessage)

        #messages.info(request, warningMessage, extra_tags='safe')
        #messages.error(request, errorMessage, extra_tags='safe')
        #t = django.template.loader.get_template("suggestion.html")
        #c = django.template.Context()
        #return HttpResponse(t.render(c))
        c['error'] = errorMessage
        c['form'] = form		
        c['writers'] = witers_list
        return TemplateResponse(request, 'suggestion.html', c)

def search(request):
    q = request.GET['q']
    c = RequestContext(request)
    if len(q) > 0:
        q = q.strip()
    books, suggestions, writers = models.searchSuggestion(q)

    c['group_book_list'] = books
    c['group_suggestion_list'] = suggestions
    c['writers'] = writers
    c['q'] = q

    if len(books) == 0:#Nothing found!
        #colocar uma mensagem de erro. Mas eh melhor arrumar antes as mensagens de base.html
        c['msg'] = {'title' : 'Hey', 'content' : 'Nenhum livro foi encontrado nesta pesquisa. Tente com outros termos.'}
        return TemplateResponse(request, 'books.html', c)
    else:#Display results at books.html
        return TemplateResponse(request, 'books.html', c)

def export(request):
    q = request.POST['q']
    c = RequestContext(request)
    if len(q) > 0:
        q = q.strip()
    books, suggestions, writers = models.searchSuggestion(q)

    planilha, name = models.exportWorkbook(q)

    #x = z#DEBUG

    if len(books) == 0:#Nothing found!
        #colocar uma mensagem de erro. Mas eh melhor arrumar antes as mensagens de base.html
        c['group_book_list'] = books
        c['group_suggestion_list'] = suggestions
        c['error'] = 'Nenhum livro para ser exportado. Se uma busca foi feita, tente utilizar novos termos.'
        c['q'] = q
        return TemplateResponse(request, 'books.html', c)
    else:#Display results at books.html
        #return TemplateResponse(request, 'books.html', {'group_book_list': books, 'group_suggestion_list':suggestions, 'q' : q})
       return models.xls_to_response(planilha,name)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    c = RequestContext(request)

    if username:
        if password:

            try:
                user = User.objects.get(login=username)
                if user.password == request.POST['password']:
                    request.session['login'] = user.login
                    return TemplateResponse(request, 'index.html')
                else:
                    c['error'] = 'Senha inv&aacute;lida.'
                    return TemplateResponse(request, 'index.html', c)

            except User.DoesNotExist:
                c['error'] = 'Login inexistente.'
                return TemplateResponse(request, 'index.html', c)

        else:
            c['error'] = 'Informe sua senha para login.'
            return TemplateResponse(request, 'index.html', c)
    else:
        c['error'] = 'Informe seu nome de usu&aacute;rio para login.'
        return TemplateResponse(request, 'index.html', c)

def logout(request):
    login = request.session['login']
    c = RequestContext(request)

    if login:
        del request.session['login']
        return TemplateResponse(request, 'index.html')
    else:
        c['error'] = 'Sess&atilde;o expirada.'
        return TemplateResponse(request, 'index.html', c)
