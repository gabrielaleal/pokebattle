from django import forms

from dal import autocomplete

from pokemon.helpers import pokemon_exists, pokemon_sum_valid
from pokemon.models import Pokemon
from users.models import User

from .models import Battle


class CreateBattleForm(forms.ModelForm):
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

    class Meta:
        model = Battle
        fields = ["opponent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])

    def clean(self):
        cleaned_data = super().clean()

        for field in ["pokemon_1", "pokemon_2", "pokemon_3"]:
            response = pokemon_exists(self.cleaned_data[field])

            if not response:  # in case the pokemon does not exist on the API
                self.add_error(field, "Sorry, we couldn't find this Pokemon.")

        if (
            self.cleaned_data.get("pokemon_1")
            and self.cleaned_data.get("pokemon_2")
            and self.cleaned_data.get("pokemon_3")
        ):
            is_pokemon_sum_valid = pokemon_sum_valid(
                [
                    self.cleaned_data["pokemon_1"],
                    self.cleaned_data["pokemon_2"],
                    self.cleaned_data["pokemon_3"],
                ]
            )

            if not is_pokemon_sum_valid:
                raise forms.ValidationError(
                    "The sum of the Pokemon points can't be greater than 600."
                )

        return cleaned_data
