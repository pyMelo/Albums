from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import cv2
import numpy as np


from .forms import NewItemForm, EditItemForm, RatingForm
from .models import Category, Item, Rating


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter()
    
    
    
    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)

            image = request.FILES['image'].read()
            numpy_array = np.frombuffer(image, np.uint8)
            cv_image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            face_classifier = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

            if len(faces) > 0: 
                message = 'Face detected in the uploaded image. You cannot upload images with faces.'
                return render(request, 'item/face_detection_warning.html', {
                'warning_message': message,
                })
            else:
                item.created_by = request.user
                item.save()
                return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })


def recently_viewed( request, pk ):
    print('Entered in the recently_viewed')

    if not "recently_viewed" in request.session:
        request.session["recently_viewed"] = []
        request.session["recently_viewed"].append(pk)
    else:
        if pk in request.session["recently_viewed"]:
            request.session["recently_viewed"].remove(pk)
        request.session["recently_viewed"].insert(0, pk)
        if len(request.session["recently_viewed"]) > 5:
            request.session["recently_viewed"].pop()
    request.session.modified =True

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[:3]
    ratings = Rating.objects.filter(item=item)
    
    recently_viewed(request,pk)
    if ratings:
        average_rating = round(sum(rating.value for rating in ratings) / len(ratings), 2)
    else:
        average_rating = None
        
    user_rating = Rating.objects.filter(item=item, rated_by=request.user).first()
    
    if request.method == 'POST':
        print('Entered in the POST method')
        rating_form=RatingForm(request.POST)
            
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.item = item
            rating.rated_by = request.user
            form_submitted = True 
            rating.save()
    else:
        rating_form = RatingForm()
        form_submitted = False

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'ratings': ratings,
        'average_rating': average_rating,
        'rating_form': rating_form,
        'user_rating':user_rating,
        'form_submitted': form_submitted,
    })



@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('visuals:index')