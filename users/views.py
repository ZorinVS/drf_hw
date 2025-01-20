from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import services
from users.models import User, Payment
from users.permissions import IsModeratorUser, IsProfileOwner, IsStudentUser
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
        if getattr(self, 'swagger_fake_view', False):
            return GuestUserSerializer

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

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        materials = payment.paid_course or payment.paid_lesson

        stripe_service = services.StripeCheckout(content=materials)
        stripe_service.create_product()
        stripe_service.create_price(amount=payment.amount)
        session_id, payment_link = stripe_service.create_session()

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ~IsModeratorUser]
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend,]
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Payment.objects.none()
        return Payment.objects.filter(user=self.request.user)


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudentUser | IsModeratorUser]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Успешный запрос",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'session_id': openapi.Schema(type=openapi.TYPE_STRING, title='ID сессии'),
                        'payment_status': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title='Статус платежа',
                            enum=['unpaid', 'paid'],
                            read_only=True,
                        ),
                    }
                )
            ),
        }
    )
    def get(self, request, session_id):
        try:
            payment = Payment.objects.get(session_id=session_id)
        except Payment.DoesNotExist:
            raise NotFound('Платеж с указанным session_id не найден')

        # Запуск проверки разрешений для конкретного объекта
        obj = payment.paid_course or payment.paid_lesson
        self.check_object_permissions(request, obj)

        payment_status = services.retrieve_payment_status(session_id=session_id)
        if payment.status != payment_status:
            payment.status = payment_status
            payment.save()

        return Response({
            'session_id': session_id,
            'payment_status': payment_status,
        })
