from django.db import models
from django_summernote.fields import SummernoteTextField
from django.utils.html import strip_tags
from django.core.files.base import File, BytesIO
from django.conf import settings
from django.core.mail import send_mail

from newsly.accounts.models import CustomUser
from newsly.news.ai import get_tts, get_tts_ibm, get_summary, translate_to_nepali

UserModel = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = SummernoteTextField()

    def description_text(self):
        return strip_tags(self.description.replace("<p>", "").replace("</p>", "\n"))

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    description = SummernoteTextField()

    def description_text(self):
        return strip_tags(self.description.replace("<p>", "").replace("</p>", "\n"))

    def __str__(self):
        return self.name


class News(models.Model):
    class LanguageTypes(models.TextChoices):
        ENGLISH = "EN", "en"
        NEPALI = "NP", "np"

    created = models.DateTimeField(auto_created=True, db_index=True)

    cover_image = models.ImageField(upload_to="images/news/cover_images", null=True)

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

    is_draft = models.BooleanField(default=True, editable=False)

    def comma_separate_tags(self):
        cst = ""
        for tag in self.tags.all():
            cst += tag.name + ","

        return cst

    def author_name(self):
        return self.author.first_name + " " + self.author.last_name

    def category_name(self):
        return self.category.name

    def all_tags(self):
        tag_list = []
        for tag in self.tags.all():
            tag_list.append(tag.name)
        return tag_list

    def body_text(self):
        text = strip_tags(self.body.replace("<p>", "").replace("</p>", "\n"))
        return text

    def __str__(self):
        return self.title

    def get_tts_summary(self):
        text = self.title + "\n\n" + self.summary

        if self.language == self.LanguageTypes.ENGLISH:
            tts = get_tts_ibm(text)
            self.summary_tts.save(self.title + ".mp3", File(BytesIO(tts)))
        else:
            tts = get_tts(text)
            self.summary_tts.save(self.title + ".mp3", File(tts))

    def get_tts_body(self):
        text = self.title + "\n\n" + self.body_text()

        tts = get_tts(text)
        self.full_body_tts.save(self.title + ".mp3", File(tts))

    def generate_summary(self):
        summary = get_summary(self.body_text())
        self.metadata = {} if not self.metadata else self.metadata

        try:
            summary_log = self.metadata["summary"]
        except KeyError as e:
            summary_log = []

        summary_log.append(summary)

        self.metadata["summary"] = summary_log
        self.save()

        if self.language == self.LanguageTypes.ENGLISH:
            self.summary = summary["choices"][0]["text"]
        else:
            # OPEN AI translates nepali to english while summary generation, hence converting it to nepali using
            # Google Translate API
            self.summary = translate_to_nepali(translate_to_nepali(summary["choices"][0]["text"]))
        self.save()

    def send_success_email_to_author(self):
        body_content = f"{self.title}\n\nFull TTS: {self.full_body_tts.url}\nSummary TTS: {self.summary_tts}\n\nSummary: {self.summary}"
        try:
            send_mail(
                f'News: {self.title} has been processed!',
                body_content,
                settings.EMAIL_HOST_USER,
                [self.author.email],
                fail_silently=False,
            )
        except Exception as e:
            print("ERROR SENDING EMAIL", e)

    def process_news(self):
        self.generate_summary()
        self.get_tts_summary()
        self.get_tts_body()
        self.send_success_email_to_author()

    def __name__(self):
        return self.title


class NewsInteraction(models.Model):
    user = models.ForeignKey(CustomUser, related_name="interactions", on_delete=models.CASCADE)
    news = models.ForeignKey(News, related_name="interactions", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'news')

    def __str__(self):
        return f"{self.user.id} || {self.news.id}"
