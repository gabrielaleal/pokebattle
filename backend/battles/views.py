# from django.shortcuts import render
from django.views import generic

from .forms import CreateBattleForm  # noqa
from .models import Battle  # noqa


# Create your views here.
class CreateBattleView(generic.CreateView):  # noqa
    model = Battle
    template_name = "battles/create.html"
    form_class = CreateBattleForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
