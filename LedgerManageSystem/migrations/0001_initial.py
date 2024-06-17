# Generated by Django 5.0.2 on 2024-03-14 15:35

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='名称')),
                ('notes', models.TextField(blank=True, verbose_name='备注')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_info', to=settings.AUTH_USER_MODEL, verbose_name='归属用户')),
            ],
            options={
                'verbose_name': '账本信息',
                'verbose_name_plural': '账本信息',
            },
        ),
        migrations.CreateModel(
            name='AccountEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theoretical_income', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='理论收入')),
                ('actual_income', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='实际收入')),
                ('theoretical_expenditure', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='理论支出')),
                ('actual_expenditure', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='实际支出')),
                ('theoretical_balance', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='理论余额')),
                ('actual_balance', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='实际余额')),
                ('difference', models.DecimalField(decimal_places=2, editable=False, max_digits=15, verbose_name='差额')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('remark', models.TextField(blank=True, verbose_name='备注')),
                ('account_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='LedgerManageSystem.ledgerinfo', verbose_name='归属账本')),
            ],
        ),
    ]
