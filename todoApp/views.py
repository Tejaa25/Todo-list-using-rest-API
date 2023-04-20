from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializer import TodoSerializer
from authentication.models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import Http404
from .permissions import TaskPermission
#Project level Permissions is in settings.py:
# AllowAny - everyone
# IsAuthenticated - logged in
# IsAdminUser -is_staff
# IsAuthenticatedOrReadOnly - if the user is not authenticated then he can only read
# Create your views here.

class TodoView(APIView):
    #This is view level permissions
    permission_classes=[IsAuthenticated,TaskPermission]
    authentication_classes=[TokenAuthentication]
    # Authentication determines who the user is 
    # and Permission determines whether the user has the permission to do 
    # what they are trying to do.

    def get(self,request):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=='CU':
            result=Task.objects.filter(user=self.request.user)
        else:
            result=Task.objects.all()
        serializers=TodoSerializer(result,many=True)
        return Response(serializers.data)
            
    def post(self,request):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role in ['CU','AD']:
            data=request.data
            serializer=TodoSerializer(data=data,context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'message':'Staff is not allowed to add'})
    
    def put(self,request):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=='CU' or user_profile.role=='AD':
            data=request.data
            obj=get_object_or_404(Task,id=data["id"])
            # try:
            #   obj=Task.objects.get(id=data['id'])
            # except Task.DoesNotExist:
            #    return Response({'message':"invalid id"},status=status.HTTP_404_NOT_FOUND)
            if obj.user_id==user_profile.user_id or user_profile.role=='AD':
                serializer=TodoSerializer(obj,data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message':"error in updating"})
            else:
                return Response({'message':'you can update only your tasks'})
        else:
            return Response({'message':'Staff is not allowed to update'})
    
    def patch(self,request):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=='CU' or user_profile.role=='AD':
            data=request.data 
            obj=get_object_or_404(Task,id=data["id"])
            if obj.user_id==user_profile.user_id or user_profile.role=='AD':
                serializer=TodoSerializer(obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message':'add a valid details'})
            else:
                return Response({'message':'you can update only your tasks'})
        else:
            return Response({'message':'Staff is not allowed to update'})
        
    def delete(self,request):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=='CU' or user_profile.role=='AD':
            data=request.data
            obj=get_object_or_404(Task,id=data["id"])
            if obj.user_id==user_profile.user_id or user_profile.role=='AD':
                obj.delete()
                return Response({'message':'task deleted'})
            else:
                return Response({'message':'You can delete only your own task'})
            
        else:
            return Response({'message':'Staff is not allowed to delete'})
        
class TaskView(APIView):
    permission_classes=[IsAuthenticated,TaskPermission]
    authentication_classes=[TokenAuthentication]

    def get(self,request,slug_text):
        result=get_object_or_404(Task,slug=slug_text)
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=='CU':
            if user_profile.user_id==result.user_id:
                serializers=TodoSerializer(result)
                return Response(serializers.data)
            else:
                raise Http404
        else:
            serializers=TodoSerializer(result)
            return Response(serializers.data)
    def put(self,request,slug_text):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=='CU' or user_profile.role=='AD':
            data=request.data
            obj=get_object_or_404(Task,slug=slug_text)
            if obj.user_id==user_profile.user_id or user_profile.role=='AD':
                serializer=TodoSerializer(obj,data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response({'message':"error in updating"})
            else:
                return Response({'message':'you can update only your tasks'})
        else:
            return Response({'message':'Staff is not allowed to update'})

    

