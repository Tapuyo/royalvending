# from core.serializers import ProductSerializer
# from core.models import Product
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# @api_view(['GET'])
# def getData(request):
#     # Get query params (e.g., ?search=water or ?category=drinks)
#     search = request.GET.get('search', None)
#     category = request.GET.get('category', None)

#     # Start with all products
#     products = Product.objects.all()

#     # Filter by search in product name
#     if search:
#         products = products.filter(name__icontains=search)

#     # Filter by category
#     if category:
#         products = products.filter(category__icontains=category)

#     # Serialize and return
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


from core.serializers import CategorySerializer, ProductSerializer
from core.models import Category, Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

@api_view(['GET'])
def getData(request):
    search = request.GET.get('search', '').strip()
    supplier = request.GET.get('supplier', '').strip()
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))

    # Start with all products
    products = Product.objects.all()

    # Apply search filter (name or category)
    if search:
        exact_matches = Product.objects.filter(
            Q(name__iexact=search) | Q(category__iexact=search)
        )

        partial_matches = Product.objects.filter(
            Q(name__icontains=search) | Q(category__icontains=search)
        ).exclude(id__in=exact_matches.values_list('id', flat=True))

        products = list(exact_matches) + list(partial_matches)
    else:
        products = list(products)

    # Apply supplier filter
    if supplier:
        products = [p for p in products if supplier.lower() in p.supplier.lower()]

    # Normalize and save categories (optional)
    for product in products:
        if product.category:
            normalized_name = product.category.strip().lower()
            Category.objects.get_or_create(name=normalized_name)

    # Pagination
    total = len(products)
    start = (page - 1) * limit
    end = start + limit
    paginated_products = products[start:end]

    serializer = ProductSerializer(paginated_products, many=True)
    return Response({
        "total": total,
        "page": page,
        "limit": limit,
        "results": serializer.data
    })


@api_view(['GET'])
def getCategories(request):

    products = Category.objects.all()
    
    serializer = CategorySerializer(products, many=True)
    return Response(serializer.data)
