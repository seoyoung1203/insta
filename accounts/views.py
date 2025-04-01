from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustiomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
from django.contrib.auth.decorators import login_required

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

@login_required
def logout(request):
    auth_logout(request)
    return redirect('posts:index')

def profile(request, username):
    user_profile = User.objects.get(username=username)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)

@login_required
def follow(request, username):
    me = request.user # 로그인한 사람
    you = User.objects.get(username=username) #페이지의 정보(들어간 페이지 유저)

    if me == you:
        return redirect('accounts:profile', username)

    # if you in me.follings.all():
    if me in you.followers.all():
        you.followers.remove(me)
    else: 
        you.followers.add(me)
        # me.followings.add(you)

    return redirect('accounts:profile', username)
