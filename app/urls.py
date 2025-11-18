from django.urls import path, re_path

from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView

from . import views





## All app urls here ...


urlpatterns = [

    path('', views.home, name="home"),


    path('login/', views.loginPage, name="login"),


    path('register/', views.clientregisterPage, name="register"),


    path('activate/<uidb64>/<token>/', views.activate, name='activate'),


    path('clienthome/', views.clienthome, name='clienthome'),


    path('adminhome/', views.adminhome, name='adminhome'),


    path('about/', TemplateView.as_view(template_name='app/about.html'), name="about"),

    path('services/', TemplateView.as_view(template_name='app/services.html'), name="services"),
    
    path('contact/', TemplateView.as_view(template_name='app/contact.html'), name="contact"),


    path('customerdetail/', views.customerdetail, name="customerdetail"),


    path('detail/<int:hospital_id>/', views.detail, name='detail'),


    path('hospital_list/', views.findHospital, name="hospital_list"),




    ## URLS for Resetting Password

    # 1st step - Password reset garna ko lagi, email id halnu parxa so tyo page ko URL ho
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="app/password_reset.html"), name="reset_password"),
    # auth_views.PasswordResetView.as_view  -> yaha  .as_view kina gareko vanda PasswordResetView chai django ko default class view ho so testo view ko lagi  .as_view garna parxa  &  testo defualt django view le default django template nai render garauxa.. so yedi hamilai django ko default template man parena vani teslai override pani garna sakxau . So, to override that page ->  (template_name="accounts/password_reset.html)


    # 2nd step - Email ID hali sake paxi, paswword reset link send vai sakyo tapaiko mail ma vanera jun page display hunxa tyo page ko lagi URL ho 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_sent.html"), name="password_reset_done"),


    # 3rd Step - Naya Password halna ko lagi or Confirm garna ko lagi... yo page display garne URL ho
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_form.html"), name="password_reset_confirm"),


    # 4th Step - Password reset Sucess vai sake paxi,, password reset complete vayo aba tapai feri login garna saknu hunxa vanera jun Page display hunxa tesko URL ko lagi
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_done.html"), name="password_reset_complete"),




    ## url for log out
    path('logoutall/', views.logoutall, name="logoutall"),







    ## just for demo: for leanring google maps javascript api service integration in webpage for learning purpose only
    # path('map/', views.demo_map_page, name='map'),

]