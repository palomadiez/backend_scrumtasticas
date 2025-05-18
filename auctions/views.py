from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django.utils import timezone
from .models import Category, Auction, Bid, Rating, Comment
from .serializers import (CategoryListCreateSerializer,
                          CategoryDetailSerializer, 
                          AuctionListCreateSerializer, 
                          AuctionDetailSerializer,
                          BidListCreateSerializer,
                          BidDetailSerializer,
                          RatingSerializer,
                          CommentListCreateSerializer)

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin

#Categorías
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


#Subastas
class AuctionListCreate(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListCreateSerializer

    def get_queryset(self):
        queryset = Auction.objects.all()
        texto = self.request.query_params.get('texto', None)
        if texto:
            queryset = queryset.filter(
                Q(title__icontains=texto) |
                Q(description__icontains=texto)
            )
        
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(category__name__icontains = categoria)

        precio_min = self.request.query_params.get('precioMin')
        precio_max = self.request.query_params.get('precioMax')
        if precio_min:
            queryset = queryset.filter(price__gte=precio_min)

        if precio_max:
            queryset = queryset.filter(price__lte=precio_max)
        return queryset
    
    
class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

# Pujas
class BidListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BidListCreateSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return Bid.objects.filter(auction_id=auction_id) 
    
    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        auction = get_object_or_404(Auction, id=auction_id)
        serializer.save(auction=auction, bidder=self.request.user)

# Ver, actualizar, eliminar Bid concreta
class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"] 
        return Bid.objects.filter(auction_id=auction_id) 

    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id) 

class BidCreateView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidListCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)


# Users
class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Obtener las subastas del usuario autenticado
        user_auctions = Auction.objects.filter(auctioneer=request.user)
        serializer = AuctionListCreateSerializer(user_auctions, many=True)
        return Response(serializer.data)
    

#Ratings
class RatingCreateUpdateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingDeleteView(generics.DestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


# Comments
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentListCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return Comment.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            last_modification=timezone.now().date())
        
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        serializer.save(last_modification=timezone.now().date())
    