from core.serializers import ProductSerializer
from core.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(request):
    # Get query params (e.g., ?search=water or ?category=drinks)
    search = request.GET.get('search', None)
    category = request.GET.get('category', None)

    # Start with all products
    products = Product.objects.all()

    # Filter by search in product name
    if search:
        products = products.filter(name__icontains=search)

    # Filter by category
    if category:
        products = products.filter(category__icontains=category)

    # Serialize and return
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
