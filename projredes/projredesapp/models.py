from django.db import models

# Create your models here.

class Traceroute(models.Model):
    ip_address = models.CharField(max_length=50)
    ttl = models.IntegerField()
    icmp_type = models.IntegerField(null=True)
    icmp_code = models.IntegerField(null=True)
    remote_machine = models.CharField(max_length=50, null=True)
    protocol = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.ip_address} (TTL: {self.tt}l)"