from rest_framework import serializers

from .models import (Category, Image, Occasion, Product, RecipientType, Review,
                     Subcategory)


# Category serializers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Subcategory serializers
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"

# Category and Subcategory serializers


class CategoryAndSubcategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image',
                  'description', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = Subcategory.objects.filter(category=obj)
        serializer = SubcategorySerializer(subcategories, many=True)
        return serializer.data


# occassion serializer
class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = "__all__"


# recipient type serializer
class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipientType
        fields = "__all__"


# Image serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


# Product serializer
class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(
        source='subcategory.category.name')
    category_slug = serializers.ReadOnlyField(
        source='subcategory.category.slug')
    subcategory_name = serializers.ReadOnlyField(source='subcategory.name')
    subcategory_slug = serializers.ReadOnlyField(source='subcategory.slug')
    occasions = OccasionSerializer(many=True, read_only=True)
    recipient_types = RecipientSerializer(many=True, read_only=True)
    more_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


# serializers for review
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


# Product serializer for search
class ProductSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "primary_image",
                  "price", "discounted_price")
