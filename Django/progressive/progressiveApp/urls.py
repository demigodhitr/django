from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('add_to_home/', views.addHome, name='add_to_home'),
    path('index_crypto/', views.index_crypto, name='index_crypto'),
    path('index_secondary/', views.index_secondary, name='index_secondary'),
    path('index_waves/', views.index_waves, name='index_waves'),
    path('addCard/', views.menu_add_card, name='addCard'),
    path('setCard/', views.menu_set_card, name='setCard'),
    path('exchange/', views.menu_exchange, name='exchange'),
    path('tofriends/', views.menu_friends, name='tofriends'),
    path('highlights/', views.menu_highlights, name='highlights'),
    path('notifications/', views.menu_notifications, name='notifications'),
    path('opener/', views.menu_sidebar, name='opener'),
    path('transfer/', views.menu_transfer, name='transfer'),
    path('activities/', views.page_activity, name='activities'),
    path('crypto_reports/', views.page_crypto_report, name='crypto_reports'),
    path('page_payment/', views.page_payments, name='page_payment'),
    path('profile/', views.page_profile, name='profile'),
    path('page_reports/', views.page_report, name='page_reports'),
    path('signin/', views.page_signin, name='signin'),
    path('signup/', views.page_signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('logout/', views.signout, name='logout'),
    path('terms/', views.page_terms, name='terms'),
    path('wallet/', views.page_wallet, name='wallet'),
    path('pages/', views.pages, name='pages'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('walkthrough/', views.walkthrough, name='walkthrough'),
    path('walkthrough_slides/', views.walkthrough_slide, name='walkthrough_slides'),
    path('deposit/', views.deposit, name='deposit'), 
    path('verification/', views.verification, name='verification'), 
    path('registration/', views.secondary_view, name='registration'), 
    path('index_signup/', views.index_signup, name='index_signup'), 

    #Password Reset urls.
    #passReset
    path('reset_password/', views.custom_password_reset, name='password_reset'),
    path('reset_password_done/', views.custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_complete/', views.custom_password_reset_complete, name='password_reset_complete'),
    #passreset
]