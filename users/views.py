from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import IsModeratorUser, IsProfileOwner
from users.serializers import UserCreateSerializer, PaymentSerializer, UserSerializer, GuestUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # на случай изменения DEFAULT_PERMISSION_CLASSES в settings.py
    serializer_class = UserCreateSerializer


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestUserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        else:
            return GuestUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]
    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ~IsModeratorUser]
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ~IsModeratorUser]
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend,]
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson')

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
