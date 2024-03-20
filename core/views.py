from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from item.models import Category, Item

from .forms import SignupForm

# Create your views here.
def index(request):

    items = Item.objects.filter(is_sold=False)[0:6]
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
        
    form = SignupForm()        

    return render(request, 'core/signup.html', {
        'form': form
    })

@login_required
def custom_logout(request):
    if request.method == 'POST' and request.session:
        logout(request)

    return redirect('/')

    