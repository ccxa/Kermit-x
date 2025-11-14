from django.db.models import IntegerChoices


class PlatformType(IntegerChoices):
    X = 1, 'X - (Twitter)'