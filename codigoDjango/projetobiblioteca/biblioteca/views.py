# Create your views here.
from biblioteca.models import Book, User, Writer, Suggestion
from django.http import HttpResponse
import django.template.loader
import django.template  

def add_suggestion(request):
    t = django.template.loader.get_template("add_sugestao.html")
    c = django.template.Context()
    return HttpResponse(t.render(c))
