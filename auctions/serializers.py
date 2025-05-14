from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Category, Auction, Bid, Rating
from drf_spectacular.utils import extend_schema_field
from django.db import models
from django.db.models import Avg


# Category
class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Subasta
class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def get_rating(self, obj):
        avg = obj.ratings.aggregate(avg=Avg('score'))['avg']
        return round(avg, 2) if avg is not None else 1

    def validate(self, data):
        print("DATA", data)
        # Validación de precio
        if data.get("price", 1) <= 0:
            raise serializers.ValidationError({"price": "El precio debe ser un número natural positivo."})
        # Validación de stock
        if data.get("stock", 1) <= 0:
            raise serializers.ValidationError({"stock": "El stock debe ser un número natural positivo."})
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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()
    
    def get_rating(self, obj):
        avg = obj.ratings.aggregate(avg=Avg('score'))['avg']
        return round(avg, 2) if avg is not None else 0

    def validate(self, data):
        if data.get("price", 1) <= 0:
            raise serializers.ValidationError({"price": "El precio debe ser un número natural positivo."})
        if data.get("stock", 1) <= 0:
            raise serializers.ValidationError({"stock": "El stock debe ser un número natural positivo."})
        creation = data.get("creation_date", timezone.now())
        closing = data.get("closing_date")
        if closing <= creation:
            raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser posterior a la de creación."})
        if closing <= creation + timedelta(days=15):
            raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser al menos 15 días posterior a la de creación."})
        return data


# Puja
class BidDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "auction", "price", "creation_date", "bidder_username"]
        #read_only_fields = ['auction_id', 'bidder']

    def get_bidder_username(self, obj):
        return obj.bidder.username
    
class BidListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "auction", "price", "creation_date", "bidder_username"]
        read_only_fields = ['bidder_username']

    def get_bidder_username(self, obj):
        return obj.bidder.username

    def validate(self, data):
        auction = data['auction']
        price = data['price']

        if price <= 0:
            raise serializers.ValidationError("El precio de la puja debe ser un número positivo.")
        
        max_bid = Bid.objects.filter(auction=auction).aggregate(models.Max('price'))['price__max']
        if max_bid is not None and price <= max_bid:
            raise serializers.ValidationError("La puja debe ser mayor que las existentes.")
        
        if auction.closing_date <= timezone.now():
            raise serializers.ValidationError("La subasta ya ha cerrado, no se puede pujar.")
        
        return data
    
    def create(self, validated_data):
        validated_data['bidder'] = self.context['request'].user
        return super().create(validated_data)

# Rating
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'auction', 'score']
        read_only_fields = ['user']  # el usuario se asigna automáticamente desde la request

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("La puntuación debe estar entre 1 y 5.")
        return value
    

    def create(self, validated_data):
        # Si ya existe una valoración del usuario para la subasta, la sustituimos (update)
        instance, created = Rating.objects.update_or_create(
            user=self.context['request'].user,
            auction=validated_data['auction'],
            defaults={'score': validated_data['score']}
        )
        return instance

    def update(self, instance, validated_data):
        # Actualizar la puntuación y recalcular el rating promedio
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance
    