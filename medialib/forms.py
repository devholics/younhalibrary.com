from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Creator, Tag


class SearchInput(forms.TextInput):
    input_type = "search"


class MediaSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, required=False, widget=SearchInput)
    creator = forms.ModelChoiceField(queryset=Creator.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    date_after = forms.DateField(required=False)
    date_before = forms.DateField(required=False)

    keyword.widget.attrs.update({'type': 'search', 'class': 'form-control', 'placeholder': 'Keyword'})
    creator.widget.attrs.update({'class': 'form-select', 'data-placeholder': 'Creator'})
    tags.widget.attrs.update({'class': 'form-select', 'data-placeholder': 'Tags'})
    date_after.widget.attrs.update({'class': 'form-control', 'placeholder': 'ex) 1988-04-29'})
    date_before.widget.attrs.update({'class': 'form-control', 'placeholder': 'ex) 1988-04-29'})

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        limit = settings.MEDIALIB_TAG_SEARCH_LIMIT
        if tags.count() > limit:
            raise ValidationError(f'You should choose at most {limit} tags.')
        return tags
