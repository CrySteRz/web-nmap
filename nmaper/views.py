import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import os

from .models import NmapProfile, NmapScan, ScanForm
from .utils import execute_scan

OUTPUT_PATH = os.path.normpath("%s/nmaper/static/results" % os.getcwd()).replace("\\", "/")

@login_required(login_url='/login/')
def index(request):
    context = {'profiles': NmapProfile.objects.all()}
    template = loader.get_template('index.html')

    if request.method == 'POST':
        f = ScanForm(request.POST)
        if f.is_valid():
            new_scan = f.save(commit=False)
            new_scan.status_text = "waiting"
            new_scan.start_date = timezone.now()
            new_scan.end_date = timezone.now()
            
            nmap_cmd = NmapProfile.objects.get(id=request.POST['profile'])
            new_scan.cmd_text = "%s %s" % (nmap_cmd.args_text, new_scan.target_text)

            if 'dns_check' in request.POST:
                new_scan.cmd_text = "%s -n" % new_scan.cmd_text
            if 'ping_check' in request.POST:
                new_scan.cmd_text = "%s -Pn" % new_scan.cmd_text

            # Use the cleaned schedule_date
            schedule_date = f.cleaned_data.get('schedule_date')
            new_scan.schedule_time = schedule_date if schedule_date else timezone.now()

            new_scan.save()
            
            schedule_time = new_scan.schedule_time if new_scan.schedule_time else timezone.now()
            if new_scan.repeat == 'daily':
                execute_scan(new_scan.id, schedule=schedule_time, repeat=24*60*60)
            elif new_scan.repeat == 'weekly':
                execute_scan(new_scan.id, schedule=schedule_time, repeat=7*24*60*60)
            elif new_scan.repeat == 'monthly':
                execute_scan(new_scan.id, schedule=schedule_time, repeat=30*24*60*60)
            else:
                execute_scan(new_scan.id, schedule=schedule_time)
            
            context['popup_message'] = 'Your scan has been scheduled!'
        else:
            context['popup_message'] = f.errors

    return HttpResponse(template.render(context, request))
