# Generated by Django 3.2.25 on 2024-03-05 13:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_reference_no', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('IN_COLLECTION', 'In Collection'), ('INACTIVE', 'Inactive'), ('PAID_IN_FULL', 'Paid In Full')], max_length=20)),
                ('consumer_name', models.CharField(max_length=255)),
                ('consumer_address', models.TextField()),
                ('ssn', models.CharField(help_text='Enter ssn in the format XXX-XX-XXXX', max_length=11, validators=[django.core.validators.RegexValidator(message="SSN must be entered in the format: 'XXX-XX-XXXX'. Up to 9 digits allowed.", regex='^\\d{3}-\\d{2}-\\d{4}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client')),
            ],
        ),
    ]