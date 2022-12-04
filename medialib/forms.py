from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Creator, Media, Tag


class MediaSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, required=False)
    type = forms.ChoiceField(choices=Media.TYPE_CHOICES + (('', '---------'),), required=False)
    creator = forms.ModelChoiceField(queryset=Creator.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    keyword.widget.attrs.update({'class': 'form-control', 'placeholder': 'Keyword'})
    type.widget.attrs.update({'class': 'form-select', 'data-placeholder': 'Media type'})
    creator.widget.attrs.update({'class': 'form-select', 'data-placeholder': 'Creator'})
    tags.widget.attrs.update({'class': 'form-select', 'data-placeholder': 'Tags'})
    start_date.widget.attrs.update({'class': 'form-control', 'placeholder': 'ex) 1988-04-29'})
    end_date.widget.attrs.update({'class': 'form-control', 'placeholder': 'ex) 1988-04-29'})

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        limit = settings.MEDIALIB_TAG_SEARCH_LIMIT
        if tags.count() > limit:
            raise ValidationError(f'You should choose at most {limit} tags.')
        return tags
