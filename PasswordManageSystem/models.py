from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PasswordInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    website = models.URLField(blank=True, verbose_name='网址')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_info', verbose_name='归属用户')

    class Meta:
        verbose_name = '密码信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
