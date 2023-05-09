from django.forms import DateInput, RadioSelect
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, ChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    p_type = ChoiceFilter(
        choices=Post.TP,
        widget=RadioSelect,
        label='Тип публикации',
    )
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория',
        help_text='(или одна или несколько)',
        conjoined=True,
    )
    time = DateTimeFilter(
        field_name='time',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
            }
