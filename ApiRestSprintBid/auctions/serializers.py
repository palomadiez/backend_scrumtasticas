from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Category, Auction, Bid
from drf_spectacular.utils import extend_schema_field

class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate(self, data):
        # Validación de precio
        if data.get("price", 1) <= 0:
            raise serializers.ValidationError({"price": "El precio debe ser un número natural positivo."})
        # Validación de stock
        if data.get("stock", 1) <= 0:
            raise serializers.ValidationError({"stock": "El stock debe ser un número natural positivo."})
        # Validación de valoración
        rating = data.get("rating", None)
        if rating is not None and not (0 <= rating <= 5):
            raise serializers.ValidationError({"rating": "La valoración debe estar entre 0 y 5."})
        # Validación de fechas
        creation = data.get("creation_date", timezone.now())
        closing = data.get("closing_date")
        if closing <= creation:
            raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser posterior a la de creación."})
        if closing <= creation + timedelta(days=15):
            raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser al menos 15 días posterior a la de creación."})
        return data

class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def validate(self, data):
        if data.get("price", 1) <= 0:
            raise serializers.ValidationError({"price": "El precio debe ser un número natural positivo."})
        if data.get("stock", 1) <= 0:
            raise serializers.ValidationError({"stock": "El stock debe ser un número natural positivo."})
        rating = data.get("rating", None)
        if rating is not None and not (0 <= rating <= 5):
            raise serializers.ValidationError({"rating": "La valoración debe estar entre 0 y 5."})
        creation = data.get("creation_date", timezone.now())
        closing = data.get("closing_date")
        if closing <= creation:
            raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser posterior a la de creación."})
        if closing <= creation + timedelta(days=15):
            raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser al menos 15 días posterior a la de creación."})
        return data

class BidSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['auction', 'bidder']
