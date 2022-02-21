from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
# Create your models here.
class BroadcastNotifications(models.Model):
    to_user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    message = models.TextField()
    broadcast_on = models.DateTimeField(auto_now_add=True, blank=True)
    sent = models.BooleanField(default = False)

    def __str__(self):
        return self.message
    
    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender = BroadcastNotifications)
def notification_handler(sender, instance, created, **kwargs):
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab = schedule, name = "broadcast-notification-" + str(instance.id), task = 'notiapp.tasks.broadcast_notification', args = json.dumps((instance.id)))
