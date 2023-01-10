from django.db import models
from djmoney.models.fields import MoneyField

from manager.models import Customer


# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=32)
    mobile = models.CharField(max_length=16)
    email = models.EmailField(max_length=125, null=False)
    address = models.TextField(max_length=100, default='')
    taxcode = models.CharField(max_length=32)
    nubank = models.CharField(max_length=16, default='0123456789ABCDEF')
    thumb = models.ImageField(blank=True, null=True, upload_to='Supplier')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Supplier'


class AssetUnit(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AssetUnit'


class AssetCategory(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'AssetCategory'


class Asset(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, null=True)
    unitIN = models.ForeignKey(AssetUnit, related_name='UnitIN', on_delete=models.CASCADE, null=False)
    purchase = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    unitINOUT = models.IntegerField(default=1)
    unitOUT = models.ForeignKey(AssetUnit, related_name='UnitOUT', on_delete=models.CASCADE, null=False)
    price = MoneyField(max_digits=16, decimal_places=0, default_currency='VND', default=0)
    thumb = models.ImageField(blank=True, null=True, upload_to='Inventory')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Asset'


class Inventory(models.Model):
    idIO = models.IntegerField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantityIO = models.SmallIntegerField()

    class Meta:
        db_table = 'Inventory'


class Purchase(models.Model):
    timeI = models.DateTimeField(auto_now_add=True)
    userID = models.SmallIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Purchase'


class Bill(models.Model):
    timeO = models.DateTimeField(auto_now_add=True)
    userID = models.SmallIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Bill'
