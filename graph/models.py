from __future__ import unicode_literals

from django.db import models

class Graph(models.Model):
    u = models.CharField(max_length=50)
    v = models.CharField(max_length=50)
    bus = models.CharField(max_length=50,null=False)
    cost = models.FloatField(null=False)
    distance = models.FloatField(null=False)
    time = models.FloatField(null=False)

    class Meta:
        unique_together = (("u", "v", "bus", "cost", "time", "distance"),)

    def __unicode__(self):
        return (unicode)(str(self.u) + ' ' + str(self.v) + ' ' + str(self.bus))