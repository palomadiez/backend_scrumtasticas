from rest_framework import serializers
from .models import CustomUser
from datetime import date
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'confirm_password',
          'birth_date', 'municipality', 'locality')
        extra_kwargs = {'password': {'write_only': True}}

    # Validar email
    def validate_email(self, value):
        user = self.instance
        if not value.endswith("@comillas.edu"):
            raise serializers.ValidationError("El correo debe ser @comillas.edu")
        
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Este correo ya está en uso.")
        return value
    
    # Validar edad
    def validate_birth_date(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Debes tener al menos 18 años.")
        return value
    
    #Validar contraseña
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial.")
        
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(f"Error de validación de contraseña: {e.messages}")
        
        return value
    
    # Confirmar que las contraseñas coinciden
    def validate(self, data):
        print("---------------DATA---------------", data)
        password = data.get("password")
        confirm = data.get("confirm_password")

        if password != confirm:
            raise serializers.ValidationError({"confirm_password": "Las contraseñas no coinciden."})
        return data
    
    
    def create(self, validated_data):
       validated_data.pop('confirm_password', None)
       return CustomUser.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
