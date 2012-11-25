# Create your views here.
from biblioteca.models import Book, User, Writer, Suggestion
from biblioteca.insertionForms import SuggestionForm
from django.http import HttpResponse, HttpResponseRedirect
import django.template.loader
import django.template  

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
