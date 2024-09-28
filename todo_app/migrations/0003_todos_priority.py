# Generated by Django 3.2.16 on 2024-09-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_todos_user_alter_todos_date_alter_todos_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='todos',
            name='priority',
            field=models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], default='M', max_length=1),
        ),
    ]
