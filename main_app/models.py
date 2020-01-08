from django.db import models
import uuid

# カテゴリモデル
class  Category(models.Model):
  class Meta:
        db_table = 'category'

  name = models.CharField(verbose_name='カテゴリ名', max_length=255)

  def __str__(self):
    return self.name


# ランキングモデル
class Ranking(models.Model):
  class Meta:
        db_table = 'ranking'

  # 主キーをUUIDに変更
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

  title = models.CharField(verbose_name='タイトル', max_length=255)
  description = models.TextField(
    verbose_name='説明',
    blank=True,
    max_length=1000,
  )
  item1 = models.CharField(verbose_name='項目１', max_length=255)
  item2 = models.CharField(verbose_name='項目２', max_length=255)
  item3 = models.CharField(verbose_name='項目３', max_length=255)
  item4 = models.CharField(verbose_name='項目４', max_length=255, blank=True)
  item5 = models.CharField(verbose_name='項目５', max_length=255, blank=True)
  item6 = models.CharField(verbose_name='項目６', max_length=255, blank=True)
  item7 = models.CharField(verbose_name='項目７', max_length=255, blank=True)
  item8 = models.CharField(verbose_name='項目８', max_length=255, blank=True)
  item9 = models.CharField(verbose_name='項目９', max_length=255, blank=True)
  item10 = models.CharField(verbose_name='項目１０', max_length=255, blank=True)
  item11 = models.CharField(verbose_name='項目１１', max_length=255, blank=True)
  item12 = models.CharField(verbose_name='項目１２', max_length=255, blank=True)
  item13 = models.CharField(verbose_name='項目１３', max_length=255, blank=True)
  item14 = models.CharField(verbose_name='項目１４', max_length=255, blank=True)
  item15 = models.CharField(verbose_name='項目１５', max_length=255, blank=True)
  item16 = models.CharField(verbose_name='項目１６', max_length=255, blank=True)
  item17 = models.CharField(verbose_name='項目１７', max_length=255, blank=True)
  item18 = models.CharField(verbose_name='項目１８', max_length=255, blank=True)
  item19 = models.CharField(verbose_name='項目１９', max_length=255, blank=True)
  item20 = models.CharField(verbose_name='項目２０', max_length=255, blank=True)
  item21 = models.CharField(verbose_name='項目２１', max_length=255, blank=True)
  item22 = models.CharField(verbose_name='項目２２', max_length=255, blank=True)
  item23 = models.CharField(verbose_name='項目２３', max_length=255, blank=True)
  item24 = models.CharField(verbose_name='項目２４', max_length=255, blank=True)
  item25 = models.CharField(verbose_name='項目２５', max_length=255, blank=True)
  item26 = models.CharField(verbose_name='項目２６', max_length=255, blank=True)
  item27 = models.CharField(verbose_name='項目２７', max_length=255, blank=True)
  item28 = models.CharField(verbose_name='項目２８', max_length=255, blank=True)
  item29 = models.CharField(verbose_name='項目２９', max_length=255, blank=True)
  item30 = models.CharField(verbose_name='項目３０', max_length=255, blank=True)

  # relation
  creator = models.ForeignKey(
    'auth.User',
    on_delete=models.CASCADE,
    null=True,
    blank=True,
  )
  category = models.ManyToManyField(Category, verbose_name='カテゴリ', blank=True)

  # 現在の時間で更新
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return self.title


# 項目モデル
class Item(models.Model):
  class Meta:
        db_table = 'item'

  item = models.IntegerField(verbose_name='項目')

  def __str__(self):
    return str(self.item)


# 投票履歴モデル
class VoteHistory(models.Model):
  class Meta:
    db_table = 'vote_history'

  # relation
  voter = models.ForeignKey(
    'auth.User',
    on_delete=models.CASCADE,
    null=True,
    blank=True,
  )
  items = models.ForeignKey(Item, verbose_name='項目', on_delete=models.CASCADE)
  rankings = models.ForeignKey(Ranking, verbose_name='ランキングID', on_delete=models.CASCADE)

  # 現在の時間で更新
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return self.rankings.title + " / " + eval("self.rankings.item" + str(self.items))


# 投票数モデル
class VoteQuantity(models.Model):
  class Meta:
    db_table = 'vote_quantity'
  
  quantity = models.IntegerField(verbose_name='投票数', default=0)

  # relation
  items = models.ForeignKey(Item, verbose_name='項目', on_delete=models.CASCADE)
  rankings = models.ForeignKey(Ranking, verbose_name='ランキングID', on_delete=models.CASCADE)

  # 現在の時間で更新
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return self.rankings.title + " / " + eval("self.rankings.item" + str(self.items))

