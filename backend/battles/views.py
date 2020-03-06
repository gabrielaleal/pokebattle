from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views import generic

from pokemon.helpers import save_pokemon  # noqa

from .forms import CreateBattleForm  # noqa
from .models import Battle, BattleTeam  # noqa


class CreateBattleView(generic.CreateView):  # noqa
    model = Battle
    template_name = "create_battle.html"
    form_class = CreateBattleForm
    success_url = reverse_lazy("battles:create-battle")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.save()
        pokemon = {}

        for field in ["pokemon_1", "pokemon_2", "pokemon_3"]:
            pokemon[field] = save_pokemon(form.cleaned_data[field])

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
