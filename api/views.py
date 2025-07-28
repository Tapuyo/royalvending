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


from core.serializers import ProductSerializer
from core.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

@api_view(['GET'])
def getData(request):
    # Accept a single 'search' parameter for both name and category
    search = request.GET.get('search', '').strip()

    if not search:
        # Return all products if no search input is provided
        products = Product.objects.all()
    else:
        # Most accurate matches first (exact name or category match)
        exact_matches = Product.objects.filter(
            Q(name__iexact=search) | Q(category__iexact=search)
        )

        # Partial matches excluding the exact matches
        partial_matches = Product.objects.filter(
            Q(name__icontains=search) | Q(category__icontains=search)
        ).exclude(id__in=exact_matches.values_list('id', flat=True))

        # Combine and preserve order
        products = list(exact_matches) + list(partial_matches)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
