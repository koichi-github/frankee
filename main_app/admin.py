from django.contrib import admin
from .models import Category, Ranking, Item, VoteHistory, VoteQuantity

admin.site.register(Category)
admin.site.register(Ranking)
admin.site.register(Item)
admin.site.register(VoteHistory)
admin.site.register(VoteQuantity)