from django.shortcuts import render
from django.http import JsonResponse
from django_q.tasks import async_task

from .models import News


# Create your views here.
def email_example(r):
    return render(r, "email.html", {
        "newses": News.objects.all(),
    })


def trigger_relevancy(r):
    for news in News.objects.all():
        async_task(news.generate_relevancy)

    return JsonResponse({"status": "queued"})

