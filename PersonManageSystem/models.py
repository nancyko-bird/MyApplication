from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class PersonInfo(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name='姓名')
    pid = models.CharField(max_length=255, verbose_name='身份证号')
    birth = models.CharField(max_length=255, verbose_name='出生日期')
    birth_address = models.CharField(max_length=255, verbose_name='籍贯')
    age = models.CharField(max_length=255, verbose_name='年龄')
    gender = models.CharField(max_length=255, verbose_name='性别')
    address = models.CharField(max_length=255, verbose_name='现居地')
    phone = models.CharField(max_length=255, verbose_name='电话')
    identity = models.CharField(max_length=255, verbose_name='身份')
    relation = models.CharField(max_length=255, verbose_name='关系')
    hobby = models.CharField(max_length=255, verbose_name='爱好')
    company = models.CharField(max_length=255, verbose_name='公司')
    personality = models.CharField(max_length=255, verbose_name='性格')
    correlation_degree = models.CharField(max_length=255, verbose_name='关联度')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', verbose_name='归属用户')

    def __str__(self):
        return self.name
