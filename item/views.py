from django.shortcuts import render, get_object_or_404, redirect

from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.db.models import Q

from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

import stripe

# Create your views here.

# STRIPES

class SuccessView(TemplateView):
    template_name = 'item/success.html'


class CancelledView(TemplateView):
    template_name = 'item/cancelled.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/items/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'quantity': 1,
                        'price': 'price_1OwR2Z1vQydc3tGN1ozFeQmR',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

# END STRIPES
        
def itemsstripes(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    itemsstripes = stripe.Product.list(limit=3)
  
    return render(request, 'item/itemsstripes.html',{
        'itemsstripes' : itemsstripes
    })

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'item/items.html',{
        'items' : items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
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
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

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