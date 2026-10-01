from django.shortcuts import render
from django.http import HttpResponse

from .models import Category, Tag, Product

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the products index.")

def product_list(request):
    # Base queryset for products, using select_related for category 
    # and prefetch_related for tags to optimize queries
    products = Product.objects.select_related('category').prefetch_related('tags')

    description_search = request.GET.get('q', '')
    category_filters = request.GET.getlist('category', [])
    tag_filters = request.GET.getlist('tags', [])

    if description_search:
        products = products.filter(description__icontains=description_search)

    if category_filters:
        products = products.filter(category__name__in=category_filters)

    if tag_filters:
        products = products.filter(tags__name__in=tag_filters)

    products = products.distinct()  # Ensure distinct results when filtering by tags

    product_data = {
        'products': products,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'search_query': description_search,
        'selected_categories': category_filters,
        'selected_tags': tag_filters
    }

    return render(request, 'products/product_list.html', product_data)