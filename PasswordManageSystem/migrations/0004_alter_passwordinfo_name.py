# Generated by Django 5.0.1 on 2024-04-12 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PasswordManageSystem', '0003_alter_passwordinfo_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordinfo',
            name='name',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
    ]