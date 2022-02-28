from collections import OrderedDict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce, TruncMonth, TruncYear


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_of_the_amount(queryset):

    return queryset .aggregate(amount_sum=Sum('amount'))


def summary_of_the_month(queryset):
    zmienna = (queryset
            .order_by()
            .values('date__month')
            .annotate(amount=Sum('amount')))
    return zmienna


def summary_of_the_year(queryset):
    return (queryset
            .order_by()
            .values('date__year')
            .annotate(amount=Sum('amount')))

