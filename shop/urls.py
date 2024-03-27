from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path('featured-products/',
         views.FeaturedProducts.as_view(), name='featured-products'),

    # Get all categories and subcategories
    path('categories-subcategories/',
         views.get_all_categories_subcategories, name='category-subcategory-list'),

    # Get all categories
    path('categories/',
         views.get_all_categories, name='category-list'),

    # Get all subcategories under a specified category
    path('subcategories-by-category/<str:category_slug>',
         views.SubcategoriesByCategory.as_view(), name='subcategories-by-category'),


    # Get all occassions list
    path('occasions/', views.get_all_occasions, name="occasions"),

    # Get all recipient types list
    path('recipients/', views.get_all_recipients, name="recipients"),


    # Get single product detail
    path('products/<slug:slug>/', views.product_detail, name='product-detail'),

    # Get all the reviews for a single product
    path('reviews/<slug:product_slug>/', views.get_reviews, name='reviews'),

    # Submit the review
    path('submit-review/', views.submit_review, name='submit_review'),

    # Searching the product
    path('search/', views.ProductSearchView.as_view(), name='product-search'),

    path('products/', views.ProductListView.as_view(), name='product-list'),

]
