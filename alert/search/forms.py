# This software and any associated files are copyright 2010 Brian Carver and
# Michael Lissner.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from alert.search.models import Court
from alert.search.models import DOCUMENT_STATUSES
from django import forms

REFINE_CHOICES = (
        ('new', 'Reset filters'),
        ('refine', 'Keep filters'),
    )

SORT_CHOICES = (
        ('score asc', 'Relevance'),
        ('dateFiled desc', 'Date: newest first'),
        ('dateFiled asc', 'Date: oldest first'),
    )

class SearchForm(forms.Form):
    q = forms.CharField(required=False, initial='*')
    sort = forms.ChoiceField(
                         choices=SORT_CHOICES,
                         initial='rel',
                         required=False,
                         widget=forms.Select(
                                   attrs={'class': 'external-input'}))
    case_name = forms.CharField(
                        required=False,
                        widget=forms.TextInput(
                                   attrs={'class': 'span-5 external-input'}))
    filed_before = forms.DateTimeField(
                        required=False,
                        widget=forms.TextInput(
                                   attrs={'placeholder': 'YYYY-MM-DD',
                                          'class': 'span-3 external-input'}))
    filed_after = forms.DateTimeField(
                        required=False,
                        widget=forms.TextInput(
                                   attrs={'placeholder': 'YYYY-MM-DD',
                                          'class': 'span-3 external-input'}))
    west_cite = forms.CharField(
                        required=False,
                        widget=forms.TextInput(
                                   attrs={'class': 'span-5 external-input'}))
    docket_number = forms.CharField(
                        required=False,
                        widget=forms.TextInput(
                                   attrs={'class': 'span-5 external-input'}))

    def __init__(self, *args, **kwargs):
        print "Form init called..."
        super(SearchForm, self).__init__(*args, **kwargs)

        # Query the DB so we can build up check boxes for each court in use.  
        courts = Court.objects.filter(in_use=True).values_list(
                                                    'courtUUID', 'short_name')
        if self.data.get('sort') is not None:
            # If there's a sort order, this is a refinement.
            self.fields['refine'] = forms.ChoiceField(
                                              choices=REFINE_CHOICES,
                                              required=False,
                                              initial='refine',
                                              widget=forms.RadioSelect())
            for court in courts:
                self.fields['court_' + court[0]] = forms.BooleanField(
                                                              label=court[1],
                                                              required=False)
            for status in DOCUMENT_STATUSES:
                self.fields['stat_' + status[0]] = forms.BooleanField(
                                                              label=status[1],
                                                              required=False)
        else:
            # It's a new query, check all the boxes.
            for court in courts:
                self.fields['court_' + court[0]] = forms.BooleanField(
                                                              label=court[1],
                                                              required=False,
                                                              initial=True,
                                                              widget=forms.CheckboxInput(attrs={'checked':'checked'}))
            for status in DOCUMENT_STATUSES:
                self.fields['stat_' + status[0]] = forms.BooleanField(
                                                              label=status[1],
                                                              required=False,
                                                              initial=True,
                                                              widget=forms.CheckboxInput(attrs={'checked':'checked'}))


    def clean_q(self):
        '''
        Cleans up various problems with the query:
         - '' --> '*'
        
        '''
        q = self.cleaned_data['q']

        if q == '' :
            return '*'
        else:
            return q

    '''
    TODO: Add validation rules here:
        - parse out invalid fields
        - use label_suffix='' to eliminate colons
        - use auto_id to change the labels/ids
    '''
