from django.db import models
from django.conf import settings

from validator.fields import *

from cStringIO import StringIO

import datetime
import subprocess

class Result(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    input = models.TextField()
    output = models.TextField(blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    
    def process(self):
        args = [settings.LAPIN_BINARY_PATH, '-I', settings.LAPIN_INCLUDE_PATH, '-']
        print args
        p = subprocess.Popen(args, stdin=StringIO(subprocess.PIPE), stdout=subprocess.PIPE, shell=True)
        results = p.communicate()[0]
        self.output = results
        print results
        