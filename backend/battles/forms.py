from django import forms

from users.models import User  # noqa

from .models import Battle  # noqa


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ["opponent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=self.initial["creator_id"])
