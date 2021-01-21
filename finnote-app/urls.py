from django.urls import path
from . import views

#urls.py digunakan untuk menghandle bagaimana url akan bekerja dan diberi nama untuk memudahkan, contohnya pada redirect

urlpatterns = [
    path('', views.index, name='test'),
    path('home/', views.home, name='home'),
    path('input-saldo/<str:pk>/', views.inputSaldo, name='inputSaldo'),
    path('transaksi/', views.transaksi, name='transaksi'),
    path('tanggungan/', views.tanggungan, name='tanggungan'),
    path('tambah-transaksi/<str:pk>/', views.addTransaksi, name='addTransaksi'),
    path('tambah-tanggungan/<str:pk>/', views.addTanggungan, name='addTanggungan'),
    path('edit-tanggungan/<str:pk>/', views.updateTanggungan, name='updateTanggungan'),
    path('hapus-tanggungan/<str:pk>/', views.deleteTanggungan, name='deleteTanggungan'),
    path('profil/', views.profil, name='profil'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
]