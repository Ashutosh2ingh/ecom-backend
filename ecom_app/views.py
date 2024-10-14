from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import Customer, HeroSlider, Categories, Product, ProductVariation, Cart, ShipmentAddress, Payment, Order
from .serializers import UserSerializer, HeroSliderSerializer, CategorySerializer, ProductSerializer, CartSerializer, ShipmentAddressSerializer, PaymentSerializer, OrderSerializer

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
        

# Payment View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PaymentView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        amount = data.get('amount')
        payment_status = data.get('payment_status', 'Pending')
        razorpay_payment_id = data.get('razorpay_payment_id')

        if not amount:
            return Response({
                'status': '400',
                'message': 'Amount is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not razorpay_payment_id:
            return Response({
                'status': '400',
                'message': 'Razorpay payment ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        payment, created = Payment.objects.get_or_create(
            customer=user,
            amount=amount,
            payment_status=payment_status,
            razorpay_payment_id=razorpay_payment_id,
        )

        if not created:
            return Response({
                'status': '400',
                'message': 'Payment already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentSerializer(payment)
        return Response({
            'status': 200,
            'message': 'Payment created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
  

# Order View
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateOrderView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        payment_id = data.get('payment_id')
        product_variation_id = data.get('product_variation_id')
        quantity = data.get('quantity')

        if not payment_id:
            return Response({
                'status': '400',
                'message': 'Payment ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not product_variation_id:
            return Response({
                'status': '400',
                'message': 'Product variation ID is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not quantity:
            return Response({
                'status': '400',
                'message': 'Quantity is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(razorpay_payment_id=payment_id, customer=user)
        except Payment.DoesNotExist:
            return Response({
                'status': '404',
                'message': 'Payment not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            product_variation = ProductVariation.objects.get(id=product_variation_id)
        except ProductVariation.DoesNotExist:
            return Response({
                'status': '404',
                'message': 'Product variation not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        if product_variation.stock < quantity:
            return Response({
                'status': '400',
                'message': 'Not enough stock available.'
            }, status=status.HTTP_400_BAD_REQUEST)

        order, created = Order.objects.get_or_create(
            customer=user,
            payment=payment,
            product_variation=product_variation,
            quantity=quantity,
            defaults={
                'total_amount': product_variation.discount_price * quantity,
                'order_status': 'Processing'
            }
        )

        if not created:
            return Response({
                'status': '400',
                'message': 'Order already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update stock
        product_variation.stock -= quantity
        product_variation.save()

        serializer = OrderSerializer(order)
        return Response({
            'status': 200,
            'message': 'Order Placed successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)