# Generated by Django 5.0.4 on 2024-04-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reports', models.CharField(max_length=200, verbose_name='Сделка')),
                ('counterparty', models.CharField(blank=True, max_length=200, null=True, verbose_name='Контрагент')),
                ('undisclosed_write', models.CharField(blank=True, max_length=200, null=True, verbose_name='Неразнесенное списание')),
                ('value', models.CharField(max_length=200, verbose_name='Сумма руб.')),
                ('description', models.TextField(verbose_name='Назначения платежа')),
                ('image_cheque', models.ImageField(upload_to='', verbose_name='Чек (фото)')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'отчёт',
                'verbose_name_plural': 'Отчёты',
            },
        ),
    ]
