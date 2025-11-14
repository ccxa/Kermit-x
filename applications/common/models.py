from django.db import models
from utils.models import BaseModel
from django.utils.translation import gettext_lazy as _
from applications.common.choices import PlatformType
# Create your models here.



class PlatformAccount(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"), choices=PlatformType.choices
    )
    credentials = models.JSONField(verbose_name=_("Credentials"))

    class Meta:
        verbose_name = _("Platform Account")
        verbose_name_plural = _("Platform Accounts")

    def __str__(self):
        return f"{self.name} - {self.type}"


