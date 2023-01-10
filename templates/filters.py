import django_filters
from models import Customer

class Customer_Filter(django_filters.FilterSet):
  class Meta:
    model = Customer
    fields = {
      'full_name': ['icontains'],
      'mobile': ['icontains']
    }
