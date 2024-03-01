from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm, LoginForm
from django.contrib.auth import logout,login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
import jwt
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    items = Item.objects.all()[:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

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
def error_response(request, code=200, message='Default message'):
    template = 'core/blurred_page.html'

    if code != 200:
        # If there's an error, render the error response
        template = 'core/error_response.html'

    context = {'code': code, 'message': message}
    return render(request, template, context)

