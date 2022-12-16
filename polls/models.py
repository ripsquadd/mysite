import datetime

from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from mysite import settings


def validate_image(fieldfile_obj):
    size_of_file = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if size_of_file > megabyte_limit * 1024 * 1024:
        raise ValidationError('Максимальный размер файла %sMB' % str(megabyte_limit))


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    short_detail = models.CharField(max_length=500, blank=True)
    detail = models.CharField(max_length=2000, blank=True)
    photo = models.ImageField(upload_to="img/",
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                          validate_image], blank=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


# class Choice(models.Model): ОРИГИНАЛ
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Voter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


# https://habr.com/ru/sandbox/164517/
# https://habr.com/ru/company/leader-id/blog/501570/


class User(AbstractUser):
    first_name = models.CharField(max_length=150, verbose_name='Имя', null=False, blank=False)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', null=True, blank=True)
    second_name = models.CharField(max_length=150, verbose_name='Отчество', null=False, blank=False)
    username = models.CharField(max_length=150, verbose_name='Логин', unique=True, null=False, blank=False)
    photo = models.ImageField(upload_to="img/",
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                          validate_image], blank=False)
    email = models.CharField(max_length=150, verbose_name='Почта', unique=True, null=False, blank=False)
    password = models.CharField(max_length=150, verbose_name='Пароль', null=False, blank=False)
    personal_data = models.BooleanField(default=False, blank=False, null=False,
                                        verbose_name='Согласие на обработку персональных данных')

    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошел активацию?')

    USERNAME_FIELD = 'username'

    class Meta(AbstractUser.Meta):
        pass
