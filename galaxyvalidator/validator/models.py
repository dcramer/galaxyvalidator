from django.db import models
from django.conf import settings

from fields import *

import datetime
import subprocess

class Result(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    input = models.TextField()
    output = models.TextField(blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    
    def process(self):
        args = [settings.LAPIN_BINARY_PATH, '-I', settings.LAPIN_INCLUDE_PATH, '-']
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        results = p.communicate(input=self.input)[0]
        return results.split('In file "standard input"', 1)[1].strip()
        