from rest_framework import generics, status
from rest_framework.response import Response

from apps.auth_app.serializers import UserCreateSerializer


class UserSerializer(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)