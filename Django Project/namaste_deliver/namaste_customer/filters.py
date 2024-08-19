# filters.py
import django_filters
from .models import OrderModel, MenuItem

class OrderFilter(django_filters.FilterSet):
    created_on = django_filters.DateTimeFromToRangeFilter(field_name='created_on')
    price = django_filters.RangeFilter()
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    items = django_filters.ModelMultipleChoiceFilter(queryset=MenuItem.objects.all())

class Meta:
        model = OrderModel
        fields = ['name', 'email', 'created_on', 'price', 'items']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'created_on': 'Created On',
            'price__gte': 'Minimum Price',
            'price__lte': 'Maximum Price',
            'items': 'Items',
        }

