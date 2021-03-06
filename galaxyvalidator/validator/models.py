from django.db import models
from django.conf import settings

from fields import *

import datetime
import subprocess

class LapinError(Exception): pass

class Result(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    input = models.TextField()
    output = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    
    _input = None
    def get_input(self):
        if not self._input:
            self._input = self.input.split('\n')
        return self._input
    
    def get_line(self, lineno):
        input = self.get_input()
        return input[lineno-1]
    
    def split_output(self):
        for line in self.output.split('\n'):
            data = line.split(':')
            if data[0].lower() == 'warning':
                yield 'Warning', int(data[1].rsplit(' ', 1)[-1]), ':'.join(data[2:])
            else:
                yield 'Error', int(data[0].rsplit(' ', 1)[-1]), ':'.join(data[1:])
    
    def get_results(self):
        types = {}
        for line in self.split_output():
            if line[0] not in types:
                types[line[0]] = 0
            types[line[0]] += 1
        return types
    
    def process(self):
        args = [settings.LAPIN_BINARY_PATH, '-I', settings.LAPIN_INCLUDE_PATH, '-B', settings.LAPIN_INCLUDE_PATH, '-']
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        results = p.communicate(input=self.input)
        if results[1]:
            raise LapinError(results[1])

        results = results[0].split('\n')
        
        version = results[0]
        
        results = '\n'.join([r.strip() for r in results[6:]]).strip()

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