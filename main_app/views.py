from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Ranking, Item ,VoteHistory, VoteQuantity
from .forms import SearchForm
from .forms import RankingForm

class IndexView(View):
    def get(self, request, *args, **kwargs):
        searchForm = SearchForm(request.GET)
        if searchForm.is_valid():
            keyword = searchForm.cleaned_data['keyword']
            rankings = Ranking.objects.filter(title__contains=keyword)
        else:
            searchForm = SearchForm()
            rankings = Ranking.objects.all()

        # rank_list =[]
        # for ranking in rankings:
        #     for i in range(1,31):
        #         rank_list.append(eval("ranking.item" + str(i)))

        rankings_dict = {}
        for i in range(rankings.count()):
            temp_dict = {}
            temp_dict['uuid'] = rankings[i].uuid
            temp_dict['title'] = rankings[i].title
            categories_str = ""
            for j in range(rankings[i].category.all().count()):
                if j == rankings[i].category.all().count() - 1:
                    categories_str += rankings[i].category.all()[j].name
                else:
                    categories_str += rankings[i].category.all()[j].name + " "
            print(categories_str)
            temp_dict['categories'] = categories_str
            
            rankings_dict["dict" + str(i+1)] = temp_dict
        print(rankings_dict)

        if str(self.request.user) == "AnonymousUser":
            message = "Frankee へようこそ！！"
        else:
            message = str(self.request.user) + 'さんこんにちは'
            
        context = {
            'message': message,
            'rankings': rankings,
            # 'rank_list': rank_list,
            'searchForm': searchForm,
            'rankings_dict': rankings_dict,
        }
        return render(request, 'main_app/index.html', context)

class DetailView(View):
    def get (self, request, id, *args, **kwargs):
        ranking = get_object_or_404(Ranking, pk=id)

        # 1~30位の投票数をリストに格納
        quantity_list = []
        for i in range(1,31):
            temp_item_id = Item.objects.get(item=i).id
            print("temp_item_id : " + str(temp_item_id))
            if VoteQuantity.objects.filter(rankings_id=id, items__id=temp_item_id).exists():
                temp_vote_quantity_id = VoteQuantity.objects.get(rankings_id=id, items__id=temp_item_id).id
                print("temp_vote_quantity_id : " + str(temp_vote_quantity_id))
                vote_quantity = get_object_or_404(VoteQuantity, pk=temp_vote_quantity_id)
                quantity_list.append(vote_quantity.quantity)
            else:
                quantity_list.append(0)

        # ランキングの項目の数を取得
        item_range = 0
        for i in range(1,31):
            if eval("ranking.item" + str(i)) == "":
                item_range = i - 1
                break

        # ランキングの項目名をリストに格納
        item_name_list = []
        for i in range(1,31):
            item_name_list.append(eval("ranking.item" + str(i)))

        # 投票数の順位をリストに格納
        quantity_rank_list = [0] * 30
        for i in range(len(VoteQuantity.objects.filter(rankings_id=id))):
            quantity_rank = int(str(VoteQuantity.objects.filter(rankings_id=id).order_by('-quantity')[:item_range][::1][i].items))
            print(quantity_rank)
            # temp_item_id = Item.objects.filter(item__iexact=quantity_rank)[0].id
            quantity_rank_list[i] = quantity_rank

        sorted_item_name_list = [""] * 30
        sorted_quantity_list = [0] * 30
        for i in range(len(VoteQuantity.objects.filter(rankings_id=id))):
            sorted_item_name_list[i] = item_name_list[quantity_rank_list[i] - 1]
            sorted_quantity_list[i] = quantity_list[quantity_rank_list[i] - 1]

        # カテゴリをリスト化
        categories_list = []
        category_count = ranking.category.all().count()
        for i in range(category_count):
            categories_list.append(str(ranking.category.all()[i].name))

        if str(self.request.user) != "AnonymousUser":
            # 投票履歴からそのユーザの投票数を取得
            if VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).exists():
                user_vote_quantity = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).count()
            else:
                user_vote_quantity = 0

            # 投票可能な数
            voteable_quantity = 10

            # ユーザが投票可能か判定
            if voteable_quantity - user_vote_quantity > 0:
                voteable_Judgment = 1
            else:
                voteable_Judgment = 0

            # ユーザの投票数をリストに格納し、全体の投票数の大きい順に並べ替え
            user_vote_quantity_list = [0] * item_range
            sorted_user_vote_quantity_list = [0] * item_range
            if VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).exists():
                for i in range(user_vote_quantity):
                    user_voted_items = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id)[i].items.item
                    user_vote_quantity_list[user_voted_items - 1] += 1
                for i in range(user_vote_quantity):
                    sorted_user_vote_quantity_list[i] = user_vote_quantity_list[quantity_rank_list[i] - 1]
        else:
            voteable_Judgment = 0
            sorted_user_vote_quantity_list = []

        print("uuid : " + str(id))
        print("item_range : " + str(item_range))
        print("item_name_list : " + str(item_name_list))
        print("quantity_list : " + str(quantity_list))
        print("quantity_rank_list : " + str(quantity_rank_list))
        print("sorted_item_name_list : " + str(sorted_item_name_list))
        print("sorted_quantity_list : " + str(sorted_quantity_list))
        print("categories_list : " + str(categories_list))

        context = {
            'message': 'ランキングID： ' + str(id),
            'ranking': ranking,
            'sorted_item_name_list': sorted_item_name_list,
            'sorted_quantity_list': sorted_quantity_list,
            'item_range': item_range,
            'request_user': str(self.request.user),
            'categories_list': categories_list,
            'voteable_Judgment': voteable_Judgment,
            'sorted_user_vote_quantity_list': sorted_user_vote_quantity_list,
        }
        return render(request, 'main_app/detail.html', context)

