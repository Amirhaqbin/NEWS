# Generated by Django 4.0.1 on 2022-04-22 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khabari', '0002_alter_newspage_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspage',
            name='status',
            field=models.CharField(choices=[('Draft', 'draft'), ('Published', 'published')], default='draft', max_length=10),
        ),
    ]