from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser  # Custom user modeli
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Passwordlar mosligini tekshirish
        if password != confirm_password:
            messages.error(request, "Parol mos kelmadi. Qaytadan urinib ko'ring.")
            return redirect('register')
        
        # User yaratish
        if not CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.create_user(email=email, phone_number=phone_number, password=password)
            messages.success(request, "Ro'yxatdan o'tdingiz! Tizimga kirishingiz mumkin.")
            return redirect('login')
        else:
            messages.error(request, "Ushbu email allaqachon mavjud.")
            return redirect('register')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz.")
            return redirect('home')
        else:
            messages.error(request, "Email yoki parol noto'g'ri. Qaytadan urinib ko'ring.")
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')