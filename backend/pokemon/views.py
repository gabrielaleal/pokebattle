from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import format_html

from dal import autocomplete

from .models import Pokemon


class PokemonAutocompleteView(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Pokemon.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def get_result_label(self, result):
        return format_html('<img src="{}" height="60px"> {}', result.img_url, result.name)

    def get_selected_result_label(self, result):
        return result.name
