from rest_framework import serializers
from rest_framework import serializers,status
from rest_framework.validators import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from . models import AuthUser

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=100)
    phone_number = PhoneNumberField(allow_blank=False, allow_null=False)
    password=serializers.CharField(allow_blank=False,write_only=True)
    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'phone_number', 'password']
        
    # create custom validation for email, username
    
    def validate(self, attrs):
        email = AuthUser.objects.filter(email=attrs['email']).exists()
        if email:
            raise ValidationError({
                "success": False,
                "message": "Email already exists"
                }, code=status.HTTP_403_FORBIDDEN
            )
        
        
        username = AuthUser.objects.filter(username=attrs['username']).exists()
        if username:
            raise ValidationError({
                "success": False,
                "message": "Username already exists"
                },code=status.HTTP_403_FORBIDDEN
            )
        
        phone_number = AuthUser.objects.filter(phone_number=attrs['phone_number']).exists()
        if phone_number:
            raise ValidationError({
                "success": False,
                "message": "Pnone number already exists"
                },code=status.HTTP_403_FORBIDDEN
            )
        
        return super().validate(attrs)
    
    def create(self,validated_data):
        new_user=AuthUser(**validated_data)

        new_user.password=make_password(validated_data.get('password'))

        new_user.save()

        return new_user