from . import views
from  .views import  EmailNoti, BuyerList, AcceptRequest, MyOrders, RejectRequest
from django.urls import path
urlpatterns = [
   path('emailnoti/', EmailNoti.as_view(), name = 'emailnoti'),
   path('buyerlist/<int:id>', BuyerList.as_view(), name = 'buyerlist'),
   path('buyaccept/<int:id>', AcceptRequest.as_view(), name = 'buyaccept' ),
   path('rejectbuy/<int:id>', RejectRequest.as_view(), name = 'buyreject'),
   path('sendmail/<int:id>', views.sendmail, name = 'sendmail'),
   path('rejectmail/<int:id>', views.rejectmail, name = 'rejectmail'),
   path('myorders/', MyOrders.as_view(), name = 'myorders'),
]
