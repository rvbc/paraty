import search
from search.core import porter_stemmer
from biblioteca.models import Book, Writer


search.register(Book, ('titulo', 'editora','isbn', 'ano', ), indexer=porter_stemmer)
search.register(Writer, ('name', ), indexer=porter_stemmer)

