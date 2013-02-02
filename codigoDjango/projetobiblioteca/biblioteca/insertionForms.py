from django import forms
from django.utils.datastructures import MultiValueDictKeyError
import datetime

class SuggestionForm(forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    
    titulo = forms.CharField(max_length=100)
    #escritor = forms.CharField(max_length=100)

    editora = forms.CharField(max_length=100)
    ano = forms.IntegerField(min_value=1, max_value=datetime.datetime.now().year)
    edicao = forms.IntegerField(min_value=1)
    isbn = forms.CharField(max_length=100)

    quantidade = forms.IntegerField(min_value=1)
    comentario = forms.CharField(max_length=200, required=False, widget=forms.Textarea)

    def get_error_message(trash, field_name, value):
        #value = self.cleaned_data[field_name]
        message = ''
        
        if value == '':#Filed is empty
            message = 'empty'
        elif field_name == 'nome' or field_name == 'comentario':#CharField(max_length=200)
            message = 'O campo \'' + field_name + '\' suporta somente 200 caracteres'
        elif field_name == 'titulo' or field_name == 'escritor' or field_name == 'editora' or field_name == 'isbn':#CharField(max_length=100)
            message = 'O campo \'' + field_name + '\' suporta somente 100 caracteres'
        elif field_name == 'edicao' or field_name == 'quantidade':#IntegerField
            message = 'Insira um inteiro correto para o campo \'' + field_name + '\''
        elif field_name == 'ano':
            message = 'Por favor, insira um valor correto para o campo \'ano\''
        elif field_name == 'email':
            message = 'Email com formato incorreto'
        
        return message

    def validate_writers(trash, request):
        count = 1
        fields = []
        found_error = False
        message_error = ''
        try:
            while request.POST.has_key('escritor_' + str(count)):
                if request.POST['escritor_' + str(count)] != '':
                    fields.append(request.POST['escritor_' + str(count)])
                count = count + 1
        except MultiValueDictKeyError:
            #Nothing...
            count = count
        count = count - 1

        if len(fields) == 0:
            found_error = True
            message_error = 'Nenhum escritor.'
        else:
            for writer in fields:
                if len(writer) > 100:
                    found_error = True
                    message_error = 'O campo escritor suporta apenas 100 caracteres'

        #x = z#DEBUG
        return fields, found_error, message_error