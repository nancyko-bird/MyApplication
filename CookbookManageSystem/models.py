from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
# 定义食材模型
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    # 定义菜谱模型


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    steps = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes_info', verbose_name='归属用户')

    def __str__(self):
        return self.name
