from seller.forms import AddressForm
from seller.models import PostProduct
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import SignUpForm, LoginForm
from .models import userreg
import uuid

# Create your views here.
class HomeView(View):
    def get(self,request):
            product = PostProduct.objects.all()
            item_name = request.GET.get('item_name')
            if item_name != '' and item_name is not None:                             
                product = product.filter(product_name__icontains = item_name)
            return render(request, 'index.html', {'products' : product})


def aboutus(request):
    return render(request, 'home/about.html')


def send_mail_after_registration(email, token):
    subject = "Verify Email"
    message = f'Hi Click on the link to verfiy your account http://127.0.0.1:8000/account-verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject = subject, message = message, from_email = from_email, recipient_list = recipient_list)


class SignUp(View):
    def get(self, request):
        fm = SignUpForm()
        addform = AddressForm()
        return render(request, 'home/regup.html', {'form' : fm, 'addform' : addform})
    def post(self, request):
        fm = SignUpForm(request.POST)
        addform = AddressForm(request.POST)
        if fm.is_valid():
            new_user = fm.save()
            addf = addform.save(commit = False)
            addf.user = new_user
            addf.save()
            uid = uuid.uuid4()
            user_obj = userreg(user = new_user, token = uid)
            user_obj.save()
            send_mail_after_registration(new_user.email, uid)
            messages.success(request, "Your Account created Successful, to verify your account check your mail")
            return redirect('signup')
        else:
            messages.info(request, 'username already taken')
            return redirect('signup')


def account_verify(request, token):
    pf = userreg.objects.filter(token = token).first()
    pf.verify = True
    pf.save()
    messages.success(request, 'your account has succesffuly verified.you can login')
    return redirect('loginpage')


class LoginPage(View):
    def get(self, request):
        fm = LoginForm()
        return render(request, 'home/loginpage.html', {'form' : fm})
    def post(self, request):
        fm = LoginForm(request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            
            user = authenticate(username = username, password = password)
            pro = userreg.objects.get(user = user)
            
            if pro.verify:
                login(request, user)
                
                return redirect('userhome')
            else:
                messages.info(request, 'your account is not verified,please check your email and verify your account ')
                return redirect('signup')
        else:
            messages.info(request, 'please , enter correct username or password')
            return redirect('loginpage')
        

def user_logout(request):
    logout(request)
    return redirect('homeview')
        

def cart(request):
    return render(request, 'home/cart.html')


def allproducts(request):
    return render(request, 'home/allproducts.html')


def popularitem(request):
    return render(request, 'home/popularitem.html')


def newarrival(request):
    return render(request, 'home/newarrival.html')