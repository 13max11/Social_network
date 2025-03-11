from django import forms

class NotificationSortForm(forms.Form):
    SORT_BY_CHOICES = [
        ('all', 'усі'),
        ('unreadet', 'не прочитані'),
        ('readet', 'прочитані'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_BY_CHOICES, required=False, label='сортувати по:')