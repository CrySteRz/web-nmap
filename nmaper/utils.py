import subprocess
import os
import uuid
import datetime
import lxml.etree as ET
from django.utils import timezone
import distutils.spawn
from background_task import background
import time
from django.db import OperationalError
from NmapOptions import NmapOptions

OUTPUT_PATH = os.path.normpath(
    "%s/nmaper/static/results" % os.getcwd()
).replace("\\", "/")


def find_nmap():
    nmap_path = distutils.spawn.find_executable(
        "nmap", "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/opt/nmap/bin:/opt/homebrew/bin"
    )
    return nmap_path


def update_scan_status(scan, status_text, end_date=None):
    retries = 5
    while retries > 0:
        try:
            scan.status_text = status_text
            if end_date:
                scan.end_date = end_date
            scan.save()
            break
        except OperationalError:
            retries -= 1
            time.sleep(1)
            if retries == 0:
                raise


def generate_html_report(filename):
    dom = ET.parse("%s.xml" % filename)
    xsl_filename = dom.getroot().getprevious().getprevious().parseXSL()
    transform = ET.XSLT(xsl_filename)
    html = transform(dom)
    with open('%s.html' % filename, 'wb') as html_file:
        html_file.write(html)


@background(schedule=0)
def execute_scan(scan_id):
    from .models import NmapScan
    scan = None
    retries = 5
    while retries > 0:
        try:
            scan = NmapScan.objects.get(id=scan_id)
            break
        except OperationalError:
            retries -= 1
            time.sleep(1)
            if retries == 0:
                raise

    path = find_nmap()
    if not path:
        raise Exception("Nmap not found")

    scan.status_text = "running"
    scan.uuid = uuid.uuid4().hex
    scan.save()

    filename = "%s/%s" % (OUTPUT_PATH, scan.uuid)
    nmap_cmd = f"{path} {scan.cmd_text} -oA {filename}"
    ops = NmapOptions()
    ops.parse_string(scan.cmd_text)
    nmap_cmd_list = [path] + ops.render() + ["-oA", filename]
    
    proc = subprocess.Popen(nmap_cmd_list, shell=False)
    proc.wait()

    update_scan_status(scan, "finished", timezone.now())
    generate_html_report(filename)
