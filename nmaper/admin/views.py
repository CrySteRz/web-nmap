from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib import admin, messages
from django.utils.html import format_html
from nmaper import views, models

class NmapScanAdmin(admin.ModelAdmin):
    list_display = ('target_text', 'cmd_text', 'status_text', 'start_date', 'end_date', 'download_links')

    def download_links(self, obj):
        if obj.status_text == 'finished':
            return format_html('''
                <a class="btn btn-secondary" href="/static/results/{}.html" download>HTML</a>
                <a class="btn btn-secondary" href="/static/results/{}.nmap" download>Nmap</a>
                <a class="btn btn-secondary" href="/static/results/{}.gnmap" download>Gnmap</a>
                <a class="btn btn-secondary" href="/static/results/{}.xml" download>XML</a>
            ''', obj.uuid, obj.uuid, obj.uuid, obj.uuid)
        else:
            return format_html('''
                <button class="btn btn-secondary" disabled>HTML</button>
                <button class="btn btn-secondary" disabled>Nmap</button>
                <button class="btn btn-secondary" disabled>Gnmap</button>
                <button class="btn btn-secondary" disabled>XML</button>
            ''')

    download_links.short_description = 'Download Links'
    download_links.allow_tags = True

admin.site.register(models.NmapScan, NmapScanAdmin)
admin.site.register(models.NmapProfile)
admin.site.unregister(Group)
admin.site.unregister(User)

def clear_logs(request):
    """Clear admin activity logs if user has permissions"""

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.has_perm('admin.delete_logentry'):
        LogEntry.objects.all().filter(user__pk=request.user.id).delete()
        messages.info(request, 'Successfully cleared admin activity logs.', fail_silently=True)
    else:
        messages.warning(request, 'Unable to clear the admin activity logs.', fail_silently=True)

    return redirect('admin:index')
