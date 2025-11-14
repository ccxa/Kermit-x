from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name=_("Created time"), auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=_("Updated time"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    class Meta:
        abstract = True





class TaskSchedule(BaseModel):
    # Scheduling
    cron_expression = models.CharField(verbose_name=_("Cron expression"), max_length=255)

    # Execution tracking
    last_executed_at = models.DateTimeField(verbose_name=_("Last executed at"), null=True, blank=True)
    execution_count = models.IntegerField(verbose_name=_("Execution count"), default=0)
    
    # Process tracking
    current_pid = models.CharField(verbose_name=_("Current PID"), max_length=255, null=True, blank=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.cron_expression} - {self.last_executed_at} - {self.execution_count} - {self.current_pid}"