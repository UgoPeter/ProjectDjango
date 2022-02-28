import datetime

from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_of_the_amount, summary_of_the_month, summary_of_the_year


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if len(name) > 0:
                queryset = queryset.filter(name__icontains=name)

            date_from = form.cleaned_data.get('date_from', '')
            if type(date_from) == datetime.date:
                queryset = queryset.filter(date__gte=date_from)

            date_to = form.cleaned_data.get('date_to', '')
            if type(date_to) == datetime.date:
                queryset = queryset.filter(date__lte=date_to)

            # To do
            category_multiple = list(map(int, form.cleaned_data.get('category_multiple', '')))
            if len(category_multiple) != 0:
                queryset = queryset.filter(category__id__in=category_multiple)

            sort_values = ['asc', 'desc']
            sort_category = form.cleaned_data.get('sort_category', '')
            if sort_category in sort_values:
                sort_category_type = 'category__name' if sort_category == 'asc' else '-category__name'
                queryset = queryset.order_by(sort_category_type)

            sort_date = form.cleaned_data.get('sort_date', '')
            if sort_date in sort_values:
                sort_date_type = 'date' if sort_date == 'asc' else '-date'
                queryset = queryset.order_by(sort_date_type)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs,
            summary_of_the_amount=summary_of_the_amount(queryset),
            **kwargs,
            summary_of_the_month=summary_of_the_month(queryset),
            **kwargs,
            summary_of_the_year=summary_of_the_year(queryset),
            **kwargs
        )


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
