from django.utils import timezone
from django import forms
from django.db import models
from django.forms import ModelForm
from django.urls import reverse

SCAN_STATUS = (
    ('waiting', 'Waiting'),
    ('running', 'Running'),
    ('finished', 'Finished')
)

class NmapProfile(models.Model):
    alias_text = models.CharField(max_length=64)
    args_text = models.CharField(max_length=2048)
    pub_date = models.DateTimeField('date created')

    def __str__(self):
        return self.alias_text

class NmapScan(models.Model):
    target_text = models.CharField(max_length=1024)
    cmd_text = models.CharField(max_length=2048)
    status_text = models.CharField(max_length=16, choices=SCAN_STATUS)
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date end', null=True, blank=True)
    uuid = models.CharField(max_length=32, null=True, blank=True)
    schedule_time = models.DateTimeField('schedule time', null=True, blank=True)
    repeat = models.CharField(max_length=10, choices=[('none', 'None'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='none')

    def __str__(self):
        return "%s" % (self.cmd_text)
    
class ScanForm(forms.ModelForm):
    schedule_date = forms.DateTimeField(required=False, input_formats=['%Y-%m-%dT%H:%M'])
    
    class Meta:
        model = NmapScan
        fields = ['target_text', 'schedule_date', 'repeat']

    def clean_schedule_date(self):
        schedule_date = self.cleaned_data.get('schedule_date')
        if schedule_date and schedule_date < timezone.now():
            self.cleaned_data['schedule_date'] = timezone.now()
        return schedule_date