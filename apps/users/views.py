# views.py
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserViewSet(UserViewSet):

    @action(["post"], detail=False, url_path="activate")
    def activate(self, request, *args, **kwargs):
        response = super().activate(request, *args, **kwargs)
        if response.status_code == 204:
            user = self.get_user(request)
            refresh = RefreshToken.for_user(user)

            # Return tokens as JSON
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return response

    def get_user(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        user = self.get_serializer().validate_uid_token(uid, token)['user']
        return user
