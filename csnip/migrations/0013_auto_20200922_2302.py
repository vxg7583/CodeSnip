# Generated by Django 3.1 on 2020-09-22 23:02

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csnip', '0012_auto_20200922_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='body',
            field=ckeditor.fields.RichTextField(default='please enter code here for accurate display'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snippet',
            name='explanation',
            field=ckeditor.fields.RichTextField(default='Your snippet must have an explanation to avoid deletion over time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snippet',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
