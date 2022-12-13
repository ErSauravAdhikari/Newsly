from django.shortcuts import render
from .models import News


# Create your views here.
def email_example(r):
    return render(r, "email.html", {
        "newses": News.objects.all(),
    })
