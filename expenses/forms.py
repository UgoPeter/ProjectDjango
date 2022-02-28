from django import forms
from django.db.models import Count, F, Value, TextField
from django.db.models.functions import Coalesce, Concat

from .models import Expense, Category


class ModelChoiceCategoryField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.name}  ({obj.category_with_sum})'


class ExpenseSearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name',)

    # To do - MultipleModelChoiceField
    category_multiple = forms.MultipleChoiceField(required=False)
    date_from = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), required=False)
    date_to = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), required=False)

    sort_category = forms.ChoiceField(required=False)
    sort_date = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_queryset = Category.objects.all().annotate(expense_count=Count('expense__id'),
                                                            category_with_sum=Concat(F('name'),
                                                                                     Value(' ('),
                                                                                     F('expense_count'),
                                                                                     Value(')'),
                                                                                     output_field=TextField()))
        self.fields['name'].required = False
        self.fields['category_multiple'].choices = [(item.id, item.category_with_sum) for item in category_queryset]
        self.fields['sort_category'].choices = [('', ''), ('asc', 'ascending'), ('desc', 'descending')]
        self.fields['sort_date'].choices = [('', ''), ('asc', 'ascending'), ('desc', 'descending')]
