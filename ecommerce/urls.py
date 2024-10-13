from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ecom_app.views import RegisterView,LoginView,LogoutView,ProfileView,ChangePasswordView,HeroSliderView,CategoryView,ProductView,ProductDetailView,AddToCartView,CarttView,DeleteFromCartView,UpdateCartView,ShipmentAddressView,PaymentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/', ChangePasswordView.as_view(), name='password'),
    path('heroSlider/', HeroSliderView.as_view(), name='hero_slider'),
    path('category/', CategoryView.as_view(), name='category'),
    path('products/', ProductView.as_view(), name='product'),
    path('productdetail/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CarttView.as_view(), name='cart'),
    path('cart/update/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/delete/<int:item_id>/', DeleteFromCartView.as_view(), name='delete-cart-item'),
    path('shipment-address/', ShipmentAddressView.as_view(), name='shipment-address'),
    path('payment/', PaymentView.as_view(), name='payment'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)