class CreateView(LoginRequiredMixin, View):
    def post (self, request, *args, **kwargs):
        rankingForm = RankingForm(request.POST)

        if rankingForm.is_valid():
            ranking = rankingForm.save(commit=False)
            ranking.creator = self.request.user
            ranking = rankingForm.save()
            
        # ranking = Ranking(title='Test', item1='test1', item2='test2', item3='test2')
        # ranking.category_id = 5
        # ranking.save()

        # quantity_list = []
        print(ranking.title)

        # ランキングの項目の数を取得
        item_range = 0
        for i in range(1,31):
            if eval("ranking.item" + str(i)) == "":
                item_range = i - 1
                break
        
        # 各項目の投票数に0をセット
        for i in range(item_range):
            vote_quantity = VoteQuantity(
                quantity = 0,
            )
            vote_quantity.items_id = Item.objects.get(item=i + 1).id
            vote_quantity.rankings_id = ranking.uuid
            vote_quantity.save()

        # ランキングの項目名をリストに格納
        item_name_list = []
        for i in range(1,item_range + 1):
            item_name_list.append(eval("ranking.item" + str(i)))
        
        print("item_name_list : " + str(item_name_list))


        # 投票数の順位をリストに格納
        quantity_rank_list = [0] * 30
        for i in range(len(VoteQuantity.objects.filter(rankings_id=ranking.uuid))):
            quantity_rank = int(str(VoteQuantity.objects.filter(rankings_id=ranking.uuid).order_by('-quantity')[:item_range][::1][i].items))
            print(quantity_rank)
            quantity_rank_list[i] = quantity_rank
        print(quantity_rank_list)

        sorted_item_name_list = [""] * 30
        sorted_quantity_list = [0] * 30
        for i in range(0, len(VoteQuantity.objects.filter(rankings_id=ranking.uuid))):
            sorted_item_name_list[i] = item_name_list[quantity_rank_list[i] - 1]
            # sorted_quantity_list[i] = quantity_list[quantity_rank_list[i] - 1]

        # カテゴリをリスト化
        categories_list = []
        category_count = ranking.category.all().count()
        for i in range(category_count):
            categories_list.append(str(ranking.category.all()[i].name))

        # 投票履歴からそのユーザの投票数を取得
        if VoteHistory.objects.filter(voter=self.request.user, rankings_id=ranking.uuid).exists():
            user_vote_quantity = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).count()
        else:
            user_vote_quantity = 0

        # 投票可能な数
        voteable_quantity = 10

        # ユーザが投票可能か判定
        if voteable_quantity - user_vote_quantity > 0:
            voteable_Judgment = 1
        else:
            voteable_Judgment = 0

        # ユーザの投票数をリストに格納し、全体の投票数の大きい順に並べ替え
        user_vote_quantity_list = [0] * item_range
        sorted_user_vote_quantity_list = [0] * item_range
        if VoteHistory.objects.filter(voter=self.request.user, rankings_id=ranking.uuid).exists():
            for i in range(user_vote_quantity):
                user_voted_items = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id)[i].items.item
                user_vote_quantity_list[user_voted_items - 1] += 1
            for i in range(user_vote_quantity):
                sorted_user_vote_quantity_list[i] = user_vote_quantity_list[quantity_rank_list[i] - 1]

        print("uuid : " + str(id))
        print("item_range : " + str(item_range))
        print("item_name_list : " + str(item_name_list))
        # print("quantity_list : " + str(quantity_list))
        print("quantity_rank_list : " + str(quantity_rank_list))
        print("sorted_item_name_list : " + str(sorted_item_name_list))
        print("sorted_quantity_list : " + str(sorted_quantity_list))
        print("categories_list : " + str(categories_list))

        context = {
            'message': str(ranking.uuid) + 'を作成しました',
            'ranking': ranking,
            'sorted_item_name_list': sorted_item_name_list,
            'sorted_quantity_list': sorted_quantity_list,
            'item_range': item_range,
            'categories_list': categories_list,
            'voteable_Judgment': voteable_Judgment,
            'sorted_user_vote_quantity_list': sorted_user_vote_quantity_list,
        }
        return render(request, 'main_app/detail.html', context)

