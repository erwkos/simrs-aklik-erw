from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def dashboard(request):
    return render(request, 'user/dashboard.html')


def profil(request):
    return render(request, 'user/profil.html')


def login(request):
    if request.user.is_anonymous:
        return render(request, 'user/login.html')
    else:
        return redirect('/user/dashboard')


def postlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        messages.info(request,
                      'Selamat datang di aKLIK.')
        return redirect('/user/dashboard')
    else:
        messages.info(request, 'Login gagal')
        return redirect('login')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Anda telah keluar, terima kasih sudah berkunjung.')
    return redirect('login')
