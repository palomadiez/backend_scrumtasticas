from django.urls import path
from .views import (
    CategoryListCreate, CategoryRetrieveUpdateDestroy,
    AuctionListCreate, AuctionRetrieveUpdateDestroy,
    BidListCreate, BidRetrieveUpdateDestroy
)

app_name="auctions"
urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),

    #Pujas
    path('<int:auction_id>/bid/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),
]