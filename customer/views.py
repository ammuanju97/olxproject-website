from asgiref.sync import async_to_sync
from buyer.forms import BuyerForm
from buyer.models import BuyProduct
from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.db import reset_queries
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic 
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import AddressForm, ProfileForm, AddressDetForm, CreatePostForm
from home.models import Useradd
from .models import PostProduct, UserAddress
from notiapp.models import BroadcastNotifications
from sellproject.settings import EMAIL_HOST_USER
import json
# Create your views here.
class Userhome(View):
    def get(self,request):
        product = PostProduct.objects.all()
        return render(request, 'customer/userhome.html', {'products' : product,  'room_name' : request.user.username })
   

def editprofile(request):
    msg = None
    userdetails = Useradd.objects.get(user = request.user)
    useraddress = UserAddress.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance = request.user)
        form1 = AddressForm(request.POST, instance = userdetails)
        form2 = AddressDetForm(request.POST, instance = useraddress)
        if form.is_valid() and form1.is_valid() and form2.is_valid():
            form.save()
            form1.save()
            form2.save()
            msg = 'Profile Updated Successfully'
    form = ProfileForm(instance = request.user)
    form1 = AddressForm(instance = userdetails)
    form2 = AddressDetForm(instance = useraddress)
    return render(request, 'profile/editprofile.html', {'form' : form, 'msg' : msg, 'form1' : form1, 'form2' : form2})


def adddetail(request):
    msg = None
    if request.method == 'POST' :
        form = AddressDetForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit = False)
            saveForm.user = request.user
            saveForm.save()
            msg = 'Profile details added successfully'
    form = AddressDetForm()
    return render(request, 'profile/adddetails.html', {'form' : form, 'msg' : msg})


class ProfileDisplay(LoginRequiredMixin, generic.ListView):
    template_name = 'profile/viewprofile.html'
    
    def get(self, request):
        userdetails  = Useradd.objects.get(user = request.user)
        useraddress = UserAddress.objects.get(user = request.user)
        return render(request, self.template_name, {'form' : userdetails, 'form1' : useraddress,})


class CreatePost(CreateView):
    def get(self, request):
        form = CreatePostForm()
        return render(request, 'post/createpost.html', {'form' : form})
    def post(self, request):
        msg = None
        fm = CreatePostForm(request.POST, request.FILES)
        if fm.is_valid():
            form = fm.save(commit = False)
            form.user = request.user
            form.save()
            msg = 'Product details added successfully'
        form = CreatePostForm()
        return render(request, 'post/createpost.html', {'form' : form, 'msg' : msg})
        

class ProductDisplay(LoginRequiredMixin, generic.ListView):
    template_name = 'post/viewpost.html'
    def get(self ,request):
        product = PostProduct.objects.filter(user = request.user)
        return render(request, self.template_name, {'product' : product})


class EditProduct(UpdateView):
    model = PostProduct
    fields = [
        'product_name', 'description', 'category', 'price', 'time_to_publish', 'image'
    ]
    template_name = 'post/editpost.html'
    success_url = reverse_lazy('userhome')


class DeleteProduct(DeleteView):
    model = PostProduct
    template_name = 'post/deletepost.html'
    success_url = reverse_lazy('viewpost')


class ViewMore(TemplateView):
    template_name = 'post/viewmore.html'
    def get(self, request, id):
        fm = BuyerForm()
        product = PostProduct.objects.get(id = id)
        return render(request, self.template_name, {'product' : product, 'fm' : fm})
    def post(self, request, id):
        fm = BuyerForm()
        if request.method == "POST":
            fm = BuyerForm(request.POST)
            product = PostProduct.objects.get(id = id)
            seller = product.user
            if fm.is_valid():
                form = fm.save(commit = False)
                form.seller_name = seller
                form.buyer_name = request.user
                form.buy_status = False
                form.product_name = product
                form.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                "notification_%s" % product.user.username,
                {
                    'type': 'send_notification',
                    'message': f' {request.user} , sent a buy request for your {product.product_name} !!',
                }
                )
                notifications = BroadcastNotifications.objects.create(message = f'send purchase request from {request.user} for the product {product.product_name}', sent=True, to_user = seller)
                notifications.save()
                email = seller.email
                subject = 'Request for Buying a product'
                message = render_to_string('buyer/emailnoti.html', {
                    'buyer' : request.user,
                    'product' : product.product_name,
                    'price' : fm.cleaned_data['buyer_price'],
                    'seller' : seller.username
                })
                send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently= False )
                messages.success(request, "sucessfuly sent a request mail")
                return redirect('userhome')
            else:
                messages.info(request, 'already send')
                return redirect('userhome')
                