from django.db import models
from django_summernote.fields import SummernoteTextField

from django.conf import settings

UserModel = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = SummernoteTextField()

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = SummernoteTextField()

    def __str__(self):
        return self.name

class News(models.Model):
    class LanguageTypes(models.TextChoices):
        ENGLISH = "EN", "en"
        NEPALI = "NP", "np"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True, related_name="news")
    tags = models.ManyToManyField(Tag, db_index=True, related_name="news")

    author = models.ForeignKey(UserModel, on_delete=models.PROTECT)

    title = models.CharField(max_length=1024)
    body = SummernoteTextField()
    language = models.CharField(max_length=8, choices=LanguageTypes.choices, default=LanguageTypes.ENGLISH)

    # Will be created automatically after the model has been saved.
    summary = models.TextField(null=True, blank=True)

    # AI will be used to automatically create them
    full_body_tts = models.FileField(upload_to="tts/full_body", null=True, blank=True)
    summary_tts = models.FileField(upload_to="tts/summary", null=True, blank=True)

    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title