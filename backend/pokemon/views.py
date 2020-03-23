from django.contrib.auth.mixins import LoginRequiredMixin

from dal import autocomplete

from .models import Pokemon


class PokemonAutocompleteView(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Pokemon.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
