from . import views
from  .views import  EmailNoti, BuyerList, AcceptRequest
from django.urls import path
urlpatterns = [
   path('emailnoti/', EmailNoti.as_view(), name = 'emailnoti'),
   path('buyerlist/<int:id>', BuyerList.as_view(), name = 'buyerlist'),
   path('buyaccept/<int:id>', AcceptRequest.as_view(), name = 'buyaccept' ),
]
