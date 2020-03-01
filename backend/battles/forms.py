from django import forms

from pokemon.helpers import get_pokemon  # noqa
from users.models import User  # noqa

from .models import Battle  # noqa


class CreateBattleForm(forms.ModelForm):
    pokemon_1 = forms.IntegerField(required=True)
    pokemon_2 = forms.IntegerField(required=True)
    pokemon_3 = forms.IntegerField(required=True)

    class Meta:
        model = Battle
        fields = ["opponent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])

    def clean(self):
        cleaned_data = super().clean()

        for field in ["pokemon_1", "pokemon_2", "pokemon_3"]:
            response = get_pokemon(self.cleaned_data[field])  # requests from the API

            if response.status_code != 200:  # in case the pokemon does not exist on the API
                self.add_error(field, "Sorry, we couldn't find this Pokemon.")

        return cleaned_data
