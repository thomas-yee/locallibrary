# Generated by Django 3.0.3 on 2020-04-30 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200428_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_edit', 'Can edit the book'),)},
        ),
    ]
