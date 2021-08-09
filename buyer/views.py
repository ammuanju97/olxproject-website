from customer.models import PostProduct
from django.contrib import messages
from django.core.mail import send_mail
from django.forms.utils import pretty_name
from django.shortcuts import redirect, render,get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .forms import BuyerForm
from .models import BuyProduct
from sellproject.settings import EMAIL_HOST_USER
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
        approve.buy_status = True
        approve.save(update_fields = ['buy_status'])
        product = BuyProduct.objects.get(id = id)
        return render(request, 'buyer/approved.html', {'products' : product })
