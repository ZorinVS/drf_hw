from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    city = models.CharField(max_length=150, verbose_name='город', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CASH = 'cash'
    PAYMENT_TRANSFER = 'transfer'

    PAYMENT_CHOICES = [
        (PAYMENT_CASH, 'Наличные'),
        (PAYMENT_TRANSFER, 'Перевод на счет'),
    ]

    STATUS_UNPAID = 'unpaid'
    STATUS_PAID = 'paid'

    STATUS_CHOICES = [
        (STATUS_UNPAID, 'не оплачено'),
        (STATUS_PAID, 'оплачено'),
    ]

    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='payments', blank=True, null=True, verbose_name='оплаченный курс'
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='payments', blank=True, null=True, verbose_name='оплаченный урок'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма')
    payment_method = models.CharField(
        max_length=9, choices=PAYMENT_CHOICES, default=PAYMENT_TRANSFER, verbose_name='способ оплаты'
    )
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name='ссылка на оплату')
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default=STATUS_UNPAID, verbose_name='статус платежа'
    )

    def __str__(self):
        return f'Платеж {self.user} за {self.paid_course if self.paid_course else self.paid_lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
