from django import forms

from dal import autocomplete

from pokemon.helpers import pokemon_sum_valid, repeated_pokemon_in_teams
from pokemon.models import Pokemon
from users.models import User

from .models import Battle, BattleTeam


class AutocompletePokemonForm(forms.ModelForm):
    pokemon_1 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="pokemon-autocomplete",
            attrs={  # noqa
                "data-placeholder": "Autocomplete pokemon",
                "data-minimum-input-length": 3,
            },
        ),
        required=True,
    )
    pokemon_2 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="pokemon-autocomplete",
            attrs={  # noqa
                "data-placeholder": "Autocomplete pokemon",
                "data-minimum-input-length": 3,
            },
        ),
        required=True,
    )
    pokemon_3 = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="pokemon-autocomplete",
            attrs={  # noqa
                "data-placeholder": "Autocomplete pokemon",
                "data-minimum-input-length": 3,
            },
        ),
        required=True,
    )


class CreateBattleForm(AutocompletePokemonForm):
    class Meta:
        model = Battle
        fields = ["opponent", "pokemon_1", "pokemon_2", "pokemon_3"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])

    def clean(self):
        cleaned_data = super().clean()

        is_pokemon_sum_valid = pokemon_sum_valid(
            [
                self.cleaned_data["pokemon_1"],
                self.cleaned_data["pokemon_2"],
                self.cleaned_data["pokemon_3"],
            ]
        )

        if not is_pokemon_sum_valid:
            raise forms.ValidationError("The sum of the Pokemon points can't be greater than 600.")

        return cleaned_data


class SelectOpponentTeamForm(AutocompletePokemonForm):
    class Meta:
        model = BattleTeam
        fields = ["pokemon_1", "pokemon_2", "pokemon_3"]

    def clean(self):
        cleaned_data = super().clean()
        pokemon = [
            self.cleaned_data["pokemon_1"],
            self.cleaned_data["pokemon_2"],
            self.cleaned_data["pokemon_3"],
        ]

        if repeated_pokemon_in_teams(pokemon, self.initial["battle"]):
            raise forms.ValidationError("You chose a Pokemon from your opponent's team. Try again.")

        if not pokemon_sum_valid(pokemon):
            raise forms.ValidationError("The sum of the Pokemon points can't be greater than 600.")

        return cleaned_data
