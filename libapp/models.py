from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# Book
class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
    subject = models.CharField(max_length=2000)
    book_add_time = models.TimeField(default=timezone.now())
    book_add_date = models.DateField(default=date.today())
    
    class Meta:
        unique_together = ("title", "author")
        
    def __str__(self) -> str:
        return self.title



class Peminjaman(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tgl_pinjam = models.DateField(default=date.today(), blank=False)
    tgl_kembali = models.DateField(blank=True, null=True)
    
    @property
    def book_title(self):
        return self.book_id.title
    
    @property
    def username(self):
        return self.user_id.username
    
    def __str__(self) -> str:
        return (
            self.book_id.title
            + " dipinjam oleh "
            + self.user_id.username
            + " tanggal "
            + str(self.tgl_pinjam)
        )
