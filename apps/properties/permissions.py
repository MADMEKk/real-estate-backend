from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAgentOrReadOnly(BasePermission):
    """
    Custom permission to only allow agents to edit, and read-only access to others.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_agent

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it, read-only access to others.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsAdminOrAgent(BasePermission):
    """
    Custom permission to only allow admins or agents to access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_agent)

class IsAgent(BasePermission):
    """
    Custom permission to only allow agents to access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_agent
