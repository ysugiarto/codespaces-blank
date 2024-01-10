from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Book, Peminjaman

# Create your views here.
def home(request):
    return render(request, "libapp/home.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect("register")
            
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect("register")
            
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = password1
            )
            
            user.save()
            
            return redirect("login")
        
        else:
            messages.info(request, "Password mismatch")
            return redirect("register")
    
    return render(request, "libapp/register.html")
            
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)
               
        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("login")
        
        login(request, user)
        return redirect("home")
    
    else:
        return render(request, "libapp/login.html")
    
def logout_user(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def pinjam(request):
    if request.method == "POST":
        book_id = request.POST["book_id"]
        current_book = Book.objects.get(id=book_id)
        book = Book.objects.filter(id=book_id)
        peminjaman = Peminjaman.objects.create(
            user_id = request.user, 
            book_id = current_book
        )
        peminjaman.save()
        
        book.update(quantity=book[0].quantity - 1)
        
        messages.success(request, "Book issued successfully.")
        
    my_items = Peminjaman.objects.filter(
        user_id = request.user,
        tgl_kembali__isnull=True
    ).values_list("book_id")
    books = Book.objects.exclude(id__in=my_items).filter(quantity__gt=0)
    
    return render(request, "libapp/issue_item.html", {"books": books})


@login_required(login_url="login")
def history(request):
    my_items = Peminjaman.objects.filter(user_id = request.user).order_by("-tgl_pinjam")
    
    paginator = Paginator(my_items, 10)
    
    page_number = request.GET.get('page', '1')
    
    show_data_final = paginator.get_page(page_number)
    
    return render(request, "libapp/history.html", {"books": show_data_final})
