from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404

from apps.auth_app.models import AuthUser
from apps.auth_app.serializers import UserCreateSerializer


class CustomerCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerViewAll(generics.GenericAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        users = AuthUser.objects.all()
        
        serializer = self.serializer_class(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomerByIdView(generics.GenericAPIView):
    queryset = AuthUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        user = get_object_or_404(AuthUser, pk=pk)
        
        serializer = self.serializer_class(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)