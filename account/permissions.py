from rest_framework.permissions import BasePermission, SAFE_METHODS

# ---------------------------------------------------------
# ONLY TEACHER
# ---------------------------------------------------------
class IsTeacher(BasePermission):
    """
    Allows access only to authenticated teachers.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )


# ---------------------------------------------------------
# ONLY STUDENT
# ---------------------------------------------------------
class IsStudent(BasePermission):
    """
    Allows access only to authenticated students.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'student'
        )


# ---------------------------------------------------------
# ONLY ADMIN
# ---------------------------------------------------------
class IsAdmin(BasePermission):
    """
    Allows access only to authenticated admins.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


# ---------------------------------------------------------
# ADMIN + TEACHER (useful for some views)
# ---------------------------------------------------------
class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.role == 'teacher')
        )
