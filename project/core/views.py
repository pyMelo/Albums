from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm
from django.contrib.auth import logout,login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.views import View

import jwt

def index(request):
    return render(request, 'core/index.html')

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })
def logout_view(request):
    logout(request)
    
    response = redirect('core:index')
    response.delete_cookie('jwt_token')  # Remove the jwt_token cookie

    return response

def login_view(request):
    template_name = 'core/login.html'
    authentication_form = AuthenticationForm

    if request.method == 'GET':
        form = authentication_form(request)
        return render(request, template_name, {'form': form})

    elif request.method == 'POST':
        form = authentication_form(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            # Generate JWT token and set it in the cookies
            user = form.get_user()
            expiration_time = datetime.utcnow() + timedelta(days=1)
            
            payload = {
                'username': user.username,
                'exp': expiration_time,
            }
            
            jwt_token = jwt.encode(payload, '259fabc6e7b379d1babad0eb3b8ed8a14c3ccfed5acf7d93c81f1add36f7626f', algorithm='HS256')
            response = redirect('core:index') 
            response.set_cookie('jwt_token', jwt_token, httponly=True, secure=True)

            print(request.COOKIES.get('jwt_token'))
            return response

        return render(request, template_name, {'form': form})