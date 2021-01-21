from django.db import models
from django.contrib.auth.models import User

# models.py berfungsi untuk membuat tabel

class Transaksi(models.Model):
    JENIS = (
        ('Pemasukan', 'Pemasukan'),
        ('Pengeluaran', 'Pengeluaran'),
    )

    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    nama = models.CharField(max_length=200, null=True)
    jenis_transaksi = models.CharField(max_length=30, choices=JENIS)
    jumlah = models.IntegerField()
    date = models.DateField()

class Tanggungan(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    nama = models.CharField(max_length=200)
    jumlah = models.IntegerField()

class SaldoUser(models.Model):
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    current_saldo = models.IntegerField()
