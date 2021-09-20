from django.utils import timezone
from django.db import models
from rest_framework import serializers


def not_future_year_validator(year):
    if year > timezone.now().year:
        raise models.ValidationError("Incorrect year")


def validate_score(value):
    if value < 1 or value > 10:
        raise serializers.ValidationError('Некорректная оценка')
    return value
