from django.contrib import admin

# Register your models here.
from .models import Book, Peminjaman

# Register your models here.
class BookFilter(admin.ModelAdmin):
    list_display = ("title","author","quantity","subject")
    list_filter = ("title","author","subject","book_add_date")
    search_fields = ("title","author","subject")
    
admin.site.register(Book, BookFilter)

class IssuedItemFilter(admin.ModelAdmin):
    list_display = ("book_title","username","tgl_pinjam","tgl_kembali")
    list_filter = ("tgl_pinjam","tgl_kembali","book_id__title","user_id__username") 
    search_fields = ("user_id__username","book_id__title","book_id__subject")

admin.site.register(Peminjaman, IssuedItemFilter)