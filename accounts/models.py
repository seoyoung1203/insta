from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# user 지정 공간
# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='profile',
    )
# 내가 팔로우 하는 사람
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False) # 유저와 유저를 n:n으로 연결(스스로를) 팔로우 버튼 누른 사람 저장 버튼

# 나를 팔로우 하는 사람