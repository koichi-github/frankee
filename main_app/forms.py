from django import forms

from .models import Ranking, VoteHistory, VoteQuantity

class SearchForm(forms.Form):
  keyword = forms.CharField(label='検索', max_length=100)

class RankingForm(forms.ModelForm):
  class Meta:
    model = Ranking
    fields = (
      'title',
      'category',
      'description',
      'item1',
      'item2',
      'item3',
      'item4',
      'item5',
      'item6',
      'item7',
      'item8',
      'item9',
      'item10',
      'item11',
      'item12',
      'item13',
      'item14',
      'item15',
      'item16',
      'item17',
      'item18',
      'item19',
      'item20',
      'item21',
      'item22',
      'item23',
      'item24',
      'item25',
      'item26',
      'item27',
      'item28',
      'item29',
      'item30',
    )
