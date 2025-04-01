from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustiomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES) # 유저정보와 , 사진)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm

    context = {
        'form': form
    }

    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        form = CustiomAuthenticationForm(request, request.POST) 
        if form.is_valid():
            user = form.get_user() # 여러 정보 중 사용자의 정보를 꺼내옴
            auth_login(request, user) # 넣어서 세션 발급, 쿠키 .. 처리(로그인처리)
            return redirect('posts:index')

    else:
        form = CustiomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('posts:index')

def profile(request, username):
    user_profile = User.objects.get(username=username)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)
