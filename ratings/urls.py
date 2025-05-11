from django.urls import path
from .views import RatingCreateUpdateView, RatingDeleteView

urlpatterns = [
    path('auctions/<int:auction_id>/ratings/', RatingCreateUpdateView.as_view(), name='create_rating'),
    path('auctions/<int:auction_id>/ratings/<int:pk>/', RatingDeleteView.as_view(), name='delete_rating'),
]
