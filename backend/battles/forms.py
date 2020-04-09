from django import forms

from dal import autocomplete

from pokemon.helpers import (
    are_pokemon_positions_repeated,
    pokemon_sum_valid,
    repeated_pokemon_in_teams,
)
from pokemon.models import Pokemon
from users.models import User

from .models import Battle, BattleTeam


POSITION_CHOICES = [(1, 1), (2, 2), (3, 3)]


class AutocompletePokemonForm(forms.ModelForm):
    pokemon_1_position = forms.ChoiceField(choices=POSITION_CHOICES, label="Pokemon position")
    pokemon_2_position = forms.ChoiceField(choices=POSITION_CHOICES, label="Pokemon position")
    pokemon_3_position = forms.ChoiceField(choices=POSITION_CHOICES, label="Pokemon position")
    pokemon_1 = forms.ModelChoiceField(
        label="Pokemon",
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="pokemon-autocomplete",
            attrs={  # noqa
                "data-placeholder": "Autocomplete pokemon",
                "data-minimum-input-length": 3,
                "data-html": True,
            },
        ),
        required=True,
    )
    pokemon_2 = forms.ModelChoiceField(
        label="Pokemon",
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="pokemon-autocomplete",
            attrs={  # noqa
                "data-placeholder": "Autocomplete pokemon",
                "data-minimum-input-length": 3,
                "data-html": True,
            },
        ),
        required=True,
    )
    pokemon_3 = forms.ModelChoiceField(
        label="Pokemon",
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="pokemon-autocomplete",
            attrs={  # noqa
                "data-placeholder": "Autocomplete pokemon",
                "data-minimum-input-length": 3,
                "data-html": True,
            },
        ),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        if are_pokemon_positions_repeated(self.cleaned_data):
            raise forms.ValidationError("Each Pokemon must have a unique position.")

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


class CreateBattleForm(AutocompletePokemonForm):
    class Meta:
        model = Battle
        fields = [
            "opponent",
            "pokemon_1",
            "pokemon_1_position",
            "pokemon_2",
            "pokemon_2_position",
            "pokemon_3",
            "pokemon_3_position",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])


class SelectOpponentTeamForm(AutocompletePokemonForm):
    class Meta:
        model = BattleTeam
        fields = [
            "pokemon_1",
            "pokemon_1_position",
            "pokemon_2",
            "pokemon_2_position",
            "pokemon_3",
            "pokemon_3_position",
        ]

    def clean(self):
        cleaned_data = super().clean()
        pokemon = [
            self.cleaned_data["pokemon_1"],
            self.cleaned_data["pokemon_2"],
            self.cleaned_data["pokemon_3"],
        ]

        if repeated_pokemon_in_teams(pokemon, self.initial["battle"]):
            raise forms.ValidationError("You chose a Pokemon from your opponent's team. Try again.")

        return cleaned_data
