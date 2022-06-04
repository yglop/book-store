from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('user_settings/', views.user_settings, name='user_settings'),
    path('become_seller/', views.become_seller, name='become_seller'),
    path('user_page/<int:id>/', views.user_page, name='user_page'),

    path('book_management/', views.book_management, name='book_management'),
    path('book_creation/', views.book_creation, name='book_creation'),
    path('book_redaction/<int:id>/', views.book_redaction, name='book_redaction'),
    path('book_delete/<int:id>/', views.book_delete, name='book_delete'),
    path('book_page/<int:id>/', views.book_page, name='book_page'),
    path('book_buy/<int:id>/', views.book_buy, name='book_buy'),

    path('search/', views.search, name='search'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
         name='password_reset_complete'),
]


'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''