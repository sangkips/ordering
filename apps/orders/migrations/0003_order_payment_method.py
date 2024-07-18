# Generated by Django 5.0.7 on 2024-07-18 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_orderdetails_orderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'card'), ('MPESA', 'mpesa')], default='CASH', max_length=25),
        ),
    ]