class DeleteView(LoginRequiredMixin, View):
    def get (self, request, id, *args, **kwargs):
        ranking = get_object_or_404(Ranking, pk=id)
        ranking.delete()

        rankings = Ranking.objects.all()
        context = {
            'message': ranking.title + "を削除しました",
            # 'message': str(id) + "を削除しました",
            'rankings': rankings,
        }
        return render(request, 'main_app/index.html', context)

class NewView(LoginRequiredMixin, View):
    def get (self, request, *args, **kwargs):
        rankingForm = RankingForm()

        context = {
            'message': 'ランキングの新規作成',
            'rankingForm': rankingForm,
        }
        return render(request, 'main_app/new.html', context)

class EditView(LoginRequiredMixin, View):
    def get (self, request, id, *args, **kwargs):
        ranking = get_object_or_404(Ranking, pk=id)
        rankingForm = RankingForm(instance=ranking)

        context = {
            'message': 'ランキングの編集' + str(id),
            'ranking': ranking,
            'rankingForm': rankingForm,
        }
        return render(request, 'main_app/edit.html', context)

class UpdateView(LoginRequiredMixin, View):
    def post (self, request, id, *args, **kwargs):
        ranking = get_object_or_404(Ranking, pk=id)
        rankingForm = RankingForm(request.POST, instance=ranking)
        if rankingForm.is_valid():
            ranking = rankingForm.save(commit=False)
            if ranking.creator != self.request.user:
                raise PermissionDenied('You do not have permission to edit.')
            else:
                ranking = rankingForm.save()

        quantity_list = []
        for i in range(1,31):
            temp_item_id = Item.objects.get(item=i).id
            print("temp_item_id : " + str(temp_item_id))
            if VoteQuantity.objects.filter(rankings_id=id, items__id=temp_item_id).exists():
                temp_vote_quantity_id = VoteQuantity.objects.get(rankings_id=id, items__id=temp_item_id).id
                print("temp_vote_quantity_id : " + str(temp_vote_quantity_id))
                vote_quantity = get_object_or_404(VoteQuantity, pk=temp_vote_quantity_id)
                quantity_list.append(vote_quantity.quantity)
            else:
                quantity_list.append(0)

        # ランキングの項目の数を取得
        item_range = 0
        for i in range(1,31):
            if eval("ranking.item" + str(i)) == "":
                item_range = i - 1
                break

        # ランキングの項目名をリストに格納
        item_name_list = []
        for i in range(1,31):
            item_name_list.append(eval("ranking.item" + str(i)))

        # 投票数の順位をリストに格納
        quantity_rank_list = [0] * 30
        for i in range(len(VoteQuantity.objects.filter(rankings_id=id))):
            quantity_rank = int(str(VoteQuantity.objects.filter(rankings_id=id).order_by('-quantity')[:item_range][::1][i].items))
            print(quantity_rank)
            quantity_rank_list[i] = quantity_rank
        print(quantity_rank_list)
        sorted_item_name_list = [""] * 30
        sorted_quantity_list = [0] * 30
        for i in range(0, len(VoteQuantity.objects.filter(rankings_id=id))):
            sorted_item_name_list[i] = item_name_list[quantity_rank_list[i] - 1]
            sorted_quantity_list[i] = quantity_list[quantity_rank_list[i] - 1]

        # カテゴリをリスト化
        categories_list = []
        category_count = ranking.category.all().count()
        for i in range(category_count):
            categories_list.append(str(ranking.category.all()[i].name))

        # 投票履歴からそのユーザの投票数を取得
        if VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).exists():
            user_vote_quantity = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).count()
        else:
            user_vote_quantity = 0

        # 投票可能な数
        voteable_quantity = 10

        # ユーザが投票可能か判定
        if voteable_quantity - user_vote_quantity > 0:
            voteable_Judgment = 1
        else:
            voteable_Judgment = 0

        # ユーザの投票数をリストに格納し、全体の投票数の大きい順に並べ替え
        user_vote_quantity_list = [0] * item_range
        sorted_user_vote_quantity_list = [0] * item_range
        if VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).exists():
            for i in range(user_vote_quantity):
                user_voted_items = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id)[i].items.item
                user_vote_quantity_list[user_voted_items - 1] += 1
            for i in range(user_vote_quantity):
                sorted_user_vote_quantity_list[i] = user_vote_quantity_list[quantity_rank_list[i] - 1]

        print("uuid : " + str(id))
        print("item_range : " + str(item_range))
        print("item_name_list : " + str(item_name_list))
        print("quantity_list : " + str(quantity_list))
        print("quantity_rank_list : " + str(quantity_rank_list))
        print("sorted_item_name_list : " + str(sorted_item_name_list))
        print("sorted_quantity_list : " + str(sorted_quantity_list))
        print("categories_list : " + str(categories_list))

        context = {
            'message': str(id) + 'を更新しました',
            'ranking': ranking,
            'sorted_item_name_list': sorted_item_name_list,
            'sorted_quantity_list': sorted_quantity_list,
            'item_range': item_range,
            'categories_list': categories_list,
            'voteable_Judgment': voteable_Judgment,
            'sorted_user_vote_quantity_list': sorted_user_vote_quantity_list,
        }
        return render(request, 'main_app/detail.html', context)

