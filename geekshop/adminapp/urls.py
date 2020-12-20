from django.urls import path
import adminapp.views as adminapp

app_name = 'adminappp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.UserListView.as_view(), name='users'),
    path('users/update/<pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('categories/update/<pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/read/<pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/read/category/<pk>/', adminapp.ProductListview.as_view(), name='products'),
    path('products/update/category/<pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/category/<pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),

]
