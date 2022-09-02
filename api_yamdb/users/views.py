import uuid
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .serializers import (
    SendCodeSerializer, CheckCodeSerializer, UserSerializer)
from api.permissions import (
    IsAdmin,
)
from .models import User
from api_yamdb.settings import FROM_EMAIL


@api_view(['POST'])
def send_confirmation_code(request):
    '''
    Генерирует код, привязывает его к юзеру и
    отправляет его на почту пользователя.
    Код доступен в корне в папке sent_emails
    '''
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if not User.objects.filter(username=username, email=email).exists():
        if (
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()
        ):
            return Response(
                {"result": "Этот email или username уже используются."},
                status=status.HTTP_400_BAD_REQUEST
            )
        User.objects.create_user(username=username, email=email)
    user = User.objects.get(username=username)
    user.confirmation_code = uuid.uuid4()
    user.save()
    send_mail(
        'Подтверждение аккаунта на Yamdb',
        f'Код подтверждения: {user.confirmation_code}',
        FROM_EMAIL,
        [email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    '''
    Достает введеный код и сверяет с присвоенным юзеру.
    Возвращает токен для авторизации.
    '''
    serializer = CheckCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    '''
    Получение всех юзеров от имени админа.
    Создание/изменение/удаление/получение юзера по
    username вроде должно работать.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]


class UserDetailPach(APIView):
    '''
    Работа с эндпоинтом <users/me/>.
    Получение и изменение детальной информации о себе.
    '''
    def get(self, request):
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
