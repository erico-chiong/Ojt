from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item

# List all items

def item_list(request):
    items = Item.objects.all()
    return render(request, 'pages/item_list.html', {'items': items})

# Create a new item

def item_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Item.objects.create(name=name, description=description)
        return redirect('item_list')
    return render(request, 'pages/item_form.html')

# Update an item

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.save()
        return redirect('item_list')
    return render(request, 'pages/item_form.html', {'item': item})

# Delete an item

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'pages/item_confirm_delete.html', {'item': item})

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the home page!")
