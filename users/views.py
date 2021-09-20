from api_yamdb import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsOwner
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'

    def partial_update(self, request, username):
        user = get_object_or_404(User, username=username)
        role = request.data.get('role')
        if role is not None:
            if role == User.ADMIN:
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsOwner,),
    )
    def me(self, request):
        if self.request.method == 'PATCH':
            instance = self.request.user
            serializer = self.get_serializer(instance, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        self.send_mail(email)
        return Response(
            {'info': 'Confirmation code was sent to your email'},
            status=status.HTTP_201_CREATED
        )

    def send_mail(self, email):
        confirmation_code = make_password(email, salt=None, hasher='default')
        subject = 'Confirmation code from YaMDb'
        body = f'Your confirmation code is {confirmation_code}'
        email_from = settings.EMAIL_FROM
        email_to = email
        send_mail(
            subject,
            body,
            email_from,
            [email_to],
            fail_silently=False,
        )


class TokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = User.objects.get_or_create(
            username=username, email=email)
        data = self.get_tokens_for_user(user)

        return Response(data, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
