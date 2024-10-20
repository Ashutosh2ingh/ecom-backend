from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.

# User Manager Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Customer Model
class Customer(AbstractUser):
    username = None 
    email = models.EmailField(_('email address'), unique=True, max_length=191) 
    first_name = models.CharField(max_length=191)
    last_name = models.CharField(max_length=191)
    password = models.CharField(max_length=191)
    country = models.CharField(max_length=191,default='')
    address = models.CharField(max_length=191,default='')
    city = models.CharField(max_length=191,default='')
    state = models.CharField(max_length=191,default='')
    zip = models.IntegerField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name
    

# Categories Model
class Categories(models.Model):
    category_name = models.CharField(max_length=191)
    category_image = models.ImageField(upload_to='category/', max_length=191)

    def __str__(self):
        return self.category_name
    

# Product Model
class Product(models.Model):
    sku = models.CharField(max_length=191, unique=True)
    product_name = models.CharField(max_length=191)
    category = models.ManyToManyField(Categories)
    new = models.BooleanField(default=False) 
    featured = models.BooleanField(default=False) 
    short_description = models.TextField()
    full_description = models.TextField()
    replacement = models.TextField(null=True)
    list_image1 = models.ImageField(upload_to='productlist/', max_length=191, null=True, blank=True)
    list_image2 = models.ImageField(upload_to='productlist/', max_length=191, null=True, blank=True)

    def __str__(self):
        return self.product_name
    

# Color Model
class Color(models.Model):
    color = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.color


# Size Model
class Size(models.Model):
    size = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.size


# Product Variation Model
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'color', 'size'], name='unique_product_color_size')
        ]

    def __str__(self):
        return f'{self.product.product_name} - {self.color.color} - {self.size.size}'


# Product Image Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name='color_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', max_length=191)

    def __str__(self):
        return f'{self.product.product_name} - {self.color.color} Image'


# Product Offers Model
class ProductOffer(models.Model):
    offer = models.CharField(max_length=191)
    Terms_Condition = models.TextField(null=True)
    products = models.ManyToManyField(Product, related_name='offers')

    def __str__(self):
        return self.offer


# Cart Item Model
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product} for {self.customer}'
    

# Hero Slider Model
class HeroSlider(models.Model):
    title = models.CharField(max_length=191)
    description = models.CharField(max_length=191)
    image = models.ImageField(upload_to='heroSlider/', max_length=191)
    url = models.CharField(max_length=191)
    bg = models.CharField(max_length=191)

    def __str__(self):
        return self.title
    

# Category Slider Model
class CategorySlider(models.Model):
    title = models.CharField(max_length=191)
    image = models.ImageField(upload_to='categorySlider/', max_length=191)

    def __str__(self):
        return self.title
    

# Shipment Address Model
class ShipmentAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=191)
    email = models.EmailField(max_length=191)
    phone = models.CharField(max_length=20)
    flat_building_no = models.CharField(max_length=191) 
    city = models.CharField(max_length=191)
    pincode = models.IntegerField()
    state = models.CharField(max_length=191)
    country = models.CharField(max_length=191)

    def __str__(self):
        return f'Shipping Address for {self.customer.first_name} {self.customer.last_name}'


# Order Model
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')
    razorpay_payment_id = models.CharField(max_length=255, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.razorpay_payment_id} for {self.customer.first_name}'


# Order Model
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )
    order_date = models.DateTimeField(default=timezone.now)
    order_status_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update order_status_date if order_status is changed
        if self.pk is not None:  # Check if the instance already exists
            original = Order.objects.get(pk=self.pk)
            if original.order_status != self.order_status:
                self.order_status_date = timezone.now()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.order_id} by {self.customer.email}'