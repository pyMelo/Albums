# urls.py
from django.urls import path
from . import views


app_name = 'profiles'
urlpatterns = [
    # Your other URL patterns
    path('<str:username>/', views.user_detail, name='user_detail'),

]
