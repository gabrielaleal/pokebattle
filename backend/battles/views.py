from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views import generic

from .forms import CreateBattleForm, SelectOpponentTeamForm
from .models import Battle, BattleTeam
from .utils.battle import get_round_winner, run_battle_and_send_result_email


class CreateBattleView(LoginRequiredMixin, generic.CreateView):
    model = Battle
    template_name = "create_battle.html"
    form_class = CreateBattleForm
    success_url = reverse_lazy("battles:create-battle")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.status = "ONGOING"
        form.instance.save()
        pokemon = {}

        for field in ["pokemon_1", "pokemon_2", "pokemon_3"]:
            pokemon[field] = form.cleaned_data[field]

        BattleTeam.objects.create(
            creator=self.request.user, battle=form.instance, **pokemon
        )  # TODO: revisit this later

        success_message = format_html(
            f"<h5>Your battle against <b>{form.instance.opponent}</b> was created!</h5>"
            f"<div>Round 1: <b>{pokemon.get('pokemon_1').name}</b> - Attack: \
            {pokemon.get('pokemon_1').attack} | Defense: {pokemon.get('pokemon_1').defense} \
            | HP: {pokemon.get('pokemon_1').hp}</div>"
            f"<div>Round 2: <b>{pokemon.get('pokemon_2').name}</b> - Attack: \
            {pokemon.get('pokemon_2').attack} | Defense: {pokemon.get('pokemon_2').defense} \
            | HP: {pokemon.get('pokemon_2').hp}</div>"
            f"<div>Round 3: <b>{pokemon.get('pokemon_3').name}</b> - Attack: \
            {pokemon.get('pokemon_3').attack} | Defense: {pokemon.get('pokemon_3').defense} \
            | HP: {pokemon.get('pokemon_3').hp}</div>"
            f"<div style='margin-top: 10px;'>Now wait for your opponent to fight back!</div>"
        )
        messages.success(self.request, success_message)

        return super().form_valid(form)

    def get_initial(self):
        return {"creator_id": self.request.user.id}


class SelectOpponentTeamView(LoginRequiredMixin, generic.CreateView):
    template_name = "select_opponent_team.html"
    model = BattleTeam
    form_class = SelectOpponentTeamForm

    def dispatch(self, request, *args, **kwargs):
        battle = Battle.objects.filter(pk=self.kwargs["pk"]).first()
        if request.user != battle.opponent or battle.status == "SETTLED":
            return HttpResponseRedirect(reverse_lazy("home"))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        super(SelectOpponentTeamView, self).get_initial()
        battle = Battle.objects.filter(pk=self.kwargs["pk"]).first()
        self.initial = {"battle": battle}
        return self.initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["battle"] = Battle.objects.filter(pk=self.kwargs["pk"]).first()
        context["page_title"] = f"Select Battle #{context['battle'].id} Team"
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.battle = Battle.objects.filter(pk=self.kwargs["pk"]).first()
        form.instance.save()

        return super().form_valid(form)

    def get_success_url(self):
        run_battle_and_send_result_email(self.object)
        return reverse_lazy("battles:battle-detail", args=(self.kwargs["pk"],))


class SettledBattlesListView(LoginRequiredMixin, generic.ListView):
    template_name = "settled_battles_list.html"
    model = Battle
    login_url = reverse_lazy("login")

    def get_queryset(self):
        queryset = Battle.objects.filter(status="SETTLED").filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        )
        return queryset


class OnGoingBattlesListView(LoginRequiredMixin, generic.ListView):
    template_name = "on_going_battles_list.html"
    model = Battle
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["battles_i_created"] = (
            Battle.objects.filter(status="ONGOING")
            .filter(creator=self.request.user)
            .order_by("timestamp")
        )
        context["battles_im_invited"] = (
            Battle.objects.filter(status="ONGOING")
            .filter(opponent=self.request.user)
            .order_by("timestamp")
        )
        return context


class BattleDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "battle_details.html"
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creator_team = (
            BattleTeam.objects.filter(battle=self.object)
            .filter(creator=self.object.creator)
            .first()
        )

        opponent_team = (
            BattleTeam.objects.filter(battle=self.object)
            .filter(creator=self.object.opponent)
            .first()
        )

        context["creator_team"] = [
            creator_team.pokemon_1,
            creator_team.pokemon_2,
            creator_team.pokemon_3,
        ]

        if opponent_team:
            context["opponent_team"] = [
                opponent_team.pokemon_1,
                opponent_team.pokemon_2,
                opponent_team.pokemon_3,
            ]

            winners = []

            for creator_pokemon, opponent_pokemon in zip(
                context["creator_team"], context["opponent_team"]
            ):
                winners.append(get_round_winner(creator_pokemon, opponent_pokemon))

            context["matches"] = zip(
                [1, 2, 3], context["creator_team"], context["opponent_team"], winners
            )
        return context
