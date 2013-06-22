import search
from search.core import porter_stemmer_non_stop
from biblioteca.models import Book, Writer

search.register(Book, ('titulo', 'editora','isbn', 'ano', ), indexer=porter_stemmer_non_stop)
search.register(Writer, ('name', ), indexer=porter_stemmer_non_stop)

