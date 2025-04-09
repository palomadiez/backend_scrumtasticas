from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction
from drf_spectacular.utils import extend_schema_field
from .models import Bid

class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuctionListCreateSerializer(serializers.ModelSerializer):
    # Modifica el formato
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ",read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    
    # Campo dinámico
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField()) 
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def validate_closing_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Closing date must be greater than now.")
        return value

class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ",read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField()) 
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def validate_closing_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Closing date must be greater than now.")
        return value
    
class BidSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'