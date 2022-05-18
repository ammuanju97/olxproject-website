from .models import BroadcastNotifications
def notifications(request):
    allnotifications = BroadcastNotifications.objects.all()
    return {'notifications' : allnotifications }
    