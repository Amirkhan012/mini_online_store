from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'

    ROLES_USER = [
        (USER, 'User'),
        (EMPLOYEE, 'Employee'),
        (ADMIN, 'Administrator'),
    ]
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        null=False
    )
    password = models.CharField(
        'password',
        max_length=150,
        blank=False
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=100,
        choices=ROLES_USER,
        default=USER
    )
    is_email_verified = models.BooleanField(
        'Подтверждение почты',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username'
    ]

    @property
    def is_admin(self) -> str:
        return self.role == self.ADMIN

    @property
    def is_employee(self) -> str:
        return self.role == self.EMPLOYEE

    class Meta:
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
