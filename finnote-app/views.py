from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from json import dumps 

from .models import *
from .forms import *
import datetime

def loginPage(request):
    #if else ini berguna untuk menghandle user yg sudah login agar tidak bisa mengakses halaman login lagi
    #penggunaan if else seperti ini tidak disarankan, melainkan menggunakan MIDDLEWARE
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None: #jika data user benar seperti yang ada di database
                login(request, user)
                return redirect('/home')
            else:
                messages.error(request, 'Username atau password salah')

        return render(request, 'login.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Registrasi berhasil untuk ' + user)
                return redirect('/login')

        context = {'form':form}
        return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request, 'landing.html')

def date_converter(date):
    if isinstance(date, datetime.date):
        return date.__str__()

@login_required(login_url='login') #dipake ini biar user yg belom login, tidak bisa akses halaman ini. Dipake untuk setiap halaman yg perlu authentication
def home(request):
    transaksis = request.user.transaksi_set.all().order_by('-date')[:3]
    tanggungans = request.user.tanggungan_set.all()
    transaksiAll = list(request.user.transaksi_set.all().order_by('-date').values())[:7]

    current_user_saldo = request.user.saldouser_set.first()
    form = SaldoUserForm()

    if request.method == 'POST':
        print(request.POST)
        form = SaldoUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/home')

    jumlah_tanggungan = 0
    for tanggungan in tanggungans:
        jumlah_tanggungan += tanggungan.jumlah

    context = {'form':form, 'transaksis':transaksis, 'tanggungans':tanggungans, 'current_saldo':current_user_saldo}

    if current_user_saldo is not None:
        data = [current_user_saldo.current_saldo, jumlah_tanggungan]
        data = dumps(data)
        if jumlah_tanggungan > current_user_saldo.current_saldo:
            messages.error(request, 'Jumlah tanggungan Anda melebihi saldomu sekarang!')
        context['data'] = data
        
        transaksiAll = dumps(transaksiAll, default = date_converter)
        context['transaksiAll'] = transaksiAll

    return render(request, 'list.html', context)

@login_required(login_url='login')
def inputSaldo(request, pk):
    # current_saldo = SaldoUser.objects.get(user_id=pk)
    saldo_form = SaldoUserForm()

    if request.method == 'POST':
        saldo_form = SaldoUserForm(request.POST)
        if saldo_form.is_valid():
            # saldo_form.save()
            SaldoUser = saldo_form.save(commit=False)
            SaldoUser.user_id = request.user
            SaldoUser = SaldoUser.save()
            return redirect('/home')

    context = {'saldo_form':saldo_form}

    return render(request, 'inputSaldo.html', context)

@login_required(login_url='login')
def transaksi(request):
    transaksis = request.user.transaksi_set.all().order_by('-date')
    paginator = Paginator(transaksis, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'transaksis':transaksis, 'page_obj': page_obj}
    return render(request, 'transaksi.html', context)

@login_required(login_url='login')
def tanggungan(request):
    tanggungans = request.user.tanggungan_set.all()
    paginator = Paginator(tanggungans, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'tanggungans':tanggungans, 'page_obj': page_obj}
    return render(request, 'tanggungan.html', context)

@login_required(login_url='login')
def profil(request):
    current_user_saldo = request.user.saldouser_set.first()
    tanggungan = request.user.tanggungan_set.all()
    context = {'current_saldo':current_user_saldo, 'tanggungan':tanggungan}
    return render(request, 'profil.html', context)

@login_required(login_url='login')
def addTransaksi(request, pk):
    form = TransaksiForm()
    saldo_user = SaldoUser.objects.get(user_id=pk)
    saldo_form = SaldoUserForm(instance=saldo_user)

    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            tipe = form.cleaned_data.get('jenis_transaksi')
            jumlah_uang = form.cleaned_data.get('jumlah')

            instance = saldo_form.save(commit=False)
            if tipe == 'Pemasukan':
                instance.current_saldo = instance.current_saldo + jumlah_uang
                instance.save()
            else:
                instance.current_saldo = instance.current_saldo - jumlah_uang
                instance.save()

            Transaksi = form.save(commit=False)
            Transaksi.user_id = request.user
            Transaksi = Transaksi.save()
            return redirect('/home')
        else:
            messages.error(request, 'Data tidak lengkap! Harap isi ulang.')

    context = {'form':form}
    
    return render(request, 'addTransaksi.html', context)

@login_required(login_url='login')
def addTanggungan(request, pk):
    current_user_saldo = request.user.saldouser_set.first()
    tanggungans = request.user.tanggungan_set.all()
    form = TanggunganForm()

    jumlah_tanggungan = 0
    for tanggungan in tanggungans:
        jumlah_tanggungan += tanggungan.jumlah

    if request.method == 'POST':
        form = TanggunganForm(request.POST)
        if form.is_valid():
            jumlah_uang = form.cleaned_data.get('jumlah')
            jumlah_tanggungan += jumlah_uang
            if current_user_saldo.current_saldo < jumlah_tanggungan:
                messages.error(request, 'Uang Anda tidak cukup untuk tanggungan tersebut!')
                return redirect('/home')
            else:
                Tanggungan = form.save(commit=False)
                Tanggungan.user_id = request.user
                Tanggungan = Tanggungan.save()
                return redirect('/home')

    context = {'form':form}
    
    return render(request, 'addTanggungan.html', context)

@login_required(login_url='login')
def updateTanggungan(request, pk):
    tanggungan = Tanggungan.objects.get(id=pk)
    form = TanggunganForm(instance=tanggungan)

    if request.method == 'POST':
        form = TanggunganForm(request.POST, instance=tanggungan)
        if form.is_valid():
            form.save()
            return redirect('/home')

    context = {'form':form}
    return render(request, 'updateTanggungan.html', context)

@login_required(login_url='login')
def deleteTanggungan(request, pk):
    item = Tanggungan.objects.get(id=pk)
    item.delete()

    return redirect('/home')

@login_required(login_url='login')
def deleteTransaksi(request, pk, user_id):
    item = Transaksi.objects.get(id=pk)
    saldo_user = SaldoUser.objects.get(user_id=user_id)

    if item.jenis_transaksi == 'Pemasukan':
        saldo_user.current_saldo -= item.jumlah
        saldo_user.save()
    elif item.jenis_transaksi == 'Pengeluaran':
        saldo_user.current_saldo += item.jumlah
        saldo_user.save()

    item.delete()
    messages.success(request, 'Transaksi berhasil dihapus!')
    
    return redirect('/transaksi')