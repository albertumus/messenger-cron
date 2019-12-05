from django.urls import path
from django.conf.urls import url
#Views Created 
from messenger import views
#Views by JWT
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    url(r'^api/check-api/$', views.check_api, name="check-api"),
    url(r'^api/send-daily-messages/$', views.send_daily_messages, name="send-daily-messages"),
    url(r'^api/token/$', jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair")
]