import telebot

from django.db import models
from django_summernote.fields import SummernoteTextField
from django.utils.html import strip_tags
from django.core.files.base import File, BytesIO
from django.conf import settings
from django.core.mail import send_mail

from newsly.accounts.models import CustomUser
from newsly.news.ai import get_tts, get_tts_ibm, get_summary, translate_to_nepali

import requests

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

    cover_image = models.ImageField(upload_to="images/self/cover_images", null=True)

    category = models.ManyToManyField(Category, db_index=True, related_name="self")
    tags = models.ManyToManyField(Tag, db_index=True, related_name="self")

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

    def created_str(self):
        return self.created.strftime('%m/%d/%Y %H:%M')

    def comma_separate_tags(self):
        cst = ""
        for tag in self.tags.all():
            cst += tag.name + ","

        return cst

    def author_name(self):
        return self.author.first_name + " " + self.author.last_name

    def category_name(self):
        categories = ""
        for category in self.category.all():
            categories += category.name + ","
        return categories

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
        self.generate_relevancy()
        self.send_success_email_to_author()

    def generate_relevancy(self):
        """
        Run AI to generate relevancy
        Also sends webhook if the news is relevant to the user
        :return: None
        """
        for user in CustomUser.objects.all():
            is_rel = self.is_this_relevant_news_for_user(user)
            print(user, is_rel)
            if is_rel:
                RelevantNews.objects.get_or_create(user=user, news=self)
            else:
                try:
                    RelevantNews.objects.get(user=user, news=self).delete()
                except RelevantNews.DoesNotExist:
                    pass

    def is_this_relevant_news_for_user(self, user: CustomUser):
        interactions = NewsInteraction.objects.filter(user=user)

        all_fav_tags = {}
        all_fav_category = {}

        total_read = interactions.count()

        for interaction in interactions:
            for tag in interaction.news.tags.all():
                try:
                    all_fav_tags[tag] = all_fav_tags[tag] + 1
                except KeyError:
                    all_fav_tags[tag] = 1

            for category in interaction.news.category.all():
                try:
                    all_fav_category[category] = all_fav_category[category] + 1
                except KeyError:
                    all_fav_category[category] = 1

        news_tags = self.tags.all()
        news_categories = self.category.all()

        interaction_points = 0

        for tag in news_tags:
            try:
                interaction_points += all_fav_tags[tag]
            except KeyError:
                pass

        for category in news_categories:
            try:
                interaction_points += all_fav_category[category]
            except KeyError:
                pass

        if total_read < 5:
            return True
        elif interaction_points == 0:
            return False
        else:
            pts = interaction_points / total_read
            if pts > 0.2:
                return True
            else:
                return False

    def __name__(self):
        return self.title


def send_news_in_discord(news):
    all_relevance = news.relevant_news.all()
    for news_relevance in all_relevance:
        try:
            news_relevance.user.webhook.send_webhook_for_news(news)
        except DiscordWebhookStore.DoesNotExist:
            pass


def send_news_in_telegram(news):
    all_relevance = news.relevant_news.all()
    for news_relevance in all_relevance:
        try:
            news_relevance.user.webhook.send_telegram_for_news(news)
        except DiscordWebhookStore.DoesNotExist:
            pass


class NewsInteraction(models.Model):
    user = models.ForeignKey(CustomUser, related_name="interactions", on_delete=models.CASCADE)
    news = models.ForeignKey(News, related_name="interactions", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} || {self.news.id}"


class RelevantNews(models.Model):
    user = models.ForeignKey(CustomUser, related_name="relevant_news", on_delete=models.CASCADE)
    news = models.ForeignKey(News, related_name="relevant_news", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} || {self.news.id}"


class DiscordWebhookStore(models.Model):
    """
    Stores information about the social media account we need to send news to. Currently supported
    - Telegram
    - Discord
    """
    user = models.OneToOneField(CustomUser, related_name="webhook", on_delete=models.CASCADE)
    webhook = models.URLField(blank=True, null=True)
    telegram_id = models.CharField(blank=True, null=True, max_length=256)

    def __str__(self):
        return f"{self.user}"

    def send_telegram_for_news(self, news: News):
        if self.telegram_id:
            news_image = news.cover_image.url if news.cover_image.url else "https://media.discordapp.net/attachments/1047848577386426412/1053345656288329778/Newsly_500x500.png"
            news_image = "https://media.discordapp.net/attachments/1047848577386426412/1053345656288329778/Newsly_500x500.png"
            news_text = news.title + "\n\n" + news.summary
            settings.TG_BOT.send_photo(
                chat_id=self.telegram_id,
                photo=news_image,
                caption=news_text
            )

    def send_webhook_for_news(self, news: News):
        print(news.cover_image.url)
        payload = {
            "username": "Newsly",
            "avatar_url": "https://i.imgur.com/4M34hi2.png",
            "content": "New News from Newsly.",
            "embeds": [
                {
                    "author": {
                        "name": f"{news.author.first_name} {news.author.last_name}"
                    },
                    "title": news.title,
                    "description": news.summary,
                    "thumbnail": {
                        "url": str(news.cover_image.url),
                    }
                }
            ]
        }

        result = requests.request("POST", self.webhook, json=payload, headers={
            "Content-Type": "application/json"
        })

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            print(result.text)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
        return
