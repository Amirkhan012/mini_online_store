from rest_framework import permissions

from .models import User


class IsEmailVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_email_verified
        )


class IsEmployeeOrHigherChange(permissions.BasePermission):
    """
    Доступ разрешен только сотрудникам и
    администраторам для создания, обновления и удаления.
    """
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return bool(
                request.user and request.user.is_authenticated and
                request.user.role in [User.EMPLOYEE, User.ADMIN]
            )
        return True


class IsUserOrHigher(permissions.BasePermission):
    """
    Доступ разрешен всем пользователям и выше.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role in [User.USER, User.EMPLOYEE, User.ADMIN]
        )
