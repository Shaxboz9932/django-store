from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', null=True, blank=True)
    is_verification = models.BooleanField(default=False)

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email verification for {self.user.email}'

    def send_email_verification(self):
        link = reverse('users:email_verify', kwargs={'email': self.user.email, 'code': self.code})
        verify_link = f'http://localhost:8000/{link}'
        subject = f'Verify your email {self.user.email}'
        message = f'Aktivlash uchun quyidagi manzilga uting {verify_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email='from@mail.ru',
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expire(self):
        return True if now() >= self.expiration else False




