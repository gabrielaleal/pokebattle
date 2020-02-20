from django import forms

from .models import Battle  # noqa


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ["opponent"]
