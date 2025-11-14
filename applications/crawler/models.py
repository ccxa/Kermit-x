from django.db import models
from applications.common.models import PlatformAccount
from utils.models import TaskSchedule, BaseModel
from django.utils.translation import gettext_lazy as _
from utils.app_scheduler import bs
from django.utils import timezone


class Crawler(BaseModel):
    name = models.CharField(unique=True, verbose_name=_("Name"), max_length=255)
    account = models.ForeignKey(PlatformAccount, verbose_name=_("Account"), on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name = _("Crawler")
        verbose_name_plural = _("Crawlers")

    def __str__(self):
        return self.name


    def crawl(self):
        print(f"🪱")


class CrawlerTask(TaskSchedule):
    crawler = models.ForeignKey(Crawler, verbose_name=_("Crawler"), on_delete=models.CASCADE)
    search_query = models.CharField(verbose_name=_("Search query"), max_length=255)
    
    class Meta:
        verbose_name = _("Crawler Task")
        verbose_name_plural = _("Crawler Tasks")

    def __str__(self):
        return f"{self.crawler.name} - {self.search_query} - {self.last_executed_at}"


    def run_task(self):
        print('running task')
        self.last_executed_at = timezone.now()
        self.execution_count += 1
        self.save()
        self.crawler.crawl()

    def run(self):
        print(f"Running crawler task {self.id} for {self.search_query}")
        job = bs.get_job(job_id=self.current_pid)
        if job:
            job.resume()
        else:
            job = bs.add_job(self.run_task, 'interval', seconds=int(self.cron_expression))
            self.current_pid = job.id
            self.save()

    def pause(self):
        job = bs.get_job(job_id=self.current_pid)
        if job:
            job.pause()

    @property
    def status(self):
        job = bs.get_job(job_id=self.current_pid)
        return getattr(job, 'next_run_time', None) is not None

    