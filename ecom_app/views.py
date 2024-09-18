from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import Customer, HeroSlider, Categories, Product
from .serializers import UserSerializer, HeroSliderSerializer, CategorySerializer, ProductSerializer

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