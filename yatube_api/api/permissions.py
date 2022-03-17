from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Полный доступ к объекту только у его автора.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
