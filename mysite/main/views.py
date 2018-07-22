from django.shortcuts import render
from django.http import HttpResponse
from main.models import Item, Category, Cart, Image
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from main.serializers import ItemSerializer, CategorySerializer, CartSerializer, ImageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils.encoding import smart_str
from decimal import Decimal


class ItemViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving items.
    """
    def list(self, request):
        items = Item.objects
        if request.GET.get('category'):
            items = items.filter(category=request.GET.get('category'))
        items = items.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        items = Item.objects.all()
        item = get_object_or_404(items, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """
    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cats = Category.objects.all()
        cat = get_object_or_404(cats, pk=pk)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    def create(self, request):
        serializer = CartSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing cart items.
    """

    def list(self, request):
        cart = Cart.objects.filter(user=request.user).all()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def upload_image(request):
    instance = Image(file=request.FILES['fileimg'])
    instance.save()
    return HttpResponse(str(instance.pk))

@api_view(['GET'])
def cart_submit(request, id, quantity):
    data = request.data.copy()
    items = Item.objects.all()
    item = get_object_or_404(items, pk=id)
    # FIXME: This whole thing is so wrong
    TWOPLACES = Decimal(10) ** -2 
    data['user'] = 1
    data['item'] = item.id
    data['price'] = float(Decimal(item.price).quantize(TWOPLACES))
    data['quantity'] = quantity
    data['charge'] = float(Decimal(Decimal((5/100)).quantize(TWOPLACES) * item.price).quantize(TWOPLACES))
    data['currency'] = item.currency
    data['total'] = float(Decimal(data['price']).quantize(TWOPLACES) + Decimal(data['charge']).quantize(TWOPLACES))
    data['timestamp_added'] = 'xxx' ## FIXME

    serializer = CartSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving images.
    """
    def list(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def serve_image(request, id):
    img = get_object_or_404(Image, pk=id)
    response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(img.file.name)
    response['X-Sendfile'] = smart_str(img.file.path)
    return response
