from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Avg

from .models import (Category, Occasion, Product, RecipientType, Review,
                     Subcategory)
from .serializers import (CategoryAndSubcategorySerializer, CategorySerializer,
                          OccasionSerializer, ProductSearchSerializer,
                          ProductSerializer, RecipientSerializer,
                          ReviewSerializer, SubcategorySerializer)


# getting the subcategories list under a specified category
class FeaturedProducts(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):

        return Product.objects.filter(featured=True)


# views for getting all categories and subcategories
@api_view(['GET'])
def get_all_categories_subcategories(request):
    categories = Category.objects.all()
    serializer = CategoryAndSubcategorySerializer(categories, many=True)
    return Response(serializer.data)


# views for getting all categories
@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# getting the subcategories list under a specified category
class SubcategoriesByCategory(ListAPIView):
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        # Extract category_slug from URL
        category_slug = self.kwargs['category_slug']
        return Subcategory.objects.filter(category__slug=category_slug)


# getting all occasion list
@api_view(['GET'])
def get_all_occasions(request):
    occasions = Occasion.objects.all()
    serializer = OccasionSerializer(occasions, many=True)
    return Response(serializer.data)

# getting all occasion list


@api_view(['GET'])
def get_all_recipients(request):
    recipients = RecipientType.objects.all()
    serializer = RecipientSerializer(recipients, many=True)
    return Response(serializer.data)


# get single product
@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


# getting all reviews for a single product
@api_view(['GET'])
def get_reviews(request, product_slug):
    try:
        reviews = Review.objects.filter(product__slug=product_slug)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Reviews not found'}, status=404)


@api_view(['POST'])
def submit_review(request):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Product search functionality
class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filter based on parameters in the query string
        filters = Q()

        occasion = self.request.query_params.get('occasion')
        if occasion:
            filters &= Q(occasions__slug=occasion)

        recipient_type = self.request.query_params.get('recipient_type')
        if recipient_type:
            filters &= Q(recipient_types__slug=recipient_type)

        category = self.request.query_params.get('category')
        if category:
            filters &= Q(subcategory__category__slug=category)

        subcategory = self.request.query_params.get('subcategory')
        if subcategory:
            filters &= Q(subcategory__slug=subcategory)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            filters &= Q(discounted_price__gte=min_price)

        max_price = self.request.query_params.get('max_price')
        if max_price:
            filters &= Q(discounted_price__lte=max_price)


        # Sorting parameters
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'priceLowToHigh':
            queryset = queryset.order_by('discounted_price')
        elif sort_by == 'priceHighToLow':
            queryset = queryset.order_by('-discounted_price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'ratingLowToHigh':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
        elif sort_by == 'ratingHighToLow':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')

        return queryset.filter(filters)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_count = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data, total_count=total_count)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_paginated_response(self, data, total_count):
        response = super().get_paginated_response(data)
        response.data['total_count'] = total_count
        return response
