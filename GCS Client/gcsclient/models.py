from django.db import models

class Settings(models.Model):

    MITIGATION_ACTIONS = [
        ('RTH', 'Return to Home'),
        ('HOVER', 'Hover'),
        ('LAND', 'Land'),
        ('TELEM', 'Disable Telemetry'),
        ('ALERT', 'Alert Only'),
        ]

    CONNECTION_METHODS = [
        ('GCS', 'Local GCS'),
        ('DIRECT', 'Direction Connection'),
        ]

    dos_enabled = models.BooleanField(default=False)
    gps_enabled = models.BooleanField(default=False)
    default_action = models.CharField(
        max_length=6,
        choices=MITIGATION_ACTIONS,
        default='RTH')
    default_initiate_time = models.IntegerField(default=0)
    default_return_time = models.IntegerField(default=0)
    connection_method = models.CharField(
        max_length=6,
        choices=CONNECTION_METHODS,
        default='GCS')

class Connection(models.Model):
    established = models.BooleanField(default=False)
