from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
def registerUser(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username, is_superuser=False)
        newUser.set_password(password)

        newUser.save()
        login(request, newUser)
        messages.success(request, "Başarıyla kaydoldunuz. Giriş yapıldı.")
        return redirect("index")
    else:
        context = {
        "form":form
        }
        return render(request, "register.html", context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {"form":form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if user is None:
            messages.info(request, "Kullanıcı adı veya şifre hatalı.")
            return render(request, "login.html", context)

        messages.success(request, "Giriş yapıldı.")
        login(request, user)
        return redirect("index")
    return render(request,"login.html", context)

def logoutUser(request):
    logout(request)
    messages.warning(request,"Başarıyla çıkış yapıldı.")
    return redirect("index")
