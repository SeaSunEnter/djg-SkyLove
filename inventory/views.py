import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import FormMixin

from inventory.forms import AssetCategoryForm, AssetForm, SupplierForm, AssetUnitForm, AssetFilterForm, InventoryForm
from inventory.models import AssetCategory, Asset, Supplier, AssetUnit, Inventory, Purchase


# Create your views here.

# AssetCategory views
class AssetCategoryAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/assetcategory/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assetcategories'] = AssetCategory.objects.order_by('id')
        return context


class AssetCategoryNew(LoginRequiredMixin, CreateView):
    model = AssetCategory
    template_name = 'inventory/assetcategory/create.html'
    form_class = AssetCategoryForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:ass_cat_all')


class AssetCategoryUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/assetcategory/edit.html'
    form_class = AssetCategoryForm
    login_url = 'manager:login'
    model = AssetCategory
    success_url = reverse_lazy('inventory:ass_cat_all')


# AssetUnit views
class AssetUnitAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/assetunit/index.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assetunits'] = AssetUnit.objects.order_by('name')
        return context


class AssetUnitNew(LoginRequiredMixin, CreateView):
    model = AssetCategory
    template_name = 'inventory/assetunit/create.html'
    form_class = AssetUnitForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:ass_unt_all')


class AssetUnitUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/assetunit/edit.html'
    form_class = AssetUnitForm
    login_url = 'manager:login'
    model = AssetUnit
    success_url = reverse_lazy('inventory:ass_unt_all')


# Asset views
class AssetAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/asset/overview.html'
    login_url = 'manager:login'
    model = Asset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = AssetCategory.objects.order_by('id')
        context['assets'] = Asset.objects.order_by('id')
        context['asset_total'] = Asset.objects.all().count()
        return context


class AssetNew(LoginRequiredMixin, CreateView):
    model = Asset
    template_name = 'inventory/asset/create.html'
    form_class = AssetForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:asset_all')


class AssetUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/asset/edit.html'
    form_class = AssetForm
    login_url = 'manager:login'
    model = Asset
    success_url = reverse_lazy('inventory:asset_all')


class AssetView(LoginRequiredMixin, DetailView):
    queryset = Asset.objects.select_related('category')
    template_name = 'inventory/asset/single.html'
    context_object_name = 'asset'
    login_url = 'manager:login'


# Supplier views
class SupplierAll(LoginRequiredMixin, ListView):
    template_name = 'inventory/supplier/overview.html'
    login_url = 'manager:login'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suppliers'] = Supplier.objects.order_by('id')
        return context


class SupplierNew(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'inventory/supplier/create.html'
    form_class = SupplierForm
    login_url = 'manager:login'
    success_url = reverse_lazy('inventory:supplier_all')


class SupplierUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'inventory/supplier/edit.html'
    form_class = SupplierForm
    login_url = 'manager:login'
    model = Supplier
    success_url = reverse_lazy('inventory:supplier_all')


class SupplierView(LoginRequiredMixin, DetailView):
    queryset = Supplier.objects.order_by('id')
    template_name = 'inventory/supplier/single.html'
    context_object_name = 'supplier'
    login_url = 'manager:login'


class InventoryView(LoginRequiredMixin, ListView):
    template_name = 'inventory/inv/overview.html'
    model = Inventory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """"""
        context['inventories'] = \
            Inventory.objects.values(
                'asset',
                'asset__thumb',
                'asset__name',
                'asset__category__name').order_by('asset').annotate(quantity=Sum('quantityIO'))
        """"""
        # context['inventories'] = Inventory.objects.order_by('id')
        context['categories'] = AssetCategory.objects.order_by('id')
        return context


class PurchaseNew(LoginRequiredMixin, FormMixin, ListView):
    model = Purchase
    template_name = 'inventory/inv/create.html'
    form_class = InventoryForm
    login_url = 'manager:login'

    def get_success_url(self):
        return reverse('inventory:inv_all')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.form_class
        form = self.get_form()
        if form.is_valid():
            Purchase.objects.create(
                userID=request.user.pk,
                supplier=form.cleaned_data['supplier']
            )
            Inventory.objects.create(
                idIO=Purchase.objects.all().count(),
                asset=form.cleaned_data['asset'],
                quantityIO=form.cleaned_data['quantityIO']
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message # passed in form.cleaned_data['message']
        return super().form_valid(form)
