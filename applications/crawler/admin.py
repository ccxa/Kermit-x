from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.template.loader import render_to_string
from applications.crawler.models import Crawler, CrawlerTask


class CrawlerTaskAdminInline(admin.TabularInline):
    model = CrawlerTask
    list_display = ('crawler', 'search_query', 'last_executed_at', 'execution_count', 'current_pid')
    readonly_fields = ('last_executed_at', 'execution_count', 'current_pid')
    extra = 1
    

@admin.register(Crawler)
class CrawlerAdmin(admin.ModelAdmin):
    list_display = ('name', 'account')
    inlines = [CrawlerTaskAdminInline]


@admin.register(CrawlerTask)
class CrawlerTaskAdmin(admin.ModelAdmin):
    list_display = ('crawler', 'search_query', 'last_executed_at', 'execution_count', 'current_pid', 'status_toggle')
    readonly_fields = ('last_executed_at', 'execution_count', 'current_pid')
    
    def status_toggle(self, obj):
        """Render a toggle switch for run/pause"""
        is_running = obj.status  # True if running, False if paused
        toggle_url = reverse('admin:crawler_task_toggle', args=[obj.pk])
        
        # Render from template - completely separated presentation
        html = render_to_string('admin/crawler/crawlertask/widgets/toggle_switch.html', {
            'is_running': is_running,
            'toggle_url': toggle_url,
        })
        return mark_safe(html)
    
    status_toggle.short_description = 'Status'
    
    def get_urls(self):
        """Add custom URL for toggle action"""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:task_id>/toggle/',
                self.admin_site.admin_view(self.toggle_task_view),
                name='crawler_task_toggle',
            ),
        ]
        return custom_urls + urls
    
    def toggle_task_view(self, request, task_id):
        """Handle the toggle action"""
        task = CrawlerTask.objects.get(pk=task_id)
        
        # Check current status and toggle
        if task.status:  # If running, pause it
            task.pause()
        else:  # If paused, run it
            task.run()
        
        # Redirect back to the changelist
        return redirect('admin:crawler_crawlertask_changelist')
