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

import tkMessageBox

def home(request):
    t = django.template.loader.get_template("index.html")
    c = django.template.Context()
    return HttpResponse(t.render(c))

def suggestion(request):
    t = django.template.loader.get_template("suggestion.html")
    c = django.template.Context()
    return HttpResponse(t.render(c))
    
def books(request):
    t = django.template.loader.get_template("books.html")
    c = django.template.Context()
    return HttpResponse(t.render(c))

    #if request.method == 'POST'

def add_suggestion(request):
    form = SuggestionForm(request.POST)
    errorMessage = ''
    #warningMessage = 'Caso queira alterar os dados da tentativa anterior, volte.'
    if form.is_valid():#add suggestion at DB and notify user
        #x = request.POST['comentario']
        #y=x.split('\r\n')
        #y = (value for value in y if value != '\n') 
        #form.get_error_message(x)
        #tkMessageBox.showinfo(title="Greetings", message="Hello World!")
        #z = 1 + k
        models.addSuggestion(request)
        return HttpResponse('<script>alert(\'Cadastro realizado com sucesso. Obrigado!\')</script>')
    else:#Notify errors and user must try again
        emptyFields = []
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

        return TemplateResponse(request, 'suggestion.html', {'error': errorMessage, 'form':form})