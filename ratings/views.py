from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Rating
from .serializers import RatingSerializer

class RatingCreateUpdateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingDeleteView(generics.DestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
