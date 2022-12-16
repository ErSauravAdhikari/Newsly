import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string

from newsly.accounts.models import CustomUser
from newsly.news.models import News, DiscordWebhookStore

from datetime import datetime, timedelta
from django.utils.timezone import make_aware



def send_daily_newsletter():
    users = CustomUser.objects.all()
    for user in users:

        yesterday = datetime.now() - timedelta(1)

        aware_yesterday = make_aware(yesterday)

        news = News.objects.filter(is_draft=False).filter(~Q(full_body_tts="")).filter(~Q(summary_tts="")).filter(
            ~Q(summary="")).order_by('-created').filter(relevant_news__user=user).filter(
            created__gte=aware_yesterday).distinct()

        if news.count() == 0:
            continue

        html_text = render_to_string(
            "email.html",
            {
                "newses": news
            }
        )

        text = ""
        for n in news:
            text += n.title + "\n\n"
            text += n.summary + "\n\n\n"

        try:
            send_mail(
                subject=f"Newsly's Daily Newsletter For Today!",
                message=text,
                html_message=html_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print("Newsletter sent to: ", user.email)
        except Exception as e:
            print("ERROR SENDING NEWSLETTER EMAIL", e)
