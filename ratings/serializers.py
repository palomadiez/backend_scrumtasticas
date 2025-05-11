from rest_framework import serializers
from .models import Rating

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
