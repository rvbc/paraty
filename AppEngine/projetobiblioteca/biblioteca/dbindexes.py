from models import Book, Writer
from dbindexer.api import register_index

register_index(Book, {'search': 'icontains'})
register_index(Writer, {'search': 'icontains'})