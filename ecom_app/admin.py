from django.contrib import admin
from .models import Customer,Categories,Product,Color,Size,ProductImage,ProductOffer,Cart,HeroSlider,CategorySlider,ProductVariation

# Register your models here.

# Register Customer 
@admin.register(Customer)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'state')

# Register Categories
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_image')

# Register Product
@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id','sku', 'product_name')

# Register Color
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'color')

# Register Size
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size')

# Register Product Variation
@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'discount_price', 'stock')

# Register Product Image
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'image')

# Register Product Offer
@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('offer', 'Terms_Condition')

# Register Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity')

# Register Hero Slider
@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url')

# Register Category Slider
@admin.register(CategorySlider)
class CategorySliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')