class VoteView(LoginRequiredMixin, View):
    def post (self, request, id, *args, **kwargs):
        ranking = get_object_or_404(Ranking, pk=id)

        # ランキングの項目の数を取得
        item_range = 0
        for i in range(1,31):
            if eval("ranking.item" + str(i)) == "":
                item_range = i - 1
                break

        # クリックした投票ボタンの場所を取得
        for i in range(1,31):
            vote_place = request.POST.get("vote_place" + str(i), False)
            vote_cancel_place = request.POST.get("vote_cancel_place" + str(i), False)
            if vote_place == "True":
                vote_status = "vote"
                true_vote_place = i
                print("選ばれたのはplace" + str(true_vote_place) + "の投票でした。")
            if vote_cancel_place == "True":
                vote_status = "vote_cancel"
                true_vote_cancel_place = i
                print("選ばれたのはplace" + str(true_vote_cancel_place) + "の取消でした。")

        # 投票するか投票キャンセルか(vote_status)で分岐
        if vote_status == "vote":
            true_vote_item = VoteQuantity.objects.filter(rankings_id=id).order_by('-quantity')[:item_range][::1][true_vote_place - 1].items.item
            print("true_vote_item : " + str(true_vote_item))
            rial_item_id = Item.objects.get(item=true_vote_item).id

            vote_history = VoteHistory(
                voter = self.request.user,
            )
            vote_history.items_id = rial_item_id
            vote_history.rankings_id = ranking.uuid
            vote_history.save()

            if VoteQuantity.objects.filter(rankings_id=id, items__id=rial_item_id).exists():
                target_vote_quantity_id = VoteQuantity.objects.get(rankings_id=id, items__id=rial_item_id).id
                print(target_vote_quantity_id)
                vote_quantity = get_object_or_404(VoteQuantity, pk=target_vote_quantity_id)
                vote_quantity.quantity += 1
                vote_quantity.save()
            # else:
            #     vote_quantity = VoteQuantity(
            #         quantity = 1,
            #     )
            #     vote_quantity.items_id = rial_item_id
            #     vote_quantity.rankings_id = ranking.uuid
            #     vote_quantity.save()
            message = str(self.request.user)+ "さんが「" + eval("ranking.item" + str(true_vote_item)) + "」に投票しました！"
            print("投票操作完了")
        
        if vote_status == "vote_cancel":
            search_item_id = VoteQuantity.objects.filter(rankings_id=id).order_by('-quantity')[:item_range][::1][true_vote_cancel_place - 1].items_id

            # 投票履歴削除
            vote_history = VoteHistory.objects.filter(voter=self.request.user, rankings_id=ranking.uuid, items_id=search_item_id).order_by('-created_at')[0]
            vote_history.delete()

            # 投票数を１つ減らす
            vote_quantity = VoteQuantity.objects.get(rankings_id=id, items_id=search_item_id)
            vote_quantity.quantity -= 1
            vote_quantity.save()

            message = str(self.request.user)+ "さんが「" + eval("ranking.item" + str(search_item_id)) + "」の投票を1票取り消しました！"
            print("投票取消操作完了")

        # テンプレート表示用情報の取得
        quantity_list = []
        for i in range(1,31):
            temp_item_id = Item.objects.filter(item=i)[0].id
            print("temp_item_id : " + str(temp_item_id))
            if VoteQuantity.objects.filter(rankings_id=id, items__id=temp_item_id).exists():
                temp_vote_quantity_id = VoteQuantity.objects.get(rankings_id=id, items__id=temp_item_id).id
                print("temp_vote_quantity_id : " + str(temp_vote_quantity_id))
                vote_quantity = get_object_or_404(VoteQuantity, pk=temp_vote_quantity_id)
                quantity_list.append(vote_quantity.quantity)
            else:
                quantity_list.append(0)

        # ランキングの項目名をリストに格納
        item_name_list = []
        for i in range(1,31):
            item_name_list.append(eval("ranking.item" + str(i)))

        # 投票数の順位をリストに格納
        quantity_rank_list = [0] * 30
        for i in range(len(VoteQuantity.objects.filter(rankings_id=id))):
            quantity_rank = int(str(VoteQuantity.objects.filter(rankings_id=id).order_by('-quantity')[:item_range][::1][i].items))
            print(quantity_rank)
            quantity_rank_list[i] = quantity_rank
        print(quantity_rank_list)

        sorted_item_name_list = [""] * 30
        sorted_quantity_list = [0] * 30
        for i in range(0, len(VoteQuantity.objects.filter(rankings_id=id))):
            sorted_item_name_list[i] = item_name_list[quantity_rank_list[i] - 1]
            sorted_quantity_list[i] = quantity_list[quantity_rank_list[i] - 1]
        
        # カテゴリをリスト化
        categories_list = []
        category_count = ranking.category.all().count()
        for i in range(category_count):
            categories_list.append(str(ranking.category.all()[i].name))

        # 投票履歴からそのユーザの投票数を取得
        if VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).exists():
            user_vote_quantity = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).count()
        else:
            user_vote_quantity = 0

        # 投票可能な数
        voteable_quantity = 1

        # ユーザが投票可能か判定
        if voteable_quantity - user_vote_quantity > 0:
            voteable_Judgment = 1
        else:
            voteable_Judgment = 0

        # ユーザの投票数をリストに格納し、全体の投票数の大きい順に並べ替え
        user_vote_quantity_list = [0] * item_range
        sorted_user_vote_quantity_list = [0] * item_range
        if VoteHistory.objects.filter(voter=self.request.user, rankings_id=id).exists():
            for i in range(user_vote_quantity):
                user_voted_items = VoteHistory.objects.filter(voter=self.request.user, rankings_id=id)[i].items.item
                user_vote_quantity_list[user_voted_items - 1] += 1
            for i in range(user_vote_quantity):
                sorted_user_vote_quantity_list[i] = user_vote_quantity_list[quantity_rank_list[i] - 1]


        print("uuid : " + str(id))
        print("item_range : " + str(item_range))
        print("item_name_list : " + str(item_name_list))
        print("quantity_list : " + str(quantity_list))
        print("quantity_rank_list : " + str(quantity_rank_list))
        print("sorted_item_name_list : " + str(sorted_item_name_list))
        print("sorted_quantity_list : " + str(sorted_quantity_list))
        print("categories_list : " + str(categories_list))
        print("user_vote_quantity: " + str(user_vote_quantity))

        context = {
            'message': message,
            'ranking': ranking,
            'sorted_item_name_list': sorted_item_name_list,
            'sorted_quantity_list': sorted_quantity_list,
            'item_range': item_range,
            'categories_list': categories_list,
            'voteable_Judgment': voteable_Judgment,
            'sorted_user_vote_quantity_list': sorted_user_vote_quantity_list,
        }
        return render(request, 'main_app/detail.html', context)