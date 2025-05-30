from django.urls import path
from .views import (
    CategoryListCreate, CategoryRetrieveUpdateDestroy,
    AuctionListCreate, AuctionRetrieveUpdateDestroy,
    BidListCreate, BidRetrieveUpdateDestroy, UserAuctionListView,
    RatingCreateUpdateView, RatingDeleteView,
    CommentListCreateView, CommentRetrieveUpdateDestroyView
)

app_name="auctions"
urlpatterns = [
    # Categorías
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    
    # Subastas
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),

    #Pujas
    path('<int:auction_id>/bid/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),

    # Users
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),

    #Ratings
    path('<int:auction_id>/ratings/', RatingCreateUpdateView.as_view(), name='create_rating'),
    path('<int:auction_id>/ratings/<int:pk>/', RatingDeleteView.as_view(), name='delete_rating'),

    # Comments
    path('<int:auction_id>/comments/', CommentListCreateView.as_view(), name='create_comment'),
    path('<int:auction_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='delete_comment'),

]