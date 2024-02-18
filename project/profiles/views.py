from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfilePictureForm


from .models import UserProfile

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profiles/profilepage.html',user)

def user_detail(request, username):
    user = request.user
    if request.method == 'POST':
        print('button NOW pressed')
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = ProfilePictureForm(instance=user)
    # Your logic for retrieving additional user-related information if needed

    return render(request, 'profiles/user_detail.html', {'user': user})