# from django.shortcuts import render
from django.views import generic

from pokemon.helpers import save_pokemon  # noqa

from .forms import CreateBattleForm  # noqa
from .models import Battle, BattleTeam  # noqa


class CreateBattleView(generic.CreateView):  # noqa
    model = Battle
    template_name = "create_battle.html"
    form_class = CreateBattleForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.save()

        pokemon = {}

        for field in ["pokemon_1", "pokemon_2", "pokemon_3"]:
            pokemon[field] = save_pokemon(form.cleaned_data[field])

        BattleTeam.objects.create(
            creator=self.request.user, battle=form.instance, **pokemon
        )  # TODO: revisit this later

        return super().form_valid(form)

    def get_initial(self):
        return {"creator_id": self.request.user.id}
