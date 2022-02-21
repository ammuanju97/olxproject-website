from .forms import BuyerForm
from .models import BuyProduct
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from customer.models import PostProduct
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.forms.utils import pretty_name
from django.shortcuts import redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from notiapp.models import BroadcastNotifications
from sellproject.settings import EMAIL_HOST_USER
from twilio.rest import Client
import json
import os

# Create your views here.
class EmailNoti(TemplateView):
    template_name = 'buyer/emailnoti.html'
        

class BuyerList(TemplateView):
    template_name = 'buyer/buyerlist.html'
    def get(self, request, id):
        products = PostProduct.objects.get(id = id)
        buyers = BuyProduct.objects.filter(product_name = products)
        return render(request, self.template_name, {'buyers' : buyers})
    

class AcceptRequest(View):
    def get(self, request, id):
        approve = get_object_or_404(BuyProduct, id = id)
        product = BuyProduct.objects.get(id = id)
        return render(request, 'buyer/approved.html', {'products' : product })


def sendmail(request, id):
    product = BuyProduct.objects.get(id = id)
    product.buy_status = True
    product.save(update_fields = ['buy_status'])
    product_id = product.product_name.id
    product_status = PostProduct.objects.get(id = product_id)
    product_status.sale_status = True
    product_status.save(update_fields = ['sale_status'])
    subject = 'Accpeted your request for Buying a product'
    email = product.buyer_name.email
    account = settings.TWILIO_ACCOUNT_SID
    token = settings.TWILIO_AUTH_TOKEN
    client = Client(account, token)
    message = client.messages.create(
    body = f'{product.seller_name} ,is sucessfully approved your request for buying {product.product_name}',
    from_ = settings.TWILIO_FROM_,
    to = phone_number
    )
   
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
                "notification_%s" % product.buyer_name.username,
                {
                    'type': 'send_notification',
                    'message': f'{product.seller_name} ,is sucessfully approved your request for buying {product.product_name}',
                }
                )
    notifications = BroadcastNotifications.objects.create(message = f'{product.seller_name} sucessfully approved your request for buying {product.product_name}', sent=True, to_user = product.buyer_name)
    notifications.save()
    message = render_to_string('buyer/replymailnoti.html', {
                'buyer' : product.buyer_name,
                'product' : product.product_name,
                'price' : product.buyer_price,
                'seller': product.seller_name
            })
    send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently= False)
    messages.success(request, "sucessfuly sent a approved mail")
    return redirect('userhome')


class RejectRequest(View):
    def get(self, request, id):
        approve = get_object_or_404(BuyProduct, id = id)
        product = BuyProduct.objects.get(id = id)
        return render(request, 'customer/userhome.html')


def rejectmail(request, id):
    product = BuyProduct.objects.get(id = id)
    product.buy_status = False
    product.save(update_fields = ['buy_status'])
    subject = 'Cancelled!!! Your request for Buying a product is cancelled..'
    email = product.buyer_name.email
    message = render_to_string('buyer/rejectmail.html', {
                'buyer' : product.buyer_name,
                'product' : product.product_name,
                'price' : product.buyer_price,
                'seller': product.seller_name
            })
    send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently= False)
    messages.success(request, "Product reject mail send sucessfuly ")
    return redirect('userhome')


class MyOrders(TemplateView):
    template_name = 'buyer/myorders.html'
    def get(self, request):

        myorders = BuyProduct.objects.filter(buyer_name = request.user)
        return render(request, self.template_name, {'myorders' : myorders} )
