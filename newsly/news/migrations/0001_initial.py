# Generated by Django 4.1.3 on 2022-12-05 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_summernote.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('description', django_summernote.fields.SummernoteTextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('description', django_summernote.fields.SummernoteTextField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('body', django_summernote.fields.SummernoteTextField()),
                ('language', models.CharField(choices=[('EN', 'en'), ('NP', 'np')], default='EN', max_length=8)),
                ('summary', models.TextField(blank=True, null=True)),
                ('full_body_tts', models.FileField(blank=True, null=True, upload_to='tts/full_body')),
                ('summary_tts', models.FileField(blank=True, null=True, upload_to='tts/summary')),
                ('metadata', models.JSONField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.category')),
                ('tags', models.ManyToManyField(db_index=True, related_name='news', to='news.tag')),
            ],
        ),
    ]