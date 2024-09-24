import re
from rest_framework import serializers
from .models import Customer, HeroSlider, Categories, Product, ProductVariation, ProductImage, Color, Size, ProductOffer, Cart

# Create your serializers here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__' 
    
    def validate_password(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Password should only contain alphabets and numbers.")
        return value

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name should only contain alphabets.")
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name should only contain alphabets.")
        return value
    
    def validate_country(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Country should only contain alphabets.")
        return value
    
    def validate_city(self, value):
        if not value.isalpha(): 
            raise serializers.ValidationError("City should only contain alphabets.")
        return value
    
    def validate_state(self, value):
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("State should only contain alphabets.")
        return value
    
    def validate_address(self, value):
        if not re.match(r'^[a-zA-Z0-9\s/-]+$', value):
            raise serializers.ValidationError("Address contains invalid characters. Only letters, digits, spaces, slashes, hyphens, and periods are allowed.")
        return value
    
    def validate_phone(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("Phone number should only contain digits.")
        return value
    
    def validate_zip(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("Zip number should only contain digits.")
        return value


# HeroSlider Serializer
class HeroSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSlider
        fields = '__all__'


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


# Color Serializer
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

# Size Serializer
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

# Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

# Product Variation Serializer
class ProductVariationSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    size = SizeSerializer()
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    product_image = serializers.CharField(source='product.list_image1', read_only=True)
    short_description = serializers.CharField(source='product.short_description', read_only=True)

    class Meta:
        model = ProductVariation
        fields = ['id', 'color', 'size', 'original_price', 'discount_price', 'stock', 'product_name', 'product_image', 'short_description']

# Product Offer Serializer  
class ProductOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOffer
        fields = '__all__'


# Products Serializer
class ProductSerializer(serializers.ModelSerializer):
    variations = ProductVariationSerializer(many=True, source='productvariation_set')
    images = serializers.SerializerMethodField()
    offer = ProductOfferSerializer(many=True, source='offers')

    class Meta:
        model = Product
        fields = '__all__'

    def get_images(self, obj):
        color = self.context.get('color')
        color_images = ProductImage.objects.filter(product=obj, color=color)
        return ProductImageSerializer(color_images, many=True).data
    

# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    product = ProductVariationSerializer()

    class Meta:
        model = Cart
        fields = '__all__'
