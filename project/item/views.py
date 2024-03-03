from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[:3]
    ratings = Rating.objects.filter(item=item)
    
    recently_viewed = request.session.get('recently_viewed',[])
    
    if pk not in recently_viewed:
        recently_viewed.append(pk)
    recently_viewed = recently_viewed[-3:]
    request.session['recently_viewed'] = recently_viewed
    
    
    ###
    recently_items = Item.objects.filter(id__in=recently_viewed).exclude(pk=pk)[:3]
    
    print(f'recently_items{recently_items}')
    
    if ratings:
        average_rating = round(sum(rating.value for rating in ratings) / len(ratings), 2)
    else:
        average_rating = None
        
    user_rating = Rating.objects.filter(item=item,rated_by=request.user).first()
    

    if request.method == 'POST':
        
        if user_rating:
            return render(request,'item/rating_submitted.html')
        else:
            rating_form=RatingForm(request.POST)
            
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.item = item
            rating.rated_by = request.user
            rating.save()
    else:
        rating_form = RatingForm()
        
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'ratings': ratings,
        'average_rating': average_rating,
        'rating_form': rating_form,
        'recently_items': recently_items,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('visuals:index')