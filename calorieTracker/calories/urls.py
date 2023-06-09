from django.urls import path
from . import views

urlpatterns = [
     path('', views.getCalories, name="calories"),
     path('delete-consume/<str:pk>', views.delete_consume, name="delete-consume"),
     path('register', views.register_request, name="register"),
     path("login", views.login_request, name="login"),
     path("logout", views.logout_request, name= "logout"),
     path("caloriesDate", views.caloriesByDate, name= "calories-date"),
     path("changeLimit", views.limitChange, name= "change-limit")
]
