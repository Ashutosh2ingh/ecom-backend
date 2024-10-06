from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import Customer, HeroSlider, Categories, Product, ProductVariation, Cart, ShipmentAddress
from .serializers import UserSerializer, HeroSliderSerializer, CategorySerializer, ProductSerializer, CartSerializer, ShipmentAddressSerializer

# Create Register View
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = Customer.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                country=user_data['country'],
                address=user_data['address'],
                city=user_data['city'],
                state=user_data['state'],
                zip=user_data['zip'],
                phone=user_data['phone']
            )
            return Response({
                'status': 200,
                'message': 'Registration Successful',
            })
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'error': serializer.errors
        })


# Create Login View
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 200,
                'message': 'Login Successful',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'token': token.key
            })
        return Response({
            'status': 400,
            'message': 'Invalid credentials'
        })
    

# Create Logout View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({
            "status": 200,
            "message": "Logout Successful"
        })


# Profile View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "country": user.country,
            "address": user.address,
            "city": user.city,
            "state": user.state,
            "zip": user.zip,
            "phone": user.phone,
        }
        return Response(profile)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "Profile updated successfully"
            })
        return Response({
            "status": 400,
            "error": serializer.errors
        }, status=400)
    

# Change Password View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')

        if not check_password(old_password, user.password):
            return Response({"message": "Old password is incorrect"}, status=400)

        serializer = UserSerializer()

        try:
            serializer.validate_password(new_password)
        except serializer.ValidationError as e:
            return Response({
                "status": 400,
                "message": e.detail[0] if isinstance(e.detail, list) else e.detail
            })

        user.set_password(new_password)
        user.save()

        return Response({
            "status": 200,
            "message": "Password changed Successfully",
        })


# Hero Slider View
class HeroSliderView(generics.ListAPIView):
    queryset = HeroSlider.objects.all()
    serializer_class = HeroSliderSerializer


# Category View
class CategoryView(generics.ListAPIView):   
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


# Product View
class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Product Detail View
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['color'] = self.request.query_params.get('color')
        return context
    

# Create Add to Cart View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        product_variation_id = request.data.get('product_variation_id')
        quantity = request.data.get('quantity')

        if not product_variation_id:
            return Response({
                'status': '400', 
                'message': 'Product variation ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_variation = ProductVariation.objects.get(id=product_variation_id)
        except ProductVariation.DoesNotExist:
            return Response({
                'status': '404', 
                'message': 'Product variation not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = Cart.objects.get_or_create(
            customer=user,
            product=product_variation,
            defaults={'quantity': 0}
        )

        # Update quantity
        cart_item.quantity += quantity
        cart_item.save()

        return Response({
            'status': 200,
            'message': 'Item added to cart successfully.',
            'cart_item': {
                'product': cart_item.product.id,
                'quantity': cart_item.quantity
            }
        }, status=status.HTTP_200_OK)


# Cart View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CarttView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)


# Update Cart View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UpdateCartView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        product_variation_id = request.data.get('product_variation_id')
        quantity = request.data.get('quantity')

        if not product_variation_id:
            return Response({
                'status': '400',
                'message': 'Product variation ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity is None:
            return Response({
                'status': '400',
                'message': 'Quantity is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product_variation = ProductVariation.objects.get(id=product_variation_id)
        except ProductVariation.DoesNotExist:
            return Response({
                'status': '404',
                'message': 'Product variation not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_item = Cart.objects.get(customer=user, product=product_variation)
        except Cart.DoesNotExist:
            return Response({
                'status': '404',
                'message': 'Cart item not found for the given user and product.'
            }, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            cart_item.delete()  # If quantity is zero or less, remove the item from the cart
            return Response({
                'status': '200',
                'message': 'Item removed from cart as quantity'
            }, status=status.HTTP_200_OK)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({
            'status': 200,
            'message': 'Cart item updated successfully.',
            'cart_item': {
                'product': cart_item.product.id,
                'quantity': cart_item.quantity
            }
        }, status=status.HTTP_200_OK)
    

# Delete Item from Cart View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
class DeleteFromCartView(APIView):

    def delete(self, request, item_id, *args, **kwargs):
        user = request.user
        try:
            cart_item = Cart.objects.get(id=item_id, customer=user)
            cart_item.delete()
            return Response({
                "status": 200,
                "message": "Cart item deleted successfully."
            }, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Cart item not found."
            }, status=status.HTTP_404_NOT_FOUND)


# Shipment Address View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
class ShipmentAddressView(APIView):

    def get(self, request):
        try:
            address = ShipmentAddress.objects.get(customer=request.user)
            serializer = ShipmentAddressSerializer(address)
            return Response(serializer.data)
        except ShipmentAddress.DoesNotExist:
            return Response(
                {"message": "No shipment address found."}, 
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data.copy()
        data['customer'] = request.user.id  

        try:
            address = ShipmentAddress.objects.get(customer=request.user)
            serializer = ShipmentAddressSerializer(address, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message":"Shipment Details Updated Successfully",
                        "data":serializer.data, 
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                error=serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except ShipmentAddress.DoesNotExist:
            serializer = ShipmentAddressSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message":"Shipment Details Created Successfully",
                        "data":serializer.data, 
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                error=serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )