from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class LedgerInfo(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ledger_info', verbose_name='归属用户')

    class Meta:
        verbose_name = '账本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AccountEntry(models.Model):
    theoretical_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='理论收入')
    actual_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='实际收入')
    theoretical_expenditure = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='理论支出')
    actual_expenditure = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='实际支出')
    theoretical_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='理论余额')
    actual_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='实际余额')
    difference = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='差额', editable=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    remark = models.TextField(blank=True, verbose_name='备注')
    account_book = models.ForeignKey(LedgerInfo, on_delete=models.CASCADE, related_name='entries',
                                     verbose_name='归属账本')

    def __str__(self):
        return f"账目记录 - {self.created_at.date()}"
