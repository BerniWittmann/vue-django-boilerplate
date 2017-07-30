from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from authemail.views import Login, Logout, PasswordResetVerified, UserMe
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .serializers import UserSerializer
from authemail.models import PasswordResetCode

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CustomLogin(Login):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)

            if user:
                if user.is_verified:
                    if user.is_active:
                        payload = jwt_payload_handler(user)
                        token = jwt_encode_handler(payload)
                        return Response({'token': token},
                                        status=status.HTTP_200_OK)
                    else:
                        content = {'detail': _('User account not active.')}
                        return Response(content,
                                        status=status.HTTP_401_UNAUTHORIZED)
                else:
                    content = {'detail':
                                   _('User account not verified.')}
                    return Response(content, status=status.HTTP_401_UNAUTHORIZED)
            else:
                content = {'detail':
                               _('Unable to login with provided credentials.')}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CustomLogout(Logout):
    def get(self, request, format=None):
        """
        Remove all auth tokens owned by request.user.
        """
        content = {'success': _('User logged out.')}
        return Response(content, status=status.HTTP_200_OK)


class CustomPasswordResetVerified(PasswordResetVerified):
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data['code']
            password = serializer.data['password']

            try:
                password_reset_code = PasswordResetCode.objects.get(code=code)
                password_reset_code.user.set_password(password)
                password_reset_code.user.save()
                password_reset_code.delete()
                content = {'success': _('Password reset.')}
                return Response(content, status=status.HTTP_200_OK)
            except PasswordResetCode.DoesNotExist:
                content = {'detail': _('Unable to verify user.')}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CustomUserMe(UserMe):
    serializer_class = UserSerializer
