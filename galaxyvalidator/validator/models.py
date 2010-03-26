from django.db import models
from django.conf import settings

from fields import *

from cStringIO import StringIO

import datetime
import subprocess

class LapinError(Exception): pass

class Result(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    input = models.TextField()
    output = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    
    def split_output(self):
        for line in result.output.split('\n'):
            data = line.split(':', 2)
            yield data[0], data[1].rsplit(' ', 1)[-1], data[2]
    
    def process(self):
        output = StringIO()
        
        args = [settings.LAPIN_BINARY_PATH, '-I', settings.LAPIN_INCLUDE_PATH, '-']
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        results = p.communicate(input=self.input)
        if results[1]:
            raise LapinError(results[1])

        results = results[0].split('\n')
        
        version = results[0]
        
        results = '\n'.join([r.strip() for r in results[6:-4]]).strip()

        if not results:
            self.success = True
        else:
            self.output = results
            self.success = False
    
    def __unicode__(self):
        return self.input[:200]
    
    @models.permalink
    def get_absolute_url(self):
        return ('validator.results', (), {'result_id': self.id})