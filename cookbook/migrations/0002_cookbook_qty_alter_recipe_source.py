# Generated by Django 4.1 on 2022-08-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookbook',
            name='qty',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='source',
            field=models.CharField(max_length=512),
        ),
    ]
