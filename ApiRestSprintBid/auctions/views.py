from django.shortcuts import render
from rest_framework import generics
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidSerializer
from django.db.models import Q

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


#Subasta
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
        return queryset
    
class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

# Para pujas
class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction_id=auction_id)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        serializer.save(auction_id=auction_id)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidSerializer

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bid.objects.filter(auction_id=auction_id)

