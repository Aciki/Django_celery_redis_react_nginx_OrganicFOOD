# Generated by Django 4.0.3 on 2022-03-19 15:20

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250, verbose_name='Food Title')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='title', unique=True)),
                ('ref_code', models.CharField(blank=True, max_length=255, unique=True, verbose_name='Food Reference Code')),
                ('description', models.TextField(default='Default description...update me please....', verbose_name='Description')),
                ('country', django_countries.fields.CountryField(default='KE', max_length=2, verbose_name='Country')),
                ('city', models.CharField(default='Skopje', max_length=180, verbose_name='City')),
                ('postal_code', models.CharField(default='140', max_length=100, verbose_name='Postal Code')),
                ('street_address', models.CharField(max_length=150, verbose_name='Street Address')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Price')),
                ('tax', models.DecimalField(decimal_places=2, default=0.5, help_text='5% Food tax charged', max_digits=6, verbose_name='Food Tax')),
                ('cover_photo', models.ImageField(blank=True, default='/house_sample.jpg', null=True, upload_to='', verbose_name='Main Photo')),
                ('photo1', models.ImageField(blank=True, default='/interior_sample.jpg', null=True, upload_to='')),
                ('photo2', models.ImageField(blank=True, default='/interior_sample.jpg', null=True, upload_to='')),
                ('photo3', models.ImageField(blank=True, default='/interior_sample.jpg', null=True, upload_to='')),
                ('photo4', models.ImageField(blank=True, default='/interior_sample.jpg', null=True, upload_to='')),
                ('published_status', models.BooleanField(default=False, verbose_name='Published Status')),
                ('views', models.IntegerField(default=0, verbose_name='Total Views')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='agent_buyer', to=settings.AUTH_USER_MODEL, verbose_name='Agent,Seller or Buyer')),
            ],
            options={
                'verbose_name': 'OrganiC FOOD',
                'verbose_name_plural': 'Organic',
            },
        ),
        migrations.CreateModel(
            name='FoodViews',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(max_length=250, verbose_name='IP Address')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_views', to='food.food')),
            ],
            options={
                'verbose_name': 'Total Views on Item',
                'verbose_name_plural': 'Total item Views',
            },
        ),
    ]
