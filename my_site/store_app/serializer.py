from .models import (Category, Product , SubCategory, Favorite, FavoriteItem,
                     UserProfile, ProductImage, Review, Cart, CartItem)
from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    # def to_representation(self, instance):
    #     refresh = RefreshToken.for_user(instance)
    #     return {
    #         'user': {
    #             'username': instance.username,
    #             'email': instance.email,
    #         },
    #         'access': str(refresh.access_token),
    #         'refresh': str(refresh),
    #     }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','subcategory_name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategorySerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['category_name', 'category_sub']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']


class ProductListSerializer(serializers.ModelSerializer):
    product_photo = ProductImageSerializer(read_only=True, many=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_photo', 'product_name', 'price', 'avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

class SubCategoryDetailSerializer(serializers.ModelSerializer):
    sub_product = ProductListSerializer(read_only=True, many=True)
    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'sub_product']

class ReviewSerializer(serializers.ModelSerializer):
    сreated_date = serializers.DateField(format='%d-%m-%Y')
    user = UserProfileNameSerializer()
    class Meta:
        model = Review
        fields = ['user', 'star', 'text', 'сreated_date']



class ProductDetailSerializer(serializers.ModelSerializer):
    product_photo = ProductImageSerializer(read_only=True, many=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    product_review = ReviewSerializer(read_only=True, many=True)
    сreated_date = serializers.DateField(format='%d-%m-%Y')
    subcategory = SubCategorySerializer()
    class Meta:
        model = Product
        fields = ['subcategory', 'product_photo', 'product_name', 'product_type', 'price', 'avg_rating',
                  'get_count_people', 'article', 'description', 'video', 'сreated_date', 'product_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'user', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')

    class Meta:
        model = FavoriteItem
        fields = ['id', 'product', 'product_id']

class FavoriteSerializer(serializers.ModelSerializer):
    like = FavoriteItemSerializer(many=True, read_only=True)
    class Meta:
        model = Favorite
        fields = ['id', 'like', 'user']
