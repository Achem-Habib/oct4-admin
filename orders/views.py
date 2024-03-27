
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Address, Order, OrderItem, WishlistItem
from .serializers import AddressSerializer, OrderSerializer, OrderItemGetSerializer, OrderItemSubmissionSerializer, WishlistSerializer, WishlistGetSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@api_view(['GET'])
def get_order_history(request, username):
    try:
        user = User.objects.get(username=username)
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class PlaceOrderAPIView(APIView):
    def post(self, request, format=None):
        order_serializer = OrderSerializer(data=request.data)
       
        try:
            if order_serializer.is_valid():
                order = order_serializer.save()

                # Save ordered items for the order
                items_data = request.data.get('items', [])
                for item_data in items_data:
                    item_data['order'] = order.id
                    item_serializer = OrderItemSubmissionSerializer(data=item_data)
                    if item_serializer.is_valid():
                        item_serializer.save()
                    else:
                        order.delete()  # Rollback if item validation fails
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            print(order_serializer.errors)
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




"""---------Address views ---------"""
@api_view(['GET'])
def get_addresses_by_username(request, username):
    try:
        user = User.objects.get(username=username)
        addresses = Address.objects.filter(user=user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_address(request):
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_address(request, pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_address(request, pk):
    try:
        address = Address.objects.get(pk=pk)
        
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    address.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




"""-------------Wishlist views---------"""

@api_view(['GET'])
def get_wishlist(request, username):
    try:
        user = User.objects.get(username=username)
        wishlist = WishlistItem.objects.filter(user=user)
        serializer = WishlistGetSerializer(wishlist, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_wishlist_item(request):
    # Check if a wishlist item for the specific user and product exists
    user_id = request.data.get('user')  
    product_id = request.data.get('product')
    user = User.objects.get(pk=user_id)  
    
    existing_wishlist_item = WishlistItem.objects.filter(user=user, product=product_id).first()
    
    if existing_wishlist_item:
        return Response({'message': 'Wishlist item already exists for this user.'}, status=status.HTTP_409_CONFLICT)

    # If wishlist item doesn't exist, proceed to create a new one
    serializer = WishlistSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_wishlist_item(request, pk):
    try:
        wishlist = WishlistItem.objects.get(pk=pk)
    except WishlistItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    wishlist.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
