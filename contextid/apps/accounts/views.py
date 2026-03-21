from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import *

@csrf_protect
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")  
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {"form": form})

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # 'next' handles redirection back to the page they were trying to access
                next_url = request.GET.get('next', 'accounts:dashboard') 
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = LoginForm()
        
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    # Clear profile from session
    if 'current_profile_id' in request.session:
        del request.session['current_profile_id']

    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect("/")

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")