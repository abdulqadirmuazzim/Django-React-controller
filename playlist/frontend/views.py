from django.shortcuts import render


def index(req, *args, **kwargs):
    return render(req, "frontend/index.html")
