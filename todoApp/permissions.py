from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission,SAFE_METHODS
from authentication.models import UserProfile
from .models import Task


class TaskPermission(BasePermission):

    def has_permission(self, request, view):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role in ["CU","AD"]:
           return True
        elif user_profile.role=="ST":
           return request.method in SAFE_METHODS
        return False
    
    def has_object_permission(self, request, view, obj):
        user_profile=UserProfile.objects.get(user=request.user)
        if user_profile.role=="AD":
            return True
        elif user_profile.role=="ST":
            return request.method in SAFE_METHODS
        elif user_profile.role=="CU":
            return obj.user==request.user
        return False
        
