
from django.contrib import admin
from django.urls import include,path
from  . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('authentication/',include("authentication.urls")),
    path('products/<name>',views.productview,name='products'),
    path('category/',views.category,name='Category'),
    path('cart/', views.addcart, name='cart'),
    path('cartview/', views.cartview, name='cartview'),
    path('removecart/<id>', views.remove_cart, name='removecart'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlistview/',views.viewWishlist,name='viewwishlist'),
    path('removewishlist/<id>',views.remove_wishlist,name='removewishlist'),
    path('productdetail/<name>',views.productdetails,name='productdetails'),
  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
