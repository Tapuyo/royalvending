from core.serializers import (
    CategorySerializer,
    FavoriteSerializer,
    ProductSerializer,
    UserSerializer,
)
from core.models import Category, Product, Favorites
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(["GET"])
def getData(request):
    search = request.GET.get("search", "").strip()
    supplier = request.GET.get("supplier", "").strip()
    page = int(request.GET.get("page", 1))
    limit = int(request.GET.get("limit", 10))

    # Start with all products
    products = Product.objects.all()

    # Apply search filter (name or category)
    if search:
        exact_matches = Product.objects.filter(
            Q(name__iexact=search) | Q(category__iexact=search)
        )

        partial_matches = Product.objects.filter(
            Q(name__icontains=search) | Q(category__icontains=search)
        ).exclude(id__in=exact_matches.values_list("id", flat=True))

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
    return Response(
        {"total": total, "page": page, "limit": limit, "results": serializer.data}
    )


@api_view(["GET"])
def getCategories(request):

    products = Category.objects.all()

    serializer = CategorySerializer(products, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"user": {"username": request.user.username, "id": request.user.id}})


@api_view(["POST"])
def addUserFav(request):
    serializer = FavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(request)
        Favorites.objects.update_or_create(
            item_code=request.data["item_code"], 
            userid=request.data["userid"],
            defaults={
                "userid": request.data["userid"],
                "name": request.data["name"],
                "current_price": request.data["current_price"],
                "image_url": request.data["image_url"],
                "product_link": request.data["product_link"],
                "supplier": request.data["supplier"],
                "supplier_url": request.data["supplier_url"],
                "category": request.data["category"],
                "item_body": request.data["item_body"],
                "item_quantity": request.data["item_quantity"],
            },
        )
        return Response({"data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(["GET"])
def getUserFav(request):

    favorites = Favorites.objects.all().filter(userid=request.GET.get("userid", ""))

    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def deleteUserFav(request):
    fav_id = request.data.get("id")
    if not fav_id:
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        favorite = Favorites.objects.get(id=fav_id)
        favorite.delete()
        return Response({"data": "Successfully deleted"}, status=status.HTTP_200_OK)
    except Favorites.DoesNotExist:
        return Response({"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def updateUserFav(request):

    print(request)
    Favorites.objects.update_or_create(
        id=request.data["id"], 
        defaults={
            "item_quantity": request.data["item_quantity"],
        },
    )
    return Response({"data": 'Successfully updated'}, status=status.HTTP_200_OK)



@api_view(["POST"])
def addProduct(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
def updateProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data, partial=True)  
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)