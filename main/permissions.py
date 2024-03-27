from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):  # т.е. работет на те view, которые привязаны к какому-то объекту
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':                            # создавать могут все
            return True
        print("USER IS AUTHENTICATED: " + str(request.user.is_authenticated))
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and obj.user == request.user
        )


class UserPermission(BasePermission):
    # разрешение на список объектов
    def has_permission(self, request, view):
        if request.method == 'POST':                             # создавать могут все
            return True
        if request.method == 'GET':                               # читать может только админ
            return bool(request.user.is_staff)
        if request.method == 'DELETE' and request.user.is_staff:  # удалять может только админ
            return True

        return False

    # разрешение на отдельный объект
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':  # создавать могут все
            return True
        if request.method == 'GET':  # читать может только владелец или админ
            return bool(request.user and request.user.is_authenticated and request.user.username == str(obj) or request.user.is_staff)
        if request.method == 'PUT':  # изменять может только владелец или админ
            return bool(request.user and request.user.is_authenticated and obj.owner == request.user or request.user.is_staff)
        if request.method == 'DELETE' and request.user.is_staff:  # удалять может только админ
            return True

        return False


class SongPermission(BasePermission):
    # разрешение на список объектов
    def has_permission(self, request, view):
        if request.method == 'POST':                              # создавать могут все
            return True
        if request.method == 'GET':                               # читать могут все
            return True
        if request.method == 'DELETE' and request.user.is_staff:  # удалять может только админ
            return True

        return False

    # разрешение на отдельный объект
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':  # создавать могут все
            return True
        if request.method == 'GET':  # читать могут все
            return True
        if request.method == 'PUT':  # изменять может только владелец или админ
            return bool(request.user and request.user.is_authenticated and obj.owner == request.user or request.user.is_staff)
        if request.method == 'DELETE' and request.user.is_staff:  # удалять может только админ
            return True

        return